from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Отправьте /start <id> или просто /start и следуйте инструкциям.")

def get_help_handler():
    return CommandHandler("help", help_command)
