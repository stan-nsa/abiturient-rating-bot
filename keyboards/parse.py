from enum import Enum

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from university import University


class ParseType(Enum):
    university = 'university'
    speciality = 'speciality'


class ParseCbData(CallbackData, prefix='parse'):
    type: ParseType
    id: str


# Клавиатура для команды parse
def get_kb_parse(univers: dict[University]):
    kb = [
        InlineKeyboardButton(
            text=univer.name,
            callback_data=ParseCbData(type=ParseType.university, id=univer.id).pack()
        )
        for univer in univers.values()
    ]
    return InlineKeyboardBuilder().add(*kb).adjust(1)


# Клавиатура для команды university
def get_kb_university(university: University):
    kb = [
        InlineKeyboardButton(
            text=speciality.name,
            callback_data=ParseCbData(type=ParseType.speciality, id=speciality.id).pack()
        )
        for speciality in university.specialties.values()
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
