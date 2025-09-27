import os
from dotenv import load_dotenv
from aiogram import Dispatcher, Bot

load_dotenv()

token = os.getenv("BOT_TOKEN")
admins = [int(i) for i in os.getenv("ADMINS", "").split(",") if i]

if not token:
    print("BOT_TOKEN is unset! Exiting...")
    exit(1)

bot = Bot(token=token)
dp = Dispatcher()
