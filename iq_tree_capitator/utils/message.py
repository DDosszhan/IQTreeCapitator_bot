from telegram import Update


async def reply_text_if_msg(update: Update, text: str) -> None:
    if update.message:
        await reply_text_if_msg(update, text)
