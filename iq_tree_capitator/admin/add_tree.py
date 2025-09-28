from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from sqlmodel import Session
from ._common import IsAdmin
from ..database import engine, Tree
from iq_tree_capitator import utils


class AddTreeState(StatesGroup):
    photo = State()
    lon = State()
    lan = State()
    height = State()
    owner = State()


router = Router()


@router.message(Command("add_tree"), IsAdmin())
async def add_tree(message: Message, state: FSMContext) -> None:
    await message.answer("Send a photo of the tree:")
    await state.set_state(AddTreeState.photo)


@router.message(AddTreeState.photo)
async def ask_photo(message: Message, state: FSMContext) -> None:
    if not message.photo:
        await utils.fsm_err(
            message, state, AddTreeState.photo, "Please provide a photo."
        )
        return

    photo = message.photo[-1]
    filename = await utils.download_photo(photo)
    await state.update_data(photo=filename)
    await message.answer("Enter tree longitude:")
    await state.set_state(AddTreeState.lon)


@router.message(AddTreeState.lon)
async def ask_lon(message: Message, state: FSMContext) -> None:
    async def err():
        await utils.fsm_err(
            message,
            state,
            AddTreeState.lon,
            "❌ Invalid longitude. Enter a float number:",
        )

    if not message.text:
        await err()
        return

    try:
        lon = float(message.text)
        await state.update_data(lon=lon)
        await message.answer("Enter tree latitude:")
        await state.set_state(AddTreeState.lan)
    except ValueError:
        await err()


@router.message(AddTreeState.lan)
async def ask_lan(message: Message, state: FSMContext) -> None:
    async def err():
        await utils.fsm_err(
            message,
            state,
            AddTreeState.lon,
            "❌ Invalid latitude. Enter a float number:",
        )

    if not message.text:
        await err()
        return

    try:
        lan = float(message.text)
        await state.update_data(lan=lan)
        await message.answer("Enter tree height:")
        await state.set_state(AddTreeState.height)
    except ValueError:
        await err()


@router.message(AddTreeState.height)
async def ask_height(message: Message, state: FSMContext) -> None:
    async def err():
        await utils.fsm_err(
            message,
            state,
            AddTreeState.lon,
            "❌ Invalid latitude. Enter a float number:",
        )

    if not message.text:
        await err()
        return

    try:
        height = int(message.text)
        await state.update_data(height=height)
        await message.answer("Enter tree owner:")
        await state.set_state(AddTreeState.owner)
    except ValueError:
        await err()


@router.message(AddTreeState.owner)
async def ask_owner(message: Message, state: FSMContext) -> None:
    owner = message.text

    data = await state.get_data()
    photo = data.get("photo", None)
    lon = data.get("lon", None)
    lan = data.get("lan", None)
    height = data.get("height", None)

    if not photo or not lon or not lan or not height or not owner:
        message.answer("Not enough data provided.")
        await state.clear()
        return

    with Session(engine) as session:
        item = Tree(photo=photo, lon=lon, lan=lan, height=height, owner=owner)
        session.add(item)
        session.commit()

    await message.answer("✅ Item added")
    await state.clear()


@router.message(Command("cancel"), IsAdmin())
async def cancel_fsm(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("❌ Nothing to cancel — you are not in any process.")
        return

    await state.clear()
    await message.answer("✅ Process cancelled. You can start again anytime.")
