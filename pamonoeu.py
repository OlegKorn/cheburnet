from bs4 import BeautifulSoup as bs
import requests
import re
from time import sleep
import shutil


headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36"
}
page = 1

url = f"https://www.pamono.eu/sculpture-figurative?p={str(page)}&style=2931%2C4250"


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
        
        self.path = f"G:/Desktop/{name}"

        with open(self.path,'wb') as f:
            shutil.copyfileobj(self.r.raw, f)
            sleep(1.5)
            shutil.copyfileobj(self.r.raw, f, 50000)




p = P()
urls = p.get_fotos_of_item("https://www.pamono.eu/karl-hagenauer-for-werkstatte-hagenauer-female-bust-1930s-brass")
for url in urls:
    _ = url.split(" : ")[0]
    name = url.split(" : ")[1]
    
    p.download_file(_, name)

'''
last_page = p.get_last_page(url)

for page in range(1, int(last_page)+1):
    url = f"https://www.pamono.eu/sculpture-figurative?p={str(page)}&style=2931%2C4250"
    print(url)
    # p.get_fotos_of_item()
'''
# p.get_fotos_of_item("https://www.pamono.eu/karl-hagenauer-for-werkstatte-hagenauer-female-bust-1930s-brass")
