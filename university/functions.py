import requests
from bs4 import BeautifulSoup
import csv

from . import Speciality
import config


row_colors = {
    "table-success": 1,
    "table-primary no_original": 2,
    "table-secondary another_rating": 3,
    "table-light": 4,
}


def guap_get_data(speciality: Speciality, rank_id: str=None, rank_minimum: int=0) -> str:
    #-- Получение данных с сайта --
    r = requests.get(speciality.url, params={"Content-Type": "text/html; charset=utf-8"})
    html_content = BeautifulSoup(r.content, "html.parser")

    html_table = html_content.find_all('table')[0]

    html_thead = html_table.contents[0]
    html_tbody = html_table.contents[1]

    table_head = ['Цвет: 1=зелёный, 2=голубой, 3=серый, 4=белый']
    for tr in html_thead:
        for th in tr.contents:
            table_head.append(th.text)

    table_rows = []
    for tr in html_tbody:
        pts = tr.contents[3].text
        if pts.isdigit():
            if int(pts) < rank_minimum:
                break

        tr_class = ' '.join(map(str, tr.attrs['class']))
        table_row = [row_colors[tr_class]]
        for td in tr.contents:
            table_row.append(td.get_text(', '))
        table_rows.append(table_row)

    file_path = config.config.storage.folder_path.joinpath(config.config.storage.file_name_template % speciality.name)
    # with open(file_path, "w", newline='') as f:
    with open(file_path, "w", newline='', encoding = 'windows-1251') as f:
        csv_writer = csv.writer(f, dialect='excel', delimiter=';')
        csv_writer.writerow(table_head)
        csv_writer.writerows(table_rows)

    return file_path
