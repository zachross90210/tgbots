import os
import random
import logging
import requests
from datetime import datetime
import pytz
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
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

if not os.getenv("PROXY_AFFILIATE_URL"):
    logger.warning("No PROXY_AFFILIATE_URL found in .env file. Premium proxy feature will be limited.")

# Constants
HTTP_PROXY_URL = "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http_checked.txt"
SOCKS5_PROXY_URL = "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks5_checked.txt"

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors caused by updates."""
    logger.error("Exception while handling an update:", exc_info=context.error)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    welcome_message = (
        "🌟 Welcome to Free Proxy Bot! 🌟\n\n"
        "📝 Here's how to use the bot:\n\n"
        "1️⃣ Choose your proxy type:\n"
        "   • /http - For regular web browsing\n"
        "   • /socks5 - For advanced applications\n"
        "   • /any - Let the bot choose for you\n\n"
        "2️⃣ Copy the proxy address when received\n"
        "3️⃣ Use it in your browser or application settings\n\n"
        "🔍 Need help setting up?\n"
        "• Most browsers: Settings → Network/Proxy settings\n"
        "• Applications: Check app's connection settings\n\n"
        "⚠️ Remember: Free proxies may be unstable\n"
        "💡 Try /better for reliable premium proxies\n"
        "❓ Type /help to see this message again\n\n"
        "Stay secure! 🔒"
    )

    premium_message = (
        "💎 PREMIUM PROXY OFFER 💎\n\n"
        "🚀 Get reliable, high-speed proxies starting from just $1!\n\n"
        "Why choose premium?\n"
        "✅ 99.9% Uptime\n"
        "✅ Lightning-fast speeds\n"
        "✅ Dedicated support\n"
        "✅ Multiple locations\n"
        "✅ No IP conflicts\n\n"
        "Type /better to get started!"
    )
    
    try:
        # Send and pin the premium message
        premium_msg = await update.message.reply_text(premium_message)
        try:
            await premium_msg.pin(disable_notification=True)
        except TelegramError as e:
            logger.warning(f"Could not pin message: {e}")
        
        # Send the welcome message
        await update.message.reply_text(welcome_message)
    except TelegramError as e:
        logger.error(f"Error sending welcome message: {e}")

def fetch_proxies(url: str) -> list:
    """Fetch proxies from the given URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        # Filter out empty lines and strip whitespace
        proxies = [line.strip() for line in response.text.split('\n') if line.strip()]
        return proxies
    except Exception as e:
        logger.error(f"Error fetching proxies: {e}")
        return []

def format_proxy_message(proxy: str, proxy_type: str) -> str:
    """Format the proxy message with fancy styling."""
    current_time = datetime.now(pytz.UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
    return (
        f"🎯 Here's your {proxy_type} proxy:\n\n"
        f"📍 Address: `{proxy}`\n"
        f"🔒 Type: {proxy_type}\n"
        f"⚡ Status: Ready to use\n"
        f"🕒 Generated: {current_time}\n\n"
        f"⚠️ Note: Free proxies may be unstable or slow.\n"
        f"💡 Get premium proxies starting from $1 with:\n"
        f"   • Guaranteed uptime\n"
        f"   • Ultra-fast speeds\n"
        f"   • 24/7 support\n"
        f"Type /better to learn more! 🚀\n\n"
        f"Stay secure! 🛡️"
    )

async def get_http_proxy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a random HTTP proxy."""
    try:
        proxies = fetch_proxies(HTTP_PROXY_URL)
        if not proxies:
            await update.message.reply_text(
                "❌ Sorry, couldn't fetch HTTP proxies at the moment. Please try again later."
            )
            return
        
        proxy = random.choice(proxies)
        await update.message.reply_text(
            format_proxy_message(proxy, "HTTP"),
            parse_mode='Markdown'
        )
    except TelegramError as e:
        logger.error(f"Telegram error in get_http_proxy: {e}")
        await update.message.reply_text("❌ An error occurred. Please try again later.")

async def get_socks5_proxy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a random SOCKS5 proxy."""
    try:
        proxies = fetch_proxies(SOCKS5_PROXY_URL)
        if not proxies:
            await update.message.reply_text(
                "❌ Sorry, couldn't fetch SOCKS5 proxies at the moment. Please try again later."
            )
            return
        
        proxy = random.choice(proxies)
        await update.message.reply_text(
            format_proxy_message(proxy, "SOCKS5"),
            parse_mode='Markdown'
        )
    except TelegramError as e:
        logger.error(f"Telegram error in get_socks5_proxy: {e}")
        await update.message.reply_text("❌ An error occurred. Please try again later.")

async def get_any_proxy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a random proxy of any type."""
    try:
        http_proxies = fetch_proxies(HTTP_PROXY_URL)
        socks5_proxies = fetch_proxies(SOCKS5_PROXY_URL)
        
        all_proxies = []
        if http_proxies:
            all_proxies.extend([(proxy, "HTTP") for proxy in http_proxies])
        if socks5_proxies:
            all_proxies.extend([(proxy, "SOCKS5") for proxy in socks5_proxies])
        
        if not all_proxies:
            await update.message.reply_text(
                "❌ Sorry, couldn't fetch any proxies at the moment. Please try again later."
            )
            return
        
        proxy, proxy_type = random.choice(all_proxies)
        await update.message.reply_text(
            format_proxy_message(proxy, proxy_type),
            parse_mode='Markdown'
        )
    except TelegramError as e:
        logger.error(f"Telegram error in get_any_proxy: {e}")
        await update.message.reply_text("❌ An error occurred. Please try again later.")

async def get_better_proxy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Promote premium proxy services."""
    affiliate_url = os.getenv("PROXY_AFFILIATE_URL")
    if not affiliate_url:
        await update.message.reply_text(
            "🔒 Premium proxy service is currently unavailable. Please try again later."
        )
        return

    message = (
        "🚀 Want Better, Faster, More Reliable Proxies?\n\n"
        "Our premium proxy service offers:\n"
        "✨ 99.9% Uptime\n"
        "✨ Ultra-Fast Speeds\n"
        "✨ Secure & Anonymous\n"
        "✨ 24/7 Support\n"
        "✨ Multiple Locations\n"
        "✨ Dedicated IPs\n\n"
        "Click below to get started! 👇"
    )

    keyboard = [[InlineKeyboardButton("🔥 Get Premium Proxies 🔥", url=affiliate_url)]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        await update.message.reply_text(
            message,
            reply_markup=reply_markup
        )
    except TelegramError as e:
        logger.error(f"Telegram error in get_better_proxy: {e}")
        await update.message.reply_text("❌ An error occurred. Please try again later.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a help message when the command /help is issued."""
    await start(update, context)

def main() -> None:
    """Start the bot."""
    try:
        # Create the Application with rate limiting
        application = (
            Application.builder()
            .token(os.getenv("TELEGRAM_BOT_TOKEN"))
            .build()
        )

        # Add command handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("http", get_http_proxy))
        application.add_handler(CommandHandler("socks5", get_socks5_proxy))
        application.add_handler(CommandHandler("any", get_any_proxy))
        application.add_handler(CommandHandler("better", get_better_proxy))

        # Add error handler
        application.add_error_handler(error_handler)

        # Start the bot
        logger.info("Bot started successfully!")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        raise

if __name__ == "__main__":
    main() 