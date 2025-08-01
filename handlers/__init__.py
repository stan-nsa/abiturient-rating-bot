from aiogram import Router

from .commands import router as commands_router
from .parse import router as parse_router


router = Router(name=__name__)
# Роутер только для лички (фильтры для всех подключенных роутеров!!!) - уже прописаны в create_bot.py
# router.message.filter(F.chat.type == 'private')
# router.callback_query.filter(F.message.chat.type == 'private')


router.include_router(commands_router)
router.include_router(parse_router)
