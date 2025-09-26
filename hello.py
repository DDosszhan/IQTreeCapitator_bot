import logging
import os
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

ASK_ID = range(1)

# "Фейковая база" — только один id
FAKE_TREE_ID = "abcd-1234-efgh-5678"
FAKE_TREE = {
    "id": FAKE_TREE_ID,
    "longitude": 30.1,
    "latitude": 59.9,
    "height": 5.5
}

def get_tree_by_id(tree_id):
    if tree_id == FAKE_TREE_ID:
        return FAKE_TREE
    return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    args = context.args
    if args:
        tree_id = args[0]
        tree = get_tree_by_id(tree_id)
        if tree:
            await update.message.reply_text(
                f"Дерево найдено:\nID: {tree['id']}\nДолгота: {tree['longitude']}\nШирота: {tree['latitude']}\nВысота: {tree['height']}"
            )
        else:
            await update.message.reply_text("ID не найдено.")
        return ConversationHandler.END
    else:
        await update.message.reply_text("Пожалуйста, введите ID дерева:")
        return ASK_ID

async def ask_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    tree_id = update.message.text.strip()
    tree = get_tree_by_id(tree_id)
    if tree:
        await update.message.reply_text(
            f"Дерево найдено:\nID: {tree['id']}\nДолгота: {tree['longitude']}\nШирота: {tree['latitude']}\nВысота: {tree['height']}"
        )
    else:
        await update.message.reply_text("ID не найдено.")
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