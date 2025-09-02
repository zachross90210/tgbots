import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from telegram.error import TelegramError
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
LANGUAGE, COUNTRY, PROBLEM = range(3)

# Language translations
TRANSLATIONS = {
    "en": {
        "welcome": "👋 Welcome to Men's Health Advisor!",
        "select_country": "Please select your country:",
        "select_concern": "What would you like to improve?\n\nChoose your main concern:",
        "prostate_button": "Prostate Health Concerns",
        "potency_button": "Potency Enhancement",
        "prostate_offer": (
            "🏥 Take Care of Your Prostate Health!\n\n"
            "Our clinically proven solution helps:\n"
            "✅ Reduce inflammation\n"
            "✅ Improve urination\n"
            "✅ Enhance quality of life\n\n"
            "Click below to learn more!"
        ),
        "potency_offer": (
            "💪 Boost Your Confidence!\n\n"
            "Our premium formula provides:\n"
            "✅ Enhanced performance\n"
            "✅ Increased stamina\n"
            "✅ Natural ingredients\n\n"
            "Click below to learn more!"
        ),
        "get_solution": "🔥 Get Your Solution Now 🔥",
        "not_available": "Sorry, this offer is not available in your country yet."
    },
    "es": {
        "welcome": "👋 ¡Bienvenido al Asesor de Salud Masculina!",
        "select_country": "Por favor seleccione su país:",
        "select_concern": "¿Qué le gustaría mejorar?\n\nElija su principal preocupación:",
        "prostate_button": "Problemas de Próstata",
        "potency_button": "Mejora de la Potencia",
        "prostate_offer": (
            "🏥 ¡Cuide la salud de su próstata!\n\n"
            "Nuestra solución clínicamente probada ayuda a:\n"
            "✅ Reducir la inflamación\n"
            "✅ Mejorar la micción\n"
            "✅ Mejorar la calidad de vida\n\n"
            "¡Haga clic abajo para saber más!"
        ),
        "potency_offer": (
            "💪 ¡Aumente su confianza!\n\n"
            "Nuestra fórmula premium proporciona:\n"
            "✅ Mejor rendimiento\n"
            "✅ Mayor resistencia\n"
            "✅ Ingredientes naturales\n\n"
            "¡Haga clic abajo para saber más!"
        ),
        "get_solution": "🔥 ¡Obtenga Su Solución Ahora! 🔥",
        "not_available": "Lo sentimos, esta oferta no está disponible en su país todavía."
    },
    "ru": {
        "welcome": "👋 Добро пожаловать в Консультант по мужскому здоровью!",
        "select_country": "Пожалуйста, выберите вашу страну:",
        "select_concern": "Что бы вы хотели улучшить?\n\nВыберите вашу основную проблему:",
        "prostate_button": "Проблемы с простатой",
        "potency_button": "Улучшение потенции",
        "prostate_offer": (
            "🏥 Позаботьтесь о здоровье простаты!\n\n"
            "Наше клинически проверенное решение помогает:\n"
            "✅ Уменьшить воспаление\n"
            "✅ Улучшить мочеиспускание\n"
            "✅ Повысить качество жизни\n\n"
            "Нажмите ниже, чтобы узнать больше!"
        ),
        "potency_offer": (
            "💪 Повысьте свою уверенность!\n\n"
            "Наша премиум формула обеспечивает:\n"
            "✅ Улучшенную производительность\n"
            "✅ Повышенную выносливость\n"
            "✅ Натуральные ингредиенты\n\n"
            "Нажмите ниже, чтобы узнать больше!"
        ),
        "get_solution": "🔥 Получите ваше решение сейчас 🔥",
        "not_available": "Извините, это предложение пока недоступно в вашей стране."
    }
}

