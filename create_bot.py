from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, or_f, and_f
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.types import BotCommandScopeDefault, BotCommandScopeAllPrivateChats
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import router as handlers_router
from handlers.commands.commands_menu import commands_menu

from config import config


dp = Dispatcher(storage=MemoryStorage())


async def on_startup():
    print('Start NSA Worker Bot')


async def on_shutdown():
    print('Stop NSA Worker Bot')


async def init_bot():
    dp.include_router(handlers_router)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    bot = Bot(token=config.bot.token,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # Удаляем меню команд в групповых чатах
    await bot.delete_my_commands(scope=BotCommandScopeDefault())

    # Прописываем меню команд для приватного чата с ботом
    await bot.set_my_commands(commands=commands_menu, scope=BotCommandScopeAllPrivateChats())

    # Удаляем неполученные/необработанные обновления/сообщения
    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
