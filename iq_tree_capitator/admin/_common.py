import os
from typing import Optional
from functools import wraps
from telegram.ext import  ConversationHandler
from telegram import Update
from telegram.ext import CallbackContext
from functools import lru_cache

@lru_cache
def get_admin_ids() -> list[int]:
    return list(map(int, os.getenv("ADMIN_IDS").split(",")))

def admin_required(handler):
    @wraps(handler)
    async def wrapper(update: Update, context: CallbackContext):
        if update.effective_user.id not in get_admin_ids():
            await update.message.reply_text("🚫 You are not allowed to use this command.")
            return ConversationHandler.END
        return await handler(update, context)
    return wrapper