# Offers dictionary by country
OFFERS = {
    "russia": {
        "prostatitis": "https://example.com/ru/prostatitis-offer",
        "potency": "https://example.com/ru/potency-offer"
    },
    "usa": {
        "prostatitis": "https://example.com/us/prostatitis-offer", 
        "potency": "https://example.com/us/potency-offer"
    },
    "ukraine": {
        "prostatitis": "https://example.com/ua/prostatitis-offer",
        "potency": "https://example.com/ua/potency-offer"
    },
    "germany": {
        "prostatitis": "https://example.com/de/prostatitis-offer",
        "potency": "https://example.com/de/potency-offer"
    },
    "france": {
        "prostatitis": "https://example.com/fr/prostatitis-offer",
        "potency": "https://example.com/fr/potency-offer"
    },
    "spain": {
        "prostatitis": "https://example.com/es/prostatitis-offer",
        "potency": "https://example.com/es/potency-offer"
    },
    "italy": {
        "prostatitis": "https://example.com/it/prostatitis-offer",
        "potency": "https://example.com/it/potency-offer"
    }
}

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors caused by updates."""
    logger.error("Exception while handling an update:", exc_info=context.error)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask for language."""
    welcome_message = (
        "👋 Welcome / Bienvenido / Добро пожаловать!\n\n"
        "🌍 Please select your language / Por favor seleccione su idioma / "
        "Пожалуйста, выберите ваш язык:"
    )
    
    keyboard = [
        [InlineKeyboardButton("English 🇬🇧", callback_data="en")],
        [InlineKeyboardButton("Español 🇪🇸", callback_data="es")],
        [InlineKeyboardButton("Русский 🇷🇺", callback_data="ru")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)
    return LANGUAGE

async def select_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle language selection and ask for country."""
    query = update.callback_query
    await query.answer()
    
    language = query.data
    context.user_data['language'] = language
    
    keyboard = [
        [InlineKeyboardButton("Russia 🇷🇺", callback_data="russia")],
        [InlineKeyboardButton("USA 🇺🇸", callback_data="usa")],
        [InlineKeyboardButton("Ukraine 🇺🇦", callback_data="ukraine")],
        [InlineKeyboardButton("Germany 🇩🇪", callback_data="germany")],
        [InlineKeyboardButton("France 🇫🇷", callback_data="france")],
        [InlineKeyboardButton("Spain 🇪🇸", callback_data="spain")],
        [InlineKeyboardButton("Italy 🇮🇹", callback_data="italy")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"{TRANSLATIONS[language]['welcome']}\n\n"
        f"{TRANSLATIONS[language]['select_country']}",
        reply_markup=reply_markup
    )
    return COUNTRY

async def select_country(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle country selection and ask about health concerns."""
    query = update.callback_query
    await query.answer()
    
    context.user_data['country'] = query.data
    language = context.user_data['language']
    
    keyboard = [
        [InlineKeyboardButton(TRANSLATIONS[language]['prostate_button'], callback_data="prostatitis")],
        [InlineKeyboardButton(TRANSLATIONS[language]['potency_button'], callback_data="potency")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        TRANSLATIONS[language]['select_concern'],
        reply_markup=reply_markup
    )
    return PROBLEM

async def show_offer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show relevant offer based on country and concern."""
    query = update.callback_query
    await query.answer()
    
    country = context.user_data.get('country')
    language = context.user_data.get('language')
    concern = query.data
    
    if country in OFFERS and concern in OFFERS[country]:
        offer_url = OFFERS[country][concern]
        keyboard = [[InlineKeyboardButton(
            TRANSLATIONS[language]['get_solution'], 
            url=offer_url
        )]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        message = TRANSLATIONS[language]['prostate_offer'] if concern == 'prostatitis' else TRANSLATIONS[language]['potency_offer']
        
        await query.edit_message_text(
            message,
            reply_markup=reply_markup
        )
    else:
        await query.edit_message_text(
            TRANSLATIONS[language]['not_available']
        )
    
    return ConversationHandler.END

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a help message when the command /help is issued."""
    await start(update, context)

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
                LANGUAGE: [CallbackQueryHandler(select_language)],
                COUNTRY: [CallbackQueryHandler(select_country)],
                PROBLEM: [CallbackQueryHandler(show_offer)]
            },
            fallbacks=[CommandHandler("help", help_command)]
        )

        application.add_handler(conv_handler)
        application.add_error_handler(error_handler)

        logger.info("Bot started successfully!")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        raise

if __name__ == "__main__":
    main()