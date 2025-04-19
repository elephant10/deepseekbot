import os
from dotenv import load_dotenv 
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode
from telegram.helpers import escape_markdown
from telegram.error import BadRequest, TelegramError, NetworkError
import deepseek_bot
import telegramify_markdown
# Load environment variables
load_dotenv()
API_TOKEN = os.environ.get("tg_bot_key")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text(r'Hello\! *I am* your Telegram deepseek bot\. How can I help you today\?', parse_mode=ParseMode.MARKDOWN_V2)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text('Processing your request...')
    #to fix this!!!!!!!!
    deepseek_for_user = create_ai(update.effective_user)

    #doesn't work:
    #safe_text = escape_markdown(answer, version=2)
    while True:
        try:
            answer = deepseek_for_user.chat(update.message.text)
            escaped_answer = telegramify_markdown.markdownify(answer)
            print(f"answer: {answer}")
            await update.message.reply_text(escaped_answer, parse_mode=ParseMode.MARKDOWN_V2)
            break
        except BadRequest as e:
            await update.message.reply_text(e)
            print(f"Error sending message: {e}")
            break
        except NetworkError as e:
            await update.message.reply_text("error. wait...")
            print(f"Network error: {e}")
            
                                   
def get_user_key(user) -> str:
    #expand logic
    return os.environ.get("deepseek_key")

def create_ai(user) -> None:
    """Create an AI instance."""
    ai_instance = deepseek_bot.Deepseek(get_user_key(user))
    return ai_instance
    

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