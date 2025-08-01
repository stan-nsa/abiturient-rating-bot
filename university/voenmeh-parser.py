import requests
# from bs4 import BeautifulSoup

sashka_id = '4415693'
max_pts = 251

# url = 'https://lk.priem.voenmeh.ru/rating/rating'
url = 'https://lk.priem.voenmeh.ru/rating/_dash-update-component'

save_path = '/tmp\\'
csv_file_tpl = '%.csv'

#-- Получение данных с сайта --
r = requests.post(url, params={"Content-Type": "application/json"})

data = r.json()

print(data)

#-- Сохранение шаблона для отображения на сайте --
# with open(save_path + csv_file_tpl.replace('%', spec), "w") as f:
#     f.write(text_head)
#     f.writelines(tbody_lines)
