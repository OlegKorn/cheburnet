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
url = "https://www.pamono.eu/catalogsearch/result/index/?cat=1465&" + \
      f"design_period_new=943%2C944%2C956&p={str(page)}&q=painting&style=2921%2C2931%2C4250"


def get_filter(): 
    s = requests.Session()
    r = s.get(url, headers=headers)
    soup = bs(r.content, 'html.parser')

    filters_merged = ""

    filters = soup.find("ol", class_="items").find_all("span", class_="value")
    for f in filters:
        f = f.text.strip()
        filters_merged = filters_merged + f + ","

    filters_merged = filters_merged[:-1]
    print("huj = ", filters_merged)
    return filters_merged 


def create_dir(path):
    if os.path.exists(path):
        print(path, " exists")
    if not os.path.exists(path):
        os.makedirs(path, mode=0o777)


try:
    f = get_filter()
    print(f)
    
    if "\?design" in url:
        search_wo_query = re.search(r'eu/(.*?)\?design', url).group(1)
        if search_wo_query:
            path = f"/home/oleg/Public/py/{search_wo_query}_{f}/"
            print(path)
            log_name = f"{search_wo_query}_{f}"
            create_dir(path)        
            
    if "&q=" in url and not f:
        search = re.search("&q=(.*)", url).group(1)
        if search:
            path = f"/home/oleg/Public/py/{search}_{f}/"
            print(path)
            log_name = f"{search}_{f}"
            create_dir(path)
 
    if "design_period_new" or "style" in url:
        path = f"/home/oleg/Public/py/{f}"
        log_name = f"{path}/log.log"
        print(path, log_name)
        create_dir(path)

                  
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
            filename=log_name, #path + log_name + ".log",
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
        print(log)

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
    url = "https://www.pamono.eu/catalogsearch/result/index/?cat=1465&" + \
          f"design_period_new=943%2C944%2C956&p={str(page)}&q=painting&style=2921%2C2931%2C4250"
    print(url)

    items = p.get_items_of_page(url)

    for item in items[:-1]:
        print("\n-----------------------")
        print(f"{item}, page={page} of {last_page}, item number={items.index(item)} of {len(items)}")
        p.write_links_of_fotos_of_an_item(item)


p.download_file()


