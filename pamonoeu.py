from bs4 import BeautifulSoup as bs
import requests
import re
from time import sleep
import shutil
import logging 


FORMAT = '%(message)s'
logging.basicConfig(
    filename="G:/Pictures/pamonoeu/accessories/1.log",
    level=logging.INFO, 
    format=FORMAT
)

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36"
}
page = 1

url = "https://www.pamono.eu/home-accessories?design_period_new=943%2C944%2C956" + \
    f"&p={str(page)}&style=2931%2C4250%2C4735%2C4251%2C4256%2C4739%2C4741%2C4" + \
    "744%2C4703%2C886%2C4746%2C4253%2C4749%2C4751%2C4753%2C4755%2C4756%2C4257" + \
    "%2C4764%2C4766%2C4767%2C4768%2C4776%2C4258%2C4260%2C4785%2C4651"

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

        item_all_items = self.s.find_all("a", class_="link")

        for i in item_all_items:
            if name_modified in i["href"]:
                url_and_name = i["href"] + " : " + name_modified + "_" + str(number) + ".jpg"
                items_urls.append(url_and_name)

                number += 1

        return items_urls    



                   
    def download_file(self, url, name):
        self.r = requests.get(url, stream=True)
        
        self.path = f"G:/Pictures/pamonoeu/accessories/{name}"

        with open(self.path,'wb') as f:
            shutil.copyfileobj(self.r.raw, f)
            sleep(1)
            shutil.copyfileobj(self.r.raw, f, 50000)




p = P()
last_page = p.get_last_page(url)

for page in range(1, int(last_page)+1):
    url = "https://www.pamono.eu/home-accessories?design_period_new=943%2C944%2C956" + \
          f"&p={str(page)}&style=2931%2C4250%2C4735%2C4251%2C4256%2C4739%2C4741%2C4" + \
          "744%2C4703%2C886%2C4746%2C4253%2C4749%2C4751%2C4753%2C4755%2C4756%2C4257" + \
          "%2C4764%2C4766%2C4767%2C4768%2C4776%2C4258%2C4260%2C4785%2C4651"
    items = p.get_items_of_page(url)

    for item in items[:-1]:
        print("-----------------------")
        print(f"{item}, page={page} of {last_page}, item number={items.index(item)} of {len(items)}")
        print("-----------------------\n")
    
        items_urls = p.get_fotos_of_item(item)

        for url in items_urls:
            _ = url.split(" : ")[0]
            name = url.split(" : ")[1]

            print(_)
            logging.info(_)

            # p.download_file(_, name) https://cdn20.pamono.com/p/z/8/4/845586_cdutd1m8ch/joseph-emmanuel-cormier-woman-dressed-in-veils-20th-century-terracotta-1.jpg

'''
f = open("G:/Pictures/pamonoeu/watercolor/1.log", "r")
p = P()

for i in f.readlines():
    print(i.strip())
    name = i.split("/")[-1].strip()
    p.download_file(i.strip(), name)
'''
