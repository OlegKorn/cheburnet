from bs4 import BeautifulSoup as bs
import requests
import re
from time import sleep
import shutil
import logging
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool


headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0"
}

page = 1

url = f"https://www.pamono.eu/work-on-paper-figurative?design_period_new=956%2C944&p={str(page)}"
search = re.search(r".*?eu\/(.*)\?.*", url).group(1)

FORMAT = '%(message)s'
logging.basicConfig(
    filename=f"/home/oleg/Public/py/{search}/{search}.log",
    level=logging.INFO,
    format=FORMAT
)


class P:
    def get_soup(self, url):
        self.session = requests.Session()
        self.request = self.session.get(url, headers=headers)
        self.soup = bs(self.request.content, 'html.parser')

        return self.soup


    def get_last_page(self, url):
        self.s = self.get_soup(url)

        try:
            self.last_page = self.s.find('div', class_='pager'). \
                                    find('div', class_='label').text. \
                                    strip().split("of ")[1]
        except Exception as e:
            return True
        return self.last_page


    def get_items_of_page(self, url):
        self.s = self.get_soup(url)
        urls = []

        page_items = self.s.find('div', class_='products'). \
                            find_all('article', class_='product-card')

        for item in page_items:
            item_link = item.find("a").get("href")
            urls.append(item_link)

        return urls


    def get_item_name(self, url):
        self.s = self.get_soup(url)

        item_name = self.s.find("h1", class_="product-name").text.strip().replace(" ", "_").replace(",", ".")

        return item_name


    def get_fotos_of_item(self, url):
        items_urls = []
        number = 1
        name = self.get_item_name(url)
        name_modified = name.lower().replace(".", "").replace("_", "-")

        self.s = self.get_soup(url) 

        all_items = self.s.find_all("a", class_="link")

        for i in all_items:
            if name_modified in i["href"]:
                url_and_name = i["href"] + " : " + name_modified + "_" + str(number) + ".jpg"
                items_urls.append(url_and_name)

                number += 1

        return items_urls


    def download_file(self, url, name):
        self.r = requests.get(url, stream=True)

        self.path = f"/home/oleg/Public/py/{search}/{name}"

        with open(self.path,'wb') as f:
            shutil.copyfileobj(self.r.raw, f)
            sleep(1)
            shutil.copyfileobj(self.r.raw, f, 50000)

p = P()
last_page = p.get_last_page(url)

for page in range(1, int(last_page)+1):
    url = "https://www.pamono.eu/catalogsearch/result/" + \
           f"index/?cat=1465&design_period_new=956%2C944%2C943&p={str(page)}&q=woman"

    items = p.get_items_of_page(url)

    for item in items[:-1]:
        print("\n-----------------------")
        print(f"{item}, page={page} of {last_page}, item number={items.index(item)} of {len(items)}")
        print("-----------------------")

        items_urls = p.get_fotos_of_item(item)

        for url in items_urls:
            _ = url.split(" : ")[0]
            name = url.split(" : ")[1]

            print(_)
            logging.info(_)


'''
f = open(f"/home/oleg/Public/py/{search}/{search}.log", "r")
for i in f.readlines():
    _ = i.strip()
    name = _.split("/")[-1]
    print(_)
    p.download_file(_, name)
'''
