import uuid
from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    ConversationHandler,
)
from sqlmodel import select, Session
from ..database import engine, Tree
from ..utils import reply_text_if_msg

ASK_ID = 1
MESSAGE_TEMPLATE = """
Дерево найдено:
ID: {id}
Долгота: {lon}
Широта: {lan}
Высота: {height}
Владелец: {owner}
"""


def get_tree_msg(tree_id: str) -> str:
    try:
        tree_uuid = uuid.UUID(tree_id)
    except ValueError:
        return "Неправильный формат ID!"

    with Session(engine) as session:
        statement = select(Tree).where(Tree.id == tree_uuid)
        tree = session.exec(statement).first()

        if tree:
            return MESSAGE_TEMPLATE.format(
                id=tree.id,
                lon=tree.lon,
                lan=tree.lan,
                height=tree.height,
                owner=tree.owner,
            )
        else:
            return "ID не найдено."


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    args = context.args
    if args:
        tree_id = args[0]
        await reply_text_if_msg(update, get_tree_msg(tree_id))
        return ConversationHandler.END
    else:
        await reply_text_if_msg(update, "Пожалуйста, введите ID дерева:")
        return ASK_ID


async def ask_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message and update.message.text:
        tree_id = update.message.text.strip()
        await reply_text_if_msg(update, get_tree_msg(tree_id))
    return ConversationHandler.END


def get_tree_handler():
    return ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_id)],
        },
        fallbacks=[],
    )
