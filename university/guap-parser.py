# Зелёный = class="table-success"
# Синий = class="table-primary no_original"
# Серый = class ="table-secondary another_rating"


import requests
from bs4 import BeautifulSoup
import csv

sashka_id = '4415693'
max_pts = 251

spec_list = {
    '09.03.02 - Информационные системы и технологии': 'https://priem.guap.ru/bach/rating/list_1_18_1_1_1_f',
    '09.03.03 - Прикладная информатика - и программирование': 'https://priem.guap.ru/bach/rating/list_1_19_1_1_1_f',
    '09.03.03 - Прикладная информатика - в информационной сфере': 'https://priem.guap.ru/bach/rating/list_1_507_1_1_1_f',
    '11.03.02 - Инфокоммуникационные технологии и системы связи': 'https://priem.guap.ru/bach/rating/list_1_38_1_1_1_f',
    '27.03.04 - Управление в технических системах': 'https://priem.guap.ru/bach/rating/list_1_122_1_1_1_f',
    '27.03.05 - Инноватика': 'https://priem.guap.ru/bach/rating/list_1_123_1_1_1_f',
}
# url = 'https://priem.guap.ru/bach/rating/list_1_18_1_1_1_f'

row_colors = {
    "table-success": 1,
    "table-primary no_original": 2,
    "table-secondary another_rating": 3,
    "table-light": 4,
}

save_path = 'tmp/'
csv_file_tpl = '%.csv'

for spec, url in spec_list.items():
    #-- Получение данных с сайта --
    # r = requests.get(url, params={"Content-Type": "text/html; charset=utf-8"})
    r = requests.get(url, params={"Content-Type": "text/html; charset=windows-1251"})
    html_content = BeautifulSoup(r.content, "html.parser")

    table = html_content.find_all('table')[0]

    thead = table.contents[0]
    tbody = table.contents[1]

    text_head = ['Цвет: 1=зелёный, 2=голубой, 3=серый, 4=белый']
    for tr in thead:
        for th in tr.contents:
            text_head.append(th.text)

    tbody_lines = []
    for tr in tbody:
        pts = tr.contents[3].text
        if pts.isdigit():
            if int(pts) < max_pts:
                break

        tr_class = ' '.join(map(str, tr.attrs['class']))
        text_line = [row_colors[tr_class]]
        for td in tr.contents:
            text_line.append(td.get_text(', '))
        tbody_lines.append(text_line)

    with open(save_path + csv_file_tpl.replace('%', spec), "w", newline='', encoding='windows-1251') as f:
        csv_writer = csv.writer(f, dialect='excel', delimiter=';')
        csv_writer.writerow(text_head)
        csv_writer.writerows(tbody_lines)

    break
