from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.enums import ChatAction

from help import help_text
import config
from keyboards import get_kb_parse, get_kb_back
from university import guap_get_data


router = Router(name=__name__)
# Роутер только для лички (фильтры уже прописаны в /handlers/__init__.py)
# router.message.filter(F.chat.type == 'private')
# router.callback_query.filter(F.chat.type == 'private')


# == Обработчик команды /start ====================================================================
@router.message(CommandStart(ignore_case=True))
@router.message(Command(commands='help', ignore_case=True))
async def handler_command_start(message: types.Message):
    await message.answer(text=help_text)
    await message.delete()
# =================================================================================================


# == Обработчик команды /parse ====================================================================
@router.message(Command(commands='parse', ignore_case=True))
async def handler_command_parse(message: types.Message):
    await message.delete()

    kb = get_kb_parse(universities=config.universities)
    kb.attach(get_kb_back(callback_data="Back"))

    await message.answer(
        text="Университеты:",
        reply_markup=kb.as_markup()
    )

# =================================================================================================
