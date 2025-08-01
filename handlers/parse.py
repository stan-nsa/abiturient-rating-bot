from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.enums import ChatAction

from university import guap_get_data
import config
from keyboards import UniversityCbData, SpecialityCbData, ParseCbData, get_kb_speciality, get_kb_university

router = Router(name=__name__)
# Роутер только для лички (фильтры уже прописаны в /handlers/__init__.py)
# router.message.filter(F.chat.type == 'private')
# router.callback_query.filter(F.chat.type == 'private')


# == Обработчик команды university ====================================================================
@router.callback_query(
    UniversityCbData.filter()
)
async def handler_university(callback: types.CallbackQuery, callback_data: UniversityCbData):
    university_id = callback_data.id
    university = config.univers.get(university_id)
    text = university.name
    await callback.message.edit_text(
        text=text,
        reply_markup=get_kb_university(university=university).as_markup()
    )
    await callback.answer()
# =================================================================================================


# == Обработчик команды speciality ====================================================================
@router.callback_query(
    SpecialityCbData.filter()
)
async def handler_speciality(callback: types.CallbackQuery, callback_data: SpecialityCbData):
    speciality_id = callback_data.id
    university_id = callback_data.university_id
    university = config.univers.get(university_id)
    speciality = university.specialties.get(speciality_id)
    text = f"{university.name}:\n"\
            f"{speciality.name}"
    await callback.message.edit_text(
        text=text,
        reply_markup=get_kb_speciality(speciality=speciality, university=university).as_markup()
    )
    await callback.answer()
# =================================================================================================


# == Обработчик команды parse ====================================================================
@router.callback_query(
    ParseCbData.filter()
)
async def handler_parse(callback: types.CallbackQuery, callback_data: ParseCbData):
    speciality_id = callback_data.id
    university_id = callback_data.university_id
    university = config.univers.get(university_id)
    speciality = university.specialties.get(speciality_id)
    text = f"Получение CSV-файла для:\n"\
            f"{speciality.name}"
    await callback.message.edit_text(
        text=text,
        # reply_markup=get_kb_speciality(speciality=speciality).as_markup()
    )
    await callback.answer()
# =================================================================================================


# == Обработчик команды /parse ====================================================================
@router.message(Command(commands='parse_all', ignore_case=True))
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
