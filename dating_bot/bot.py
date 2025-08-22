from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)

import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
DATING_URL = os.getenv("DATING_URL")

LANGUAGE, QUIZ = range(2)

LANGUAGES = {
    "🇺🇸 English": "en",
    "🇷🇺 Русский": "ru",
    "🇫🇷 Français": "fr"
}

TRANSLATIONS = {
    "en": {
        "welcome": "🌍 Welcome! Wanna meet someone new? Just a few quick taps…",
        "questions": [
            ("1. What are you looking for?", [["Casual fun", "Long-term"], ["Just chatting", "Not sure"]]),
            ("2. What excites you most?", [["Flirty talk", "Chemistry"], ["Deep connection", "All of it"]]),
            ("3. How soon to meet?", [["Tonight", "This week"], ["Let's chat", "No rush"]]),
        ],
        "result": "Great! Register now. You'll get an email. Then access the site with women 👉 <a href='{}'>CLICK HERE</a>",
        "cancel": "Cancelled.",
    },
    "ru": {
        "welcome": "🌍 Добро пожаловать! Хотите познакомиться? Пара быстрых вопросов…",
        "questions": [
            ("1. Что вы ищете?", [["Флирт", "Серьёзные отношения"], ["Просто общение", "Не уверен"]]),
            ("2. Что вас больше всего заводит?", [["Флирт", "Химия"], ["Глубокая связь", "Всё сразу"]]),
            ("3. Когда хотите встретиться?", [["Сегодня", "На этой неделе"], ["Сначала пообщаемся", "Не спешу"]]),
        ],
        "result": "Идеально! Переходи регистрируйся. Тебе на почту придет письмо. Затем ты получишь доступ к сайту с женщинами 👉  <a href='{}'>ЖМИ СЮДА</a>",
        "cancel": "Отменено.",
    },
    "fr": {
        "welcome": "🌍 Bienvenue ! Prêt à rencontrer quelqu’un ? Quelques clics suffisent…",
        "questions": [
            ("1. Que recherchez-vous ?", [["Aventure", "Relation sérieuse"], ["Discuter", "Je ne sais pas"]]),
            ("2. Qu’est-ce qui vous excite le plus ?", [["Séduction", "Alchimie"], ["Connexion profonde", "Tout ça"]]),
            ("3. Quand se rencontrer ?", [["Ce soir", "Cette semaine"], ["D’abord discuter", "Pas pressé"]]),
        ],
        "result": "Parfait ! Inscris-toi. Tu recevras un email. Puis tu accèderas au site avec des femmes 👉 <a href='{}'>Cliquez ici</a>",
        "cancel": "Annulé.",
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [[k] for k in LANGUAGES]
    await update.message.reply_text(
        "Choose your language / Выберите язык / Choisissez la langue:",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return LANGUAGE

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang_key = update.message.text.strip()
    if lang_key not in LANGUAGES:
        await update.message.reply_text("Please choose from the options.")
        return LANGUAGE
    lang = LANGUAGES[lang_key]
    context.user_data['lang'] = lang
    context.user_data['answers'] = []
    await update.message.reply_text(
        TRANSLATIONS[lang]["welcome"],
        reply_markup=ReplyKeyboardRemove()
    )
    return await send_question(update, context, 0)

async def send_question(update, context, index):
    lang = context.user_data['lang']
    q_text, options = TRANSLATIONS[lang]["questions"][index]
    markup = ReplyKeyboardMarkup(options, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(q_text, reply_markup=markup)
    return QUIZ

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['answers'].append(update.message.text.strip())
    current = len(context.user_data['answers'])
    if current < 3:
        return await send_question(update, context, current)
    else:
        lang = context.user_data['lang']
        await update.message.reply_text(
            TRANSLATIONS[lang]["result"].format(DATING_URL),
            reply_markup=ReplyKeyboardRemove(),
            disable_web_page_preview=True,
            parse_mode="HTML"
        )
        return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = context.user_data.get('lang', 'en')
    await update.message.reply_text(TRANSLATIONS[lang]["cancel"], reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_language)],
            QUIZ: [MessageHandler(filters.TEXT & ~filters.COMMAND, quiz)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(conv)
    app.run_polling()

if __name__ == "__main__":
    main()
