import os
from functools import wraps
from telegram.ext import ConversationHandler
from telegram import Update
from telegram.ext import CallbackContext
from functools import lru_cache
from ..utils import reply_text_if_msg


@lru_cache
def get_admin_ids() -> list[int]:
    env_var = os.getenv("ADMIN_IDS")
    if not env_var:
        return []
    return list(map(int, env_var.split(",")))


def admin_required(handler):
    @wraps(handler)
    async def wrapper(update: Update, context: CallbackContext):
        if not update.effective_user:
            return

        if update.effective_user.id not in get_admin_ids():
            await reply_text_if_msg(
                update, "🚫 You are not allowed to use this command."
            )
            return ConversationHandler.END
        return await handler(update, context)

    return wrapper
