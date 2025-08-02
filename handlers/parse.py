from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.enums import ChatAction

from university import guap_get_data
import config
from keyboards import (
    # CallbackData:
    UniversityCbData, SpecialityCbData, ParseCbData,
    # Keyboards:
    get_kb_speciality,
    get_kb_university,
    get_kb_back,
    get_kb_parse,
)

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

    if university_id == "_ALL_":
        text = "Университеты:"

        kb = get_kb_parse(universities=config.universities)
        kb.attach(get_kb_back(callback_data="Back"))
    else:
        university = config.universities.get(university_id)
        text = university.name

        kb = get_kb_university(university=university)
        kb.attach(get_kb_back(callback_data=UniversityCbData(id='_ALL_')))

    await callback.message.edit_text(
        text=text,
        reply_markup=kb.as_markup()
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
    university = config.universities.get(university_id)
    speciality = university.specialties.get(speciality_id)
    text = f"{university.name}:\n"\
           f"{speciality.name}"

    kb = get_kb_speciality(speciality=speciality, university=university)
    kb.attach(get_kb_back(callback_data=UniversityCbData(id=university_id)))
    await callback.message.edit_text(
        text=text,
        reply_markup=kb.as_markup()
    )
    await callback.answer()
# =================================================================================================


# == Обработчик команды parse ====================================================================
@router.callback_query(
    ParseCbData.filter()
)
async def handler_parse(callback: types.CallbackQuery, callback_data: ParseCbData):
    university_id = callback_data.university_id
    university = config.universities.get(university_id)

    speciality_id = callback_data.id
    if speciality_id == '_ALL_': # Вывод всех специальностей
        specialties = university.specialties.values()
    else:
        specialties = [university.specialties.get(speciality_id)]

    for speciality in specialties:
        await callback.message.bot.send_chat_action(
            chat_id=callback.message.chat.id,
            action=ChatAction.UPLOAD_DOCUMENT
        )

        file_path = guap_get_data(
            speciality=speciality,
            rank_minimum=config.config.rank.points_minimum
        )

        await callback.message.answer_document(
            document=types.FSInputFile(path=file_path),
            caption=speciality.name
        )

    kb = get_kb_back(callback_data=UniversityCbData(id=university_id))
    await callback.message.answer(
        text='CSV-файлы выгружены!',
        reply_markup=kb.as_markup()
    )
    # await callback.answer()
# =================================================================================================
