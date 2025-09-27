from telegram.ext import CommandHandler, MessageHandler, filters, ConversationHandler
from telegram import Update
from telegram.ext import CallbackContext
from sqlmodel import Session
from ._common import admin_required
from ..database import engine, Tree
from ..utils import reply_text_if_msg

S_ASK_LON, S_ASK_LAN, S_ASK_HEIGHT, S_ASK_OWNER = range(4)


@admin_required
async def _start_add_tree(update: Update, context: CallbackContext) -> int:
    await reply_text_if_msg(update, "Enter tree longitude:")
    return S_ASK_LON


async def _ask_lon(update: Update, context: CallbackContext) -> int:
    try:
        context.user_data["new_tree_lon"] = float(update.message.text)  # type: ignore
        await reply_text_if_msg(update, "Enter tree latitude:")
        return S_ASK_LAN
    except ValueError:
        await reply_text_if_msg(update, "❌ Invalid longitude. Enter a float number:")
        return S_ASK_LON


async def _ask_lan(update: Update, context: CallbackContext) -> int:
    try:
        context.user_data["new_tree_lan"] = float(update.message.text)  # type: ignore
        await reply_text_if_msg(update, "Enter tree height:")
        return S_ASK_HEIGHT
    except ValueError:
        await reply_text_if_msg(update, "❌ Invalid latitude. Enter a float number:")
        return S_ASK_LAN


async def _ask_height(update: Update, context: CallbackContext) -> int:
    try:
        context.user_data["new_tree_height"] = int(update.message.text)  # type: ignore
        await reply_text_if_msg(update, "Enter tree owner:")
        return S_ASK_OWNER
    except ValueError:
        await reply_text_if_msg(update, "❌ Invalid height. Enter a number:")
        return S_ASK_HEIGHT


async def _ask_owner(update: Update, context: CallbackContext) -> int:
    if not update.message or not context.user_data:
        return ConversationHandler.END

    owner = update.message.text

    lon = context.user_data.get("new_tree_lon", None)
    lan = context.user_data.get("new_tree_lan", None)
    height = context.user_data.get("new_tree_height", None)

    if not lon or not lan or not height or not owner:
        return ConversationHandler.END

    with Session(engine) as session:
        item = Tree(lon=lon, lan=lan, height=height, owner=owner)
        session.add(item)
        session.commit()

    await reply_text_if_msg(update, "✅ Item added")
    return ConversationHandler.END


async def _cancel(update: Update, context: CallbackContext) -> int:
    await reply_text_if_msg(update, "🚫 Canceled.")
    return ConversationHandler.END


def get_add_tree_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[CommandHandler("add_tree", _start_add_tree)],
        states={
            S_ASK_LON: [MessageHandler(filters.TEXT & ~filters.COMMAND, _ask_lon)],
            S_ASK_LAN: [MessageHandler(filters.TEXT & ~filters.COMMAND, _ask_lan)],
            S_ASK_HEIGHT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, _ask_height)
            ],
            S_ASK_OWNER: [MessageHandler(filters.TEXT & ~filters.COMMAND, _ask_owner)],
        },
        fallbacks=[CommandHandler("cancel", _cancel)],
    )
