from bs4 import BeautifulSoup as bs
import requests
import re, os
import shutil
import logging
from time import sleep
import wget
from string import punctuation
from unidecode import unidecode


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
}
category = "_furniture_decorative-objects"

base_url = "https://www.1stdibs.com"
BASE_PATH = "G:/Desktop/py/1stdibs/"

url = "https://www.1stdibs.com/furniture/decorative-objects/?per=1910s,1920s,early-1900s"


def get_filters():
    fil = re.search("/?per=(.*)$", url).group(1).replace(",", "_") + category
    return fil


def create_dir(filters=get_filters()):
    p = BASE_PATH + filters
    if os.path.exists(p):
        print(p, "exists")
       
    if not os.path.exists(p):
        os.makedirs(p, mode=0o777)


class Pizda:

    def get_soup(self, url):
        self.session = requests.Session()
        self.request = self.session.get(url, headers=headers)
        self.soup = bs(self.request.content, 'html.parser')

        return self.soup


    def get_last_page(self, url=url):
        self.s = self.get_soup(url)
       
        try:
            self.last_page = int(self.s.find('ul', attrs={"data-tn": "pagination-list"})["data-tp"])
        except Exception as e:
            return False

        return self.last_page


    def write_all_anchors_of_found_items(self):
        page = 1

        FORMAT = '%(message)s'
        logging.basicConfig(
            filename= BASE_PATH + get_filters() + "/" + get_filters() + "_all_items_anchors.log",
            level=logging.INFO,
            format=FORMAT
        )
 
        for i in range(page, self.get_last_page()+1):
            if page == 1:
                url = "https://www.1stdibs.com/furniture/decorative-objects/?per=1910s,1920s,early-1900s"
            else:
                url = f"https://www.1stdibs.com/furniture/decorative-objects/?page={str(page)}&per=1910s,1920s,early-1900s"
           
            print()
            print(page, "=========", sep=" ")
            print(url)
            print(page, "=========", sep=" ")
           
           
            soup = self.get_soup(url)
                       
            # links all items of a page of search results
            a = soup.find_all("a", attrs={"data-tn":"item-tile-title-anchor"})
           
            for i in a:
                try:
                    item_anchor = base_url + i["href"]
                    print(item_anchor)
                    logging.info(item_anchor)
                except Exception as e:
                    print("ERROR: ", e)
                    pass
           
            page += 1


    def write_author_title_and_url_of_one_photo(self):

        FORMAT = '%(message)s'
        logging.basicConfig(
            filename= BASE_PATH + get_filters() + "/" + get_filters() + "_authors_titles_and_urls_of_photos.log",
            level=logging.INFO,
            format=FORMAT
        )

        all_items_anchors = open(BASE_PATH + get_filters() + "/" + get_filters() + "_all_items_anchors.log", "r")
       
        for line in all_items_anchors.readlines():
            soup = self.get_soup(line.strip())                
            src = soup.find("button", attrs={"data-tn": "pdp-image-carousel-image-1"}).find("img")["src"].replace("?width=768", "")
     
            # deleting forbidden chars
            forbidden_chars = re.escape(punctuation)
           
            try:
                author_and_title = soup.find("h1", attrs={"data-tn": "pdp-resp-title"}).text

                # deleting forbidden chars
                author_and_title = re.sub('['+forbidden_chars+']', '', author_and_title)
                unidecode(author_and_title)          
            except:
                author_and_title = "Unknown Author"
             
            try:
                year = soup.find("p", attrs={"data-tn": "pdp-item-creation-date"}).text
            except:
                year = "Unknown Year"
               
            data = author_and_title + "++" + year + "++" + src
           
            print("===========")
            print("URL: ", "..." + line[20:].strip())
            print(line.strip())
            print(author_and_title)
            print()

            try:
                logging.info(data)
            except Exception as e:
                print(e)
                continue


    def download_file(self):
        try:
            print("DOWNLOADING BEGAN...")

            f = open(BASE_PATH + get_filters() + "/" + get_filters() + "_authors_titles_and_urls_of_photos.log", "r")

            for link in f.readlines():
                url = link.split('++')[2].strip()
               
                author_and_title = link.split('++')[0].strip()
               
                print(author_and_title, url, sep=" - ")
                print("++++++++++++")

                p = BASE_PATH + get_filters()
               
                self.session = requests.Session()
                self.r = requests.get(url, stream=True)
                self.image = self.r.raw.read()
                open(p + "/" + author_and_title + ".jpg", "wb").write(self.image)
       
        except ValueError as e:
            print(e)
            pass
       
create_dir()

p = Pizda()
# p.write_all_anchors_of_found_items()
p.write_author_title_and_url_of_one_photo()
# p.download_file()
