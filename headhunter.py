import os.path
import requests
from bs4 import BeautifulSoup as soup


class HeadHunter:
    url = "https://hh.ru/search/vacancy?area=1&area=2&clusters=true&enable_snippets=true&experience=noExperience&" \
          "no_magic=true&ored_clusters=true&text=стажер+python&order_by=publication_time&hhtmFrom=vacancy_search_list"
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
        items = self.html.select('.serp-item__title')
        for item in items:
            if item['href'] != self.lastkey:
                vacancies.append(item['href'])
            else:
                break
        return vacancies

    def get_lastkey(self):
        items = self.html.select('.serp-item__title')
        return items[0]['href']

    def update_lastkey(self, new_key):
        self.lastkey = new_key
        with open(self.lastkey_file, "r+") as f:
            data = f.read()
            f.seek(0)
            f.write(str(new_key))
            f.truncate()
        return new_key
