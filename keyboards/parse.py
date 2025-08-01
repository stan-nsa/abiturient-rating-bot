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
def get_kb_parse(univers: dict[University]):
    kb = [
        InlineKeyboardButton(
            text=univer.name,
            callback_data=UniversityCbData(id=univer.id).pack()
        )
        for univer in univers.values()
    ]
    return InlineKeyboardBuilder().add(*kb).adjust(1)


# Клавиатура для команды university
def get_kb_university(university: University):
    kb = [
        InlineKeyboardButton(
            text=speciality.name,
            callback_data=SpecialityCbData(id=speciality.id, university_id=university.id).pack()
        )
        for speciality in university.specialties.values()
    ]
    return InlineKeyboardBuilder().add(*kb).adjust(1)


# Клавиатура для команды speciality
def get_kb_speciality(speciality: Speciality, university: University):
    kb = [
        InlineKeyboardButton(
            text="CSV-файл рейтинга абитуриентов",
            callback_data=ParseCbData(id=speciality.id, university_id=university.id).pack()
        ),
    ]
    return InlineKeyboardBuilder().add(*kb).adjust(1)


# # Клавиатура для команды score
# def get_kb_score(schedule: Schedule):
#     return InlineKeyboardBuilder().add(
#         InlineKeyboardButton(
#             text=f"{ico['info']}Details",
#             callback_data=ScheduleCbData(type=ScheduleType.details, date=schedule.date).pack()
#         ),
#     )
#
#
# # Клавиатура для команды schedule
# def get_kb_schedule(schedule: Schedule):
#     return InlineKeyboardBuilder().add(
#         InlineKeyboardButton(
#             text=f"{ico['info']}Details",
#             callback_data=ScheduleCbData(type=ScheduleType.details, date=schedule.current_date).pack()
#         ),
#         InlineKeyboardButton(
#             text=f"{schedule.prev_date}{ico['prev']}",
#             callback_data=ScheduleCbData(type=ScheduleType.schedule, date=schedule.prev_date).pack()
#         ),
#         InlineKeyboardButton(
#             text=f"{ico['next']}{schedule.next_date}",
#             callback_data=ScheduleCbData(type=ScheduleType.schedule, date=schedule.next_date).pack()
#         ),
#     ).adjust(1,2)
