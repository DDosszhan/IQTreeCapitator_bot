from telegram.ext import CommandHandler, MessageHandler, filters, ConversationHandler
from telegram import Update
from telegram.ext import CallbackContext
from sqlmodel import Session
from ._common import admin_required
from ..database import engine, Tree

S_ASK_LON, S_ASK_LAN, S_ASK_HEIGHT, S_ASK_OWNER = range(4)


@admin_required
async def _start_add_tree(update: Update, context: CallbackContext):
    await update.message.reply_text("Enter tree longitude:")
    return S_ASK_LON


async def _ask_lon(update: Update, context: CallbackContext):
    try:
        context.user_data["new_tree_lon"] = float(update.message.text)
        await update.message.reply_text("Enter tree latitude:")
        return S_ASK_LAN
    except ValueError:
        await update.message.reply_text("❌ Invalid longitude. Enter a float number:")
        return S_ASK_LON


async def _ask_lan(update: Update, context: CallbackContext):
    try:
        context.user_data["new_tree_lan"] = float(update.message.text)
        await update.message.reply_text("Enter tree height:")
        return S_ASK_HEIGHT
    except ValueError:
        await update.message.reply_text("❌ Invalid latitude. Enter a float number:")
        return S_ASK_LAN


async def _ask_height(update: Update, context: CallbackContext):
    try:
        context.user_data["new_tree_height"] = int(update.message.text)
        await update.message.reply_text("Enter tree owner:")
        return S_ASK_OWNER
    except ValueError:
        await update.message.reply_text("❌ Invalid height. Enter a number:")
        return S_ASK_HEIGHT


async def _ask_owner(update: Update, context: CallbackContext):
    owner = update.message.text

    lon = context.user_data["new_tree_lon"]
    lan = context.user_data["new_tree_lan"]
    height = context.user_data["new_tree_height"]

    with Session(engine) as session:
        item = Tree(lon=lon, lan=lan, height=height, owner=owner)
        session.add(item)
        session.commit()

    await update.message.reply_text("✅ Item added")
    return ConversationHandler.END


async def _cancel(update: Update, context: CallbackContext):
    await update.message.reply_text("🚫 Canceled.")
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
