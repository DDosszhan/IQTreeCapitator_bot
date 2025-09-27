import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application

from .admin import get_admin_handlers
from .user import get_user_handlers


def main() -> None:
    load_dotenv()
    token = os.getenv("BOT_TOKEN")
    application = Application.builder().token(token).build()

    for handler in (*get_user_handlers(), *get_admin_handlers()):
        application.add_handler(handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
