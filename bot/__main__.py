"""Kirish nuqtasi — botni ishga tushiradi (long-polling)."""
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import BOT_TOKEN
from bot.database.connection import Database
from bot.database.repositories import AdminRepo, ChannelRepo, ElonRepo, PostRepo, UserRepo
from bot.middlewares.album import AlbumMiddleware
from bot.middlewares.subscription import SubscriptionMiddleware
from bot.middlewares.throttling import ThrottlingMiddleware


def setup_dispatcher(db: Database) -> Dispatcher:
    dp = Dispatcher(storage=MemoryStorage())

    # Repository'lar -> workflow data (DI). Handler/filtrlarga nom bo'yicha beriladi.
    dp["users"] = UserRepo(db)
    dp["admins"] = AdminRepo(db)
    dp["channels"] = ChannelRepo(db)
    dp["posts"] = PostRepo(db)
    dp["elons"] = ElonRepo(db)

    # Middleware'lar
    dp.update.outer_middleware(SubscriptionMiddleware())
    dp.message.outer_middleware(AlbumMiddleware())      # albomni filtrlashdan oldin yig'adi
    dp.message.middleware(ThrottlingMiddleware())

    # Router'lar (Faza 3+ da ulanadi)
    from bot.handlers import setup_routers
    dp.include_router(setup_routers())

    return dp


async def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

    db = Database()
    await db.connect()

    bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = setup_dispatcher(db)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await db.close()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
