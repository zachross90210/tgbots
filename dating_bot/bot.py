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

QUIZ, END = range(2)

WELCOME_TEXT = (
    "🌍 Welcome! Bienvenue! Willkommen! Добро пожаловать! 欢迎! स्वागत है! خوش آمدید! أهلاً وسهلاً!\n\n"
    "Wanna meet someone new? Just a few quick taps…"
)

QUESTIONS = [
    {
        "text": "1. What are you looking for?",
        "options": [["Casual fun", "Long-term"], ["Just chatting", "Not sure"]]
    },
    {
        "text": "2. What excites you most?",
        "options": [["Flirty talk", "Chemistry"], ["Deep connection", "All of it"]]
    },
    {
        "text": "3. How soon to meet?",
        "options": [["Tonight", "This week"], ["Let's chat", "No rush"]]
    },
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(WELCOME_TEXT)
    context.user_data['answers'] = []
    return await send_question(update, context, 0)

async def send_question(update, context, index):
    q = QUESTIONS[index]
    markup = ReplyKeyboardMarkup(q["options"], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(q["text"], reply_markup=markup)
    return QUIZ

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['answers'].append(update.message.text.strip())
    current = len(context.user_data['answers'])
    if current < len(QUESTIONS):
        return await send_question(update, context, current)
    else:
        await update.message.reply_text(
            f"Great match! Let’s get you started 👉 {DATING_URL}",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Cancelled.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={QUIZ: [MessageHandler(filters.TEXT & ~filters.COMMAND, quiz)]},
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(conv)
    app.run_polling()

if __name__ == "__main__":
    main()
