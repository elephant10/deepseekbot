import os
from dotenv import load_dotenv 
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Load environment variables
load_dotenv()
API_TOKEN = os.environ.get("tg_bot_key")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text('Hello! I am your Telegram bot. How can I help you today?')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

def main() -> None:
    """Start the bot."""
    # Create Application instance
    application = Application.builder().token(API_TOKEN).build()

    # Register handlers directly on the application
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Start polling
    application.run_polling()

if __name__ == '__main__':
    main()