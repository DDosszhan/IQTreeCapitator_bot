import os
import logging
from dotenv import load_dotenv
from database import Tree, session
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler
from sqlmodel import select

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

ASK_ID = range(1)

def get_tree_msg(tree_id: str) -> str:
    statement = select(Tree).where(Tree.tree_id == tree_id)
    results = session.exec(statement)

    for tree in results:
        return f"Дерево найдено:\nID: {tree.tree_id}\nДолгота: {tree.lon}\nШирота: {tree.lan}\nВысота: {tree.height}"

    return "ID не найдено."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    args = context.args
    if args:
        tree_id = args[0]
        await update.message.reply_text(get_tree_msg(tree_id))
        return ConversationHandler.END
    else:
        await update.message.reply_text("Пожалуйста, введите ID дерева:")
        return ASK_ID

async def ask_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    tree_id = update.message.text.strip()
    await update.message.reply_text(get_tree_msg(tree_id))
    return ConversationHandler.END

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Отправьте /start <id> или просто /start и следуйте инструкциям.")

def main() -> None:
    token = os.getenv("BOT_TOKEN")
    application = Application.builder().token(token).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_id)],
        },
        fallbacks=[],
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("help", help_command))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
