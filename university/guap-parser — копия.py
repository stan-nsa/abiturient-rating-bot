import requests
from bs4 import BeautifulSoup

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

save_path = '/tmp\\'
csv_file_tpl = '%.csv'

for spec, url in spec_list.items():
    #-- Получение данных с сайта --
    r = requests.get(url, params={"Content-Type": "text/html; charset=utf-8"})
    html_content = BeautifulSoup(r.content, "html.parser")

    table = html_content.findAll('table')[0]

    thead = table.contents[0]
    tbody = table.contents[1]

    text_head = ''
    for tr in thead:
        for th in tr.contents:
            text_head += f"{th.text};"
    text_head += '\n'

    tbody_lines = []
    for tr in tbody:
        pts = tr.contents[3].text
        if pts.isdigit():
            if int(pts) < max_pts:
                break

        text_line = ''
        for td in tr.contents:
            # text_line += f"{td.text};"
            text_line += f"{td.get_text(', ')};"
        text_line += '\n'
        tbody_lines.append(text_line)

    #-- Сохранение шаблона для отображения на сайте --
    with open(save_path + csv_file_tpl.replace('%', spec), "w") as f:
        f.write(text_head)
        f.writelines(tbody_lines)
