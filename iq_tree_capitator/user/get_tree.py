import uuid
from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from iq_tree_capitator import utils
from sqlmodel import select, Session

from iq_tree_capitator.database import engine, Tree

ASK_ID = 1
MESSAGE_TEMPLATE = """
Дерево найдено:
ID: {id}
Долгота: {lon}
Широта: {lan}
Высота: {height}
Владелец: {owner}
"""


class AskId(StatesGroup):
    tree_id = State()


router = Router()


async def send_tree_data(message: Message, tree_id: str) -> None:
    try:
        tree_uuid = uuid.UUID(tree_id)
    except ValueError:
        await message.reply("Неправильный формат ID!")
        return

    with Session(engine) as session:
        statement = select(Tree).where(Tree.id == tree_uuid)
        tree = session.exec(statement).first()

        if tree:
            input_file = FSInputFile(tree.photo)
            await message.reply_photo(
                photo=input_file,
                caption=MESSAGE_TEMPLATE.format(
                    id=tree.id,
                    lon=tree.lon,
                    lan=tree.lan,
                    height=tree.height,
                    owner=tree.owner,
                ),
            )
        else:
            await message.reply("ID не найдено.")


@router.message(Command("start"))
async def start(message: Message, command: CommandObject, state: FSMContext) -> None:
    args = command.args
    if args:
        tree_id = args.split(" ")[0]
        await send_tree_data(message, tree_id)
    else:
        await message.answer("Пожалуйста, введите ID дерева:")
        await state.set_state(AskId.tree_id)


@router.message(AskId.tree_id)
async def ask_id(message: Message, state: FSMContext) -> None:
    if not message.text:
        await state.clear()

    if not message.text:
        await utils.fsm_err(message, state, AskId.tree_id, "ID должен быть текстом!")
        return

    await send_tree_data(message, message.text.strip())
    await state.clear()
