"""Router aggregatori. TARTIB muhim: echo (menu) eng oxirida.

errors.router root sifatida ishlatiladi — xatolik bolalardan yuqoriga shu yergacha
ko'tariladi, shu sabab uning @router.errors handlerlari hammasini ushlaydi.
"""
from aiogram import Router

from bot.handlers import errors, start
from bot.handlers.admin import broadcast, manage
from bot.handlers.user import books, download, groups, info, menu, software


def setup_routers() -> Router:
    root: Router = errors.router

    root.include_router(start.router)
    root.include_router(info.router)
    root.include_router(download.router)
    root.include_router(manage.router)      # admin menejer
    root.include_router(broadcast.router)   # post yaratish/tarqatish
    root.include_router(books.router)       # catalog: maktab/booknomy
    root.include_router(software.router)    # catalog: PC dasturlar
    root.include_router(groups.router)
    root.include_router(menu.router)        # echo fallback — OXIRGI

    return root
