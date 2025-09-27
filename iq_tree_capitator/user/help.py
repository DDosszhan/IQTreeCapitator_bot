from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("help"))
async def help_command(message: Message) -> None:
    await message.answer(
        "Отправьте /start <id> или просто /start и следуйте инструкциям."
    )
