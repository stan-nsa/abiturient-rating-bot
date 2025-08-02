from enum import Enum

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from university import University, Speciality


class UniversityCbData(CallbackData, prefix='university'):
    id: str


class SpecialityCbData(CallbackData, prefix='speciality'):
    id: str
    university_id: str


class ParseCbData(SpecialityCbData, prefix='parse'):
    pass


# Клавиатура для команды parse
def get_kb_parse(universities: dict[University]):
    kb = InlineKeyboardBuilder()
    for university in universities.values():
        kb.button(
            text=university.name,
            callback_data=UniversityCbData(id=university.id).pack()
        )
    return kb.adjust(1)


# Клавиатура для команды university
def get_kb_university(university: University):
    kb = InlineKeyboardBuilder()
    for speciality in university.specialties.values():
        kb.button(
            text=speciality.name,
            callback_data=SpecialityCbData(id=speciality.id, university_id=university.id)
        )
    kb.button(
        text="Выгрузить все CSV-файлы",
        callback_data=ParseCbData(id="_ALL_", university_id=university.id)
    )
    return kb.adjust(1)


# Клавиатура для команды speciality
def get_kb_speciality(speciality: Speciality, university: University):
    kb = InlineKeyboardBuilder()
    kb.button(
        text="CSV-файл рейтинга абитуриентов",
        callback_data=ParseCbData(id=speciality.id, university_id=university.id)
    )
    return kb.adjust(1)


# Клавиатура/кнопка Back
def get_kb_back(callback_data):
    return InlineKeyboardBuilder().button(
            text="🔙 Назад",
            callback_data=callback_data
    ).adjust(1)
