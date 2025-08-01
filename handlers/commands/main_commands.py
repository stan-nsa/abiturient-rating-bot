from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.enums import ParseMode, ChatAction

from help import help_text
import config
from keyboards import get_kb_parse
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
@router.message(Command(commands='parse2', ignore_case=True))
async def handler_command_parse(message: types.Message):
    await message.delete()

    await message.answer(
        text='Университеты:',
        reply_markup=get_kb_parse(univers=config.univers).as_markup()
    )

# =================================================================================================


# == Обработчик команды /parse ====================================================================
@router.message(Command(commands='parse', ignore_case=True))
async def handler_command_parse(message: types.Message):
    await message.delete()

    for spec in config.univers['guap'].specialties.values():
        await message.bot.send_chat_action(
            chat_id=message.chat.id,
            action=ChatAction.UPLOAD_DOCUMENT
        )

        file_path = guap_get_data(
            speciality=spec,
            rank_minimum=config.config.rank.points_minimum
        )

        await message.answer_document(
            document=types.FSInputFile(path=file_path),
            caption=spec.name
        )

    await message.answer(
        text='CSV-файлы выгружены!'
    )

# =================================================================================================
