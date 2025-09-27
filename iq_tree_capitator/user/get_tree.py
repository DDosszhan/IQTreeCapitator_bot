import uuid
from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
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


@router.message(Command("start"))
async def start(message: Message, command: CommandObject, state: FSMContext) -> None:
    args = command.args
    if args:
        tree_id = args.split(" ")[0]
        await message.answer(get_tree_msg(tree_id))
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

    await message.answer(get_tree_msg(message.text.strip()))
    await state.clear()
