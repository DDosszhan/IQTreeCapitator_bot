from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from sqlmodel import Session, select
from ._common import IsAdmin
from ..database import engine, Tree
from iq_tree_capitator import utils

router = Router()

TREE_TEMPLATE = """
{uuid}
=====================
photo: {photo}
lan: {lan}
lon: {lon}
owner: {owner}
height: {height}
"""


@router.message(Command("list_trees"), IsAdmin())
async def list_trees(message: Message) -> None:
    with Session(engine) as session:
        trees = session.exec(select(Tree)).all()
        text = ""
        for i in trees:
            text += TREE_TEMPLATE.format(
                uuid=i.id,
                photo=i.photo,
                lan=i.lan,
                lon=i.lon,
                owner=i.owner,
                height=i.height,
            )

        await message.reply(text)
