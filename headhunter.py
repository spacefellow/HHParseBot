import os.path
import requests
from bs4 import BeautifulSoup as soup


class HeadHunter:
    url = "https://hh.ru/search/vacancy?text=Python+стажер&area=1&area=2&salary=&currency_code=RUR&experience" \
          "=noExperience&order_by=publication_time&search_period=0&items_on_page=50&no_magic=true&L_save_area=true "
    headers = {
         "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/102.0.5005.115 Safari/537.36 OPR/88.0.4412.75"}

    lastkey = ""
    lastkey_file = ""
    r = requests.get(url, headers=headers)
    html = soup(r.content, 'html.parser')

    def __init__(self, lastkey_file):
        self.lastkey_file = lastkey_file

        if os.path.exists(lastkey_file):
            self.lastkey = open(lastkey_file, 'r').read()
        else:
            f = open(lastkey_file, 'w')
            self.lastkey = self.get_lastkey()
            f.write(self.lastkey)
            f.close()

    def new_vacancies(self):
        vacancies = []
        items = self.html.select('.g-user-content > a')
        for item in items:
            if item['href'] != self.lastkey:
                vacancies.append(item['href'])
            else:
                break
        return vacancies

    def get_lastkey(self):
        items = self.html.select('.g-user-content > a')
        return items[0]['href']

    def update_lastkey(self, new_key):
        self.lastkey = new_key
        with open(self.lastkey_file, "r+") as f:
            data = f.read()
            f.seek(0)
            f.write(str(new_key))
            f.truncate()
        return new_key
