import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

if not os.getenv("TELEGRAM_BOT_TOKEN"):
    raise ValueError("No TELEGRAM_BOT_TOKEN found in .env file. Please add your bot token.")

# Conversation states
LANGUAGE, SUBSCRIBE, START_GAME, REGISTRATION, ID_CHECK = range(5)

# Channel link
CHANNEL_LINK = "https://t.me/+b4wB-amqey4zYTMy"  # Replace with actual channel link
REGISTRATION_LINK = "https://3rjue.bemobtrk.com/go/f2eab0c2-6178-410b-9713-fc218e06afdf?"
SIGNALBOT_LINK = "https://grizliq.github.io/gemblbot.main/"
# Language translations

OFFER_LINKS = """
    <a href="https://3rjue.bemobtrk.com/go/f2eab0c2-6178-410b-9713-fc218e06afdf">LINK1</a>\n
    <a href="https://3rjue.bemobtrk.com/go/86677532-151d-44da-9ed3-71823c1bac96">LINK2</a>\n
    <a href="https://3rjue.bemobtrk.com/go/bc4e707a-b8ae-44c4-8b86-aaf2fae51fdd">LINK3</a>\n
""";

TRANSLATIONS = {
    "ru": {
        "welcome": "Добро пожаловать, 🚀 SIGNAL BOT!",
        "subscribe_text": "Для использования бота - подпишись на наш канал🤝",
        "subscribe_channel": "Подписаться на канал",
        "already_subscribed": "Я уже подписан",
        "welcome_team": (
            "🧩 Команда W рада приветствовать тебя в своих рядах!\n\n"
            "🔥 ЛУЧШИЙ БОТ! ✅ проводит полную аналитику вашего игрового аккаунта с сигналами, "
            "при помощи которых вы сможете выйти на стабильный доход с казино!\n\n"
            "💶 Проект основан на Искусственном Интеллекте Open AI"
        ),
        "how_to_start": "Как начать играть?",
        "bot_info": (
            "🤖Бот основан и обучен на кластерной нейронной сети OpenAI!\n\n"
            "⚜️Для обучения бота было сыграно 🎰30,000 игр.\n\n"
            "В настоящее время пользователи бота успешно генерируют 15-25% от своего 💸 капитала ежедневно!\n\n"
            "Бот все еще проходит проверки и исправления! Точность бота составляет 92%!\n\n"
            "Чтобы достичь максимальной прибыли, следуйте этой инструкции:\n\n"
            "🟢 1. Зарегистрируйтесь в в казино 1WIN по одной из ссылок ниже:\n\n"
            f"👉 {OFFER_LINKS}"
            "[Если не открывается, воспользуйтесь VPN (Швеция). В Play Market/App Store есть много бесплатных сервисов, "
            "например: Vpnify, Planet VPN, Hotspot VPN и т.д.!]\n\n"
            "❗️Без регистрации и промокода доступ к сигналам не будет открыт❗️\n\n"
            "🟢 2. Пополните баланс своего счета.\n"
            "🟢 3. Перейдите в раздел игр 1win и выберите игру.\n"
            "🟢 4. Установите количество ловушек на три. Это важно!\n"
            "🟢 5. Запросите сигнал у бота и ставьте ставки в соответствии с сигналами от бота.\n"
            "🟢 6. В случае неудачного сигнала рекомендуем удвоить (x²) вашу ставку, чтобы полностью покрыть убыток с помощью следующего сигнала."
        ),
        "next": "Дальше",
        "registration_info": (
            "🌐 Шаг 2 - Зарегистрируйся.\n\n"
            "✦ Для синхронизации с нашим ботом необходимо зарегистрировать НОВЫЙ аккаунт. "
            "Во время регистрации обязательно нужно ввести промокод - DOTHEDEP (иначе бот не заработает ❗️)\n\n"
            "✦ Если Вы переходите по ссылке и попадаете на старый аккаунт, необходимо выйти с него и заново перейти по ссылке регистрации!"
        ),
        "register": "Регистрация",
        "registered": "Я зарегистрировался",
        "id_check": (
            "🌐 ШАГ 3 - Пройди проверку\n\n"
            "После регистрации, для получения сигналов необходимо отправить в чат с ботом ваш ID.\n\n"
            "ГДЕ ВЗЯТЬ ID⁉️\n\n"
            "1. Нажмите кнопку \"Пополнить\"\n"
            "2. Скопируйте ваш ID, он находится справа сверху в открывшемся окне\n"
            "3. Отправьте его в чат с ботом✅\n\n"
            "‼️Обязательно прочитайте инструкцию‼️"
        ),
        "instruction": "📋 Инструкция",
        "back_to_id": "⬅️ Назад к проверке ID"
    },
    "en": {
        "welcome": "Welcome to 🚀 SIGNAL BOT!",
        "subscribe_text": "To use the bot - subscribe to our channel🤝",
        "subscribe_channel": "Subscribe to channel",
        "already_subscribed": "I'm already subscribed",
        "welcome_team": (
            "🧩 Team W is glad to welcome you to our ranks!\n\n"
            "🔥 BEST BOT! ✅ conducts a complete analysis of your gaming account with signals, "
            "with which you can achieve stable income from the casino!\n\n"
            "💶 The project is based on Artificial Intelligence Open AI"
        ),
        "how_to_start": "How to start playing?",
        "bot_info": (
            "🤖Bot is based and trained on OpenAI cluster neural network!\n\n"
            "⚜️To train the bot, 🎰30,000 games were played.\n\n"
            "Currently, bot users successfully generate 15-25% of their 💸 capital daily!\n\n"
            "The bot is still undergoing checks and corrections! Bot accuracy is 92%!\n\n"
            "To achieve maximum profit, follow this instruction:\n\n"
            "🟢 1. Register at 1WIN casino by one of the links below:\n\n"
            f"👉 {OFFER_LINKS}"
            "[If it doesn't open, use VPN (Sweden). Play Market/App Store has many free services, "
            "for example: Vpnify, Planet VPN, Hotspot VPN, etc.!]\n\n"
            "❗️Without registration and promo code, access to signals will not be opened❗️\n\n"
            "🟢 2. Top up your account balance.\n"
            "🟢 3. Go to 1win games section and select a game.\n"
            "🟢 4. Set the number of mines to three. This is important!\n"
            "🟢 5. Request a signal from the bot and place bets according to the signals from the bot.\n"
            "🟢 6. In case of an unsuccessful signal, we recommend doubling (x²) your bet to fully cover the loss with the next signal."
        ),
        "next": "Next",
        "registration_info": (
            "🌐 Step 2 - Register.\n\n"
            "✦ To synchronize with our bot, you need to register a NEW account. "
            "During registration, you must enter the promo code - DOTHEDEP (otherwise the bot won't work ❗️)\n\n"
            "✦ If you click the link and get to an old account, you need to log out and click the registration link again!"
        ),
        "register": "Registration",
        "registered": "I registered",
        "id_check": (
            "🌐 STEP 3 - Pass verification\n\n"
            "After registration, to receive signals you need to send your ID to the bot chat.\n\n"
            "WHERE TO GET ID⁉️\n\n"
            "1. Click the \"Top up\" button\n"
            "2. Copy your ID, it's located on the top right in the opened window\n"
            "3. Send it to the bot chat✅\n\n"
            "‼️Be sure to read the instruction‼️"
        ),
        "instruction": "📋 Instruction",
        "back_to_id": "⬅️ Back to ID verification"
    },
    "es": {
        "welcome": "¡Bienvenido a 🚀 SIGNAL BOT!",
        "subscribe_text": "Para usar el bot - suscríbete a nuestro canal🤝",
        "subscribe_channel": "Suscribirse al canal",
        "already_subscribed": "Ya estoy suscrito",
        "welcome_team": (
            "🧩 ¡El equipo W se alegra de darte la bienvenida a nuestras filas!\n\n"
            "🔥 ¡MEJOR BOT! ✅ realiza un análisis completo de tu cuenta de juego con señales, "
            "con las que puedes lograr ingresos estables del casino!\n\n"
            "💶 El proyecto está basado en Inteligencia Artificial Open AI"
        ),
        "how_to_start": "¿Cómo empezar a jugar?",
        "bot_info": (
            "🤖¡El bot está basado y entrenado en la red neuronal de clúster OpenAI!\n\n"
            "⚜️Para entrenar el bot, se jugaron 🎰30,000 juegos.\n\n"
            "¡Actualmente, los usuarios del bot generan exitosamente 15-25% de su 💸 capital diariamente!\n\n"
            "¡El bot aún está pasando por verificaciones y correcciones! ¡La precisión del bot es del 92%!\n\n"
            "Para lograr la máxima ganancia, sigue esta instrucción:\n\n"
            "🟢 1. Regístrate en la casa de casino 1WIN por una de las siguientes:\n\n"
            f"👉 {OFFER_LINKS}"
            "[Si no abre, usa VPN (Suecia). Play Market/App Store tiene muchos servicios gratuitos, "
            "por ejemplo: Vpnify, Planet VPN, Hotspot VPN, ¡etc.!]\n\n"
            "❗️Sin registro y código promocional, no se abrirá el acceso a las señales❗️\n\n"
            "🟢 2. Recarga el saldo de tu cuenta.\n"
            "🟢 3. Ve a la sección de juegos de 1win y selecciona un juego.\n"
            "🟢 4. Establece el número de minas en tres. ¡Esto es importante!\n"
            "🟢 5. Solicita una señal del bot y haz apuestas según las señales del bot.\n"
            "🟢 6. En caso de una señal fallida, recomendamos doblar (x²) tu apuesta para cubrir completamente la pérdida con la siguiente señal."
        ),
        "next": "Siguiente",
        "registration_info": (
            "🌐 Paso 2 - Regístrate.\n\n"
            "✦ Para sincronizar con nuestro bot, necesitas registrar una cuenta NUEVA. "
            "Durante el registro, debes ingresar el código promocional - DOTHEDEP (¡de lo contrario el bot no funcionará ❗️)\n\n"
            "✦ ¡Si haces clic en el enlace y llegas a una cuenta antigua, necesitas cerrar sesión y hacer clic en el enlace de registro nuevamente!"
        ),
        "register": "Registro",
        "registered": "Me registré",
        "id_check": (
            "🌐 PASO 3 - Pasa la verificación\n\n"
            "Después del registro, para recibir señales necesitas enviar tu ID al chat del bot.\n\n"
            "¿DÓNDE OBTENER EL ID⁉️\n\n"
            "1. Haz clic en el botón \"Recargar\"\n"
            "2. Copia tu ID, está ubicado en la parte superior derecha en la ventana abierta\n"
            "3. Envíalo al chat del bot✅\n\n"
            "‼️Asegúrate de leer la instrucción‼️"
        ),
        "instruction": "📋 Instrucción",
        "back_to_id": "⬅️ Volver a verificación de ID"
    },
    "pt": {
        "welcome": "Bem-vindo ao 🚀 SIGNAL BOT!",
        "subscribe_text": "Para usar o bot - inscreva-se no nosso canal🤝",
        "subscribe_channel": "Inscrever-se no canal",
        "already_subscribed": "Já estou inscrito",
        "welcome_team": (
            "🧩 A equipe W está feliz em dar-lhe as boas-vindas às nossas fileiras!\n\n"
            "🔥 MELHOR BOT! ✅ conduz uma análise completa da sua conta de jogo com sinais, "
            "com os quais você pode alcançar renda estável do cassino!\n\n"
            "💶 O projeto é baseado em Inteligência Artificial Open AI"
        ),
        "how_to_start": "Como começar a jogar?",
        "bot_info": (
            "🤖Bot é baseado e treinado na rede neural de cluster OpenAI!\n\n"
            "⚜️Para treinar o bot, 🎰30.000 jogos foram jogados.\n\n"
            "Atualmente, os usuários do bot geram com sucesso 15-25% do seu 💸 capital diariamente!\n\n"
            "O bot ainda está passando por verificações e correções! A precisão do bot é de 92%!\n\n"
            "Para alcançar o lucro máximo, siga esta instrução:\n\n"
            "🟢 1. Registre-se na casa de casino 1WIN por uma de las siguientes:\n\n"
            f"👉 {OFFER_LINKS}"
            "[Se não abrir, use VPN (Suécia). Play Market/App Store tem muitos serviços gratuitos, "
            "por exemplo: Vpnify, Planet VPN, Hotspot VPN, etc.!]\n\n"
            "❗️Sem registro e código promocional, o acesso aos sinais não será aberto❗️\n\n"
            "🟢 2. Recarregue o saldo da sua conta.\n"
            "🟢 3. Vá para a seção de jogos do 1win e selecione um jogo.\n"
            "🟢 4. Defina o número de minas para três. Isso é importante!\n"
            "🟢 5. Solicite um sinal do bot e faça apostas de acordo com os sinais do bot.\n"
            "🟢 6. Em caso de sinal mal-sucedido, recomendamos dobrar (x²) sua aposta para cobrir completamente a perda com o próximo sinal."
        ),
        "next": "Próximo",
        "registration_info": (
            "🌐 Passo 2 - Registre-se.\n\n"
            "✦ Para sincronizar com nosso bot, você precisa registrar uma conta NOVA. "
            "Durante o registro, você deve inserir o código promocional - DOTHEDEP (caso contrário o bot não funcionará ❗️)\n\n"
            "✦ Se você clicar no link e chegar a uma conta antiga, precisa sair e clicar no link de registro novamente!"
        ),
        "register": "Registro",
        "registered": "Eu me registrei",
        "id_check": (
            "🌐 PASSO 3 - Passe pela verificação\n\n"
            "Após o registro, para receber sinais você precisa enviar seu ID para o chat do bot.\n\n"
            "ONDE OBTER O ID⁉️\n\n"
            "1. Clique no botão \"Recarregar\"\n"
            "2. Copie seu ID, ele está localizado no canto superior direito na janela aberta\n"
            "3. Envie-o para o chat do bot✅\n\n"
            "‼️Certifique-se de ler a instrução‼️"
        ),
        "instruction": "📋 Instrução",
        "back_to_id": "⬅️ Voltar à verificação de ID"
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start conversation and ask for language."""
    keyboard = [
        [InlineKeyboardButton("🇷🇺 Русский", callback_data="ru")],
        [InlineKeyboardButton("🇬🇧 English", callback_data="en")],
        [InlineKeyboardButton("🇪🇸 Español", callback_data="es")],
        [InlineKeyboardButton("🇧🇷 Português", callback_data="pt")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Please select your language / Выберите язык / Selecciona tu idioma / Selecione seu idioma:",
        reply_markup=reply_markup
    )
    return LANGUAGE

async def language_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle language selection."""
    query = update.callback_query
    await query.answer()
    
    language = query.data
    context.user_data['language'] = language
    
    keyboard = [
        [InlineKeyboardButton(TRANSLATIONS[language]["subscribe_channel"], url=CHANNEL_LINK)],
        [InlineKeyboardButton(TRANSLATIONS[language]["already_subscribed"], callback_data="subscribed")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"{TRANSLATIONS[language]['welcome']}\n\n{TRANSLATIONS[language]['subscribe_text']}",
        reply_markup=reply_markup
    )
    return SUBSCRIBE

async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle subscription confirmation."""
    query = update.callback_query
    await query.answer()
    
    language = context.user_data['language']
    keyboard = [[InlineKeyboardButton(TRANSLATIONS[language]["how_to_start"], callback_data="how_to_start")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(TRANSLATIONS[language]["welcome_team"], reply_markup=reply_markup)
    return START_GAME

async def handle_game_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle game start button press."""
    query = update.callback_query
    await query.answer()
    
    language = context.user_data['language']
    keyboard = [[InlineKeyboardButton(TRANSLATIONS[language]["next"], callback_data="next")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(TRANSLATIONS[language]["bot_info"], reply_markup=reply_markup, parse_mode="HTML", disable_web_page_preview=True)
    return REGISTRATION

async def handle_registration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle registration step."""
    query = update.callback_query
    await query.answer()
    
    language = context.user_data['language']
    keyboard = [
        [InlineKeyboardButton(TRANSLATIONS[language]["register"], url=REGISTRATION_LINK)],
        [InlineKeyboardButton(TRANSLATIONS[language]["registered"], callback_data="registered")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(TRANSLATIONS[language]["registration_info"], reply_markup=reply_markup)
    return ID_CHECK

async def handle_registered(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle when user confirms registration."""
    query = update.callback_query
    await query.answer()
    
    language = context.user_data['language']
    keyboard = [[InlineKeyboardButton(TRANSLATIONS[language]["instruction"], callback_data="show_instruction")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(TRANSLATIONS[language]["id_check"], reply_markup=reply_markup)
    return ID_CHECK

async def show_instruction(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show bot instruction (bot_info content)."""
    query = update.callback_query
    await query.answer()
    
    language = context.user_data['language']
    keyboard = [[InlineKeyboardButton(TRANSLATIONS[language]["back_to_id"], callback_data="back_to_id")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(TRANSLATIONS[language]["bot_info"], reply_markup=reply_markup, parse_mode="HTML", disable_web_page_preview=True)
    return ID_CHECK

async def back_to_id_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Return back to ID check step."""
    query = update.callback_query
    await query.answer()
    
    language = context.user_data['language']
    keyboard = [[InlineKeyboardButton(TRANSLATIONS[language]["instruction"], callback_data="show_instruction")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    REGISTRATION_LINK
    await query.edit_message_text(TRANSLATIONS[language]["id_check"], reply_markup=reply_markup)
    return ID_CHECK

async def handle_id_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle ID input from user."""
    language = context.user_data.get('language', 'ru')
    keyboard = [[InlineKeyboardButton("🔗 Link", url=SIGNALBOT_LINK)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Open signal bot:", reply_markup=reply_markup)
    return ConversationHandler.END

def main() -> None:
    """Start the bot."""
    try:
        application = (
            Application.builder()
            .token(os.getenv("TELEGRAM_BOT_TOKEN"))
            .build()
        )

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", start)],
            states={
                LANGUAGE: [CallbackQueryHandler(language_selected)],
                SUBSCRIBE: [CallbackQueryHandler(check_subscription)],
                START_GAME: [CallbackQueryHandler(handle_game_start)],
                REGISTRATION: [CallbackQueryHandler(handle_registration, pattern="^next$")],
                ID_CHECK: [
                    CallbackQueryHandler(handle_registered, pattern="^registered$"),
                    CallbackQueryHandler(show_instruction, pattern="^show_instruction$"),
                    CallbackQueryHandler(back_to_id_check, pattern="^back_to_id$"),
                    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_id_input)
                ]
            },
            fallbacks=[CommandHandler("start", start)]
        )

        application.add_handler(conv_handler)
        logger.info("Bot started successfully!")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        logger.error(f"Error starting bot: {e}")

if __name__ == '__main__':
    main()
