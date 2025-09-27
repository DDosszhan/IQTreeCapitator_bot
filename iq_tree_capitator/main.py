import asyncio
from iq_tree_capitator.create_bot import dp, bot
from iq_tree_capitator.user import get_tree, help
from iq_tree_capitator.admin import add_tree


async def main() -> None:
    dp.include_router(get_tree.router)
    dp.include_router(help.router)
    dp.include_router(add_tree.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
