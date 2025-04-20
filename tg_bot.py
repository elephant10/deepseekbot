import os
from dotenv import load_dotenv 
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode
from telegram.helpers import escape_markdown
from telegram.error import BadRequest, TelegramError, NetworkError
import deepseek_bot
import telegramify_markdown
import signal
import asyncio
import sys
# Load environment variables
load_dotenv()
API_TOKEN = os.environ.get("tg_bot_key")
from user import User, Message

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    User(update.message.from_user.id, update.message.from_user.username)
    await update.message.reply_text('Hello! I am your Telegram deepseek bot. How can I help you today?')
    print(f"User {update.message.from_user.username} started the bot.")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """tell user bot is working on it."""
    await update.message.reply_text('Processing your request...')
    
    #to fix this!!!!!!!!
    deepseek_for_user = create_ai(update.effective_user)
    user = User.get_user_by_id(update.message.from_user.id, update.message.from_user.username)
    print(f"User {user.get_tag()} sent a message with {len(update.message.text)} characters.")
    user.add_message(Message(id= update.message.message_id,
                             text=update.message.text,
                             is_from_bot=False,chat=update.message.chat.id,
                             date=update.message.date.strftime("%Y-%m-%d %H:%M:%S")))
    while True:
        try:
            response_from_model_object = deepseek_for_user.chat(user.get_conversation(), model=user.get_model())
            answer = response_from_model_object.content
            escaped_answer = telegramify_markdown.markdownify(answer)
            if user.get_model() == "deepseek-reasoner":
                await update.message.reply_text("thought: \n" + \
                                                 telegramify_markdown.markdownify(response_from_model_object.reasoning_content),
                                                 parse_mode=ParseMode.MARKDOWN_V2)
            answer_message = await update.message.reply_text(escaped_answer, parse_mode=ParseMode.MARKDOWN_V2)
            print(f"user {user} got response")
            user.add_message(Message(id= answer_message.message_id,
                             text=answer_message.text,
                             is_from_bot=True,chat=update.message.chat.id,
                             date=answer_message.date.strftime("%Y-%m-%d %H:%M:%S")))
           
            break
        except BadRequest as e:
            await update.message.reply_text(e)
            print(f"Error sending message: {e}")
            break
        except NetworkError as e:
            await update.message.reply_text("error. wait...")
            print(f"Network error: {e}")
            

async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if (str(update.message.from_user.id) not in os.environ.get("admins").split(",")):
        print(f"User {update.message.from_user.username} tried ending the bot.")
        return
    await update.message.reply_text('bot stops working.')
    
    context.application.stop_running()
    print("Stopping the bot...")

    User.save_userlist()
    print("User list saved.")


async def clean_history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
   
    User.get_user_by_id(update.message.from_user.id, 
                        update.message.from_user.username).delete_conversation()
    print(f"User {update.message.from_user.username} deleted their conversation history.")
    await update.message.reply_text('The North remembers...')
    

async def start_think(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = User.get_user_by_id(update.message.from_user.id, update.message.from_user.username)
    user.set_model("deepseek-reasoner")
    print(f"User {user} turned thinking.")
    await update.message.reply_text('I am ...')

                           
async def stop_think(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = User.get_user_by_id(update.message.from_user.id, update.message.from_user.username)
    user.set_model("deepseek-chat")
    print(f"User {user} turned off thinking.")
    await update.message.reply_text("Sho, Umniy?")
                                   

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
    application.add_handler(CommandHandler("end", end))  # Add this line
    application.add_handler(CommandHandler("forget", clean_history))  # Add this line
    application.add_handler(CommandHandler("start_think", start_think))  # Add this line
    application.add_handler(CommandHandler("stop_think", stop_think))  # Add this line

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    
    print("Bot starts")
    User.load_userlist()
    print(f"User list loaded. {len(User.get_userlist())} users found.")
    application.run_polling()


if __name__ == '__main__':
    main()