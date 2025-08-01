from dataclasses import dataclass
from environs import Env
from pathlib import Path

from university import University, Speciality

@dataclass
class TgBot:
    token: str          # Токен для доступа к телеграм-боту
    bot_url: str        # URL телеграм-бота


@dataclass
class Storage:
    folder: str              # Путь к директории для сохранения файлов
    file_name_template: str  # Шаблон имени файла
    folder_path: Path


@dataclass
class Rank:
    id: str
    points_minimum: int


@dataclass
class Config:
    bot: TgBot
    storage: Storage
    rank: Rank


env = Env()
env.read_env()


# Создаем экземпляр класса Config и наполняем его данными из переменных окружения
config = Config(
    bot=TgBot(
        token=env('BOT_TOKEN', default=''),
        bot_url=env('BOT_URL', default=''),
    ),
    storage=Storage(
        folder=env('FOLDER', default='tmp'),
        file_name_template=env('FILE_NAME_TEMPLATE', default='%s.csv'),
        folder_path=Path(env('FOLDER', default='tmp')),
    ),
    rank=Rank(
        id=env('ID', default=''),
        points_minimum=env.int('POINTS_MINIMUM', default=0),
    ),
)

univers = {
    'guap':
        University(
            id='guap',
            name='ГУАП',
            specialties={
                '09.03.02':
                    Speciality(
                        id='09.03.02',
                        name='09.03.02 - Информационные системы и технологии',
                        url='https://priem.guap.ru/bach/rating/list_1_18_1_1_1_f',
                    ),
                '09.03.03-19':
                    Speciality(
                        id='09.03.03',
                        name='09.03.03 - Прикладная информатика - и программирование',
                        url='https://priem.guap.ru/bach/rating/list_1_19_1_1_1_f',
                    ),
                '09.03.03-507':
                    Speciality(
                        id='09.03.03',
                        name='09.03.03 - Прикладная информатика - в информационной сфере',
                        url='https://priem.guap.ru/bach/rating/list_1_507_1_1_1_f',
                    ),
                '11.03.02':
                    Speciality(
                        id='11.03.02',
                        name='11.03.02 - Инфокоммуникационные технологии и системы связи',
                        url='https://priem.guap.ru/bach/rating/list_1_38_1_1_1_f',
                    ),
                '27.03.04':
                    Speciality(
                        id='27.03.04',
                        name='27.03.04 - Управление в технических системах',
                        url='https://priem.guap.ru/bach/rating/list_1_122_1_1_1_f',
                    ),
                '27.03.05':
                    Speciality(
                        id='27.03.05',
                        name='27.03.05 - Инноватика',
                        url='https://priem.guap.ru/bach/rating/list_1_123_1_1_1_f',
                    ),
            },
        ),
    'voenmeh':
        University(
            id='voenmeh',
            name='ВоенМех',
            specialties={
                '09.03.02':
                    Speciality(
                        id='09.03.02',
                        name='09.03.02 - Информационные системы и технологии',
                        url='https://lk.priem.voenmeh.ru/rating/rating',
                    ),
            },
        ),
}
