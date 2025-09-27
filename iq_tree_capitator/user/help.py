from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from ..utils import reply_text_if_msg


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await reply_text_if_msg(
        update, "Отправьте /start <id> или просто /start и следуйте инструкциям."
    )


def get_help_handler():
    return CommandHandler("help", help_command)
