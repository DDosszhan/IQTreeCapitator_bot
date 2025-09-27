from aiogram.fsm.storage.base import StateType
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


async def fsm_err(
    message: Message, state: FSMContext, current_state: StateType, error_msg: str
) -> None:
    await message.answer(error_msg)
    await state.set_state(current_state)
