from bs4 import BeautifulSoup as bs
import requests
import re, os
import shutil
import logging
from time import sleep


headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0"
}

page = 1
url = f"https://www.pamono.eu/work-on-paper-figurative?design_period_new=941&p={str(page)}"


def get_filter(): 
    s = requests.Session()
    r = s.get(url, headers=headers)
    soup = bs(r.content, 'html.parser')
    filtr = soup.find("div", class_="filter-state").find("span", class_="value").text.strip()

    return filtr

try:
    f = get_filter()

    search_wo_query = re.search(r'eu/(.*?)\?design', url).group(1)
    if search_wo_query:
        path = f"/home/oleg/Public/py/{search_wo_query}_{f}/"
        print(path)
        log_name = f"{search_wo_query}_{f}"
                        
        if os.path.exists(path):
            print(path, " exists")

        if not os.path.exists(path):
            os.makedirs(path, mode=0o777)

    if not search_wo_query:
        search = re.search("&q=(.*)", url).group(1)
        if search:
            path = f"/home/oleg/Public/py/{search}_{f}/"
            print(path)
            log_name = f"{search}_{f}"
                            
            if os.path.exists(path):
                print(path, " exists")
                            
            if not os.path.exists(path):
                os.makedirs(path, mode=0o777)
                                        
except Exception as e:
    print(e)



class Pamono:
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
            return False

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


    def write_links_of_fotos_of_an_item(self, url):
        FORMAT = '%(message)s'
        logging.basicConfig(
            filename=path + log_name + ".log",
            level=logging.INFO,
            format=FORMAT
        )

        self.s = self.get_soup(url) 
        sleep(0.25)

        all_items = self.s.find("div", class_="main-content").find_all("a", class_="link")
        for i in all_items:
            href = i["href"]
            print(href)

            if len(all_items) == all_items.index(i) + 1:
                print("-----------------------")

            logging.info(href)


    def download_file(self):
        print("DOWNLOADING BEGAN...")

        log = path + log_name + ".log"
        f = open(log, "r")

        for link in f.readlines():
            title = link.split('/')[8].strip() 
            
            self.session = requests.Session()
            self.r = requests.get(link.strip(), stream=True)
            self.image = self.r.raw.read()
            print(title)
            open(path + title, "wb").write(self.image)


p = Pamono()

last_page = p.get_last_page(url)
for page in range(1, int(last_page)+1):
    url = f"https://www.pamono.eu/work-on-paper-figurative?design_period_new=941&p={str(page)}"

    items = p.get_items_of_page(url)

    for item in items[:-1]:
        print("\n-----------------------")
        print(f"{item}, page={page} of {last_page}, item number={items.index(item)} of {len(items)}")
        p.write_links_of_fotos_of_an_item(item)

p.download_file()


