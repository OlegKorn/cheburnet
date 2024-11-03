from bs4 import BeautifulSoup as bs
import requests
import re, os, sys
from time import sleep
import shutil
from fake_headers import Headers

from mutagen.mp3 import MP3
from mutagen.mp4 import MP4

from string import punctuation
from unidecode import unidecode


# это корневая директория, ее можно создать или указать существующую
DIR = "G:/Desktop/MP3"

# это URL, с найденным автором и его песнями, ее придется менять вручную для каждого поиска
# вот так она выглядит в браузере: https://muzofond.fm/search/alison krauss cox family
url = "https://muzofond.fm/search/alison%20krauss%20union%20station"


class Saver:
    def get_soup(self, url):
        session = requests.Session()
        headers = Headers(os="mac", headers=True).generate()

        self.request = session.get(url, headers=headers)
        self.soup = bs(self.request.content, 'html.parser')

        return self.soup


    def get_author_name_as_it_was_searched(self, url=url):
        self.s = self.get_soup(url)
        try:
            author_name_as_it_was_searched = self.s.find('h1', class_='topLineNameHeader').text.strip()
        except AttributeError:
            author_name_as_it_was_searched = self.s.find('div', class_='item main').find("h1").text.strip()

        return author_name_as_it_was_searched


    def get_mp3s_of_author_page(self, url=url):
        self.s = self.get_soup(url)
        mp3s_of_author = []

        try:
            page_items = self.s.find('ul', class_='mainSongs unstyled songs').find_all('li', class_='item')
        except:
            page_items = self.s.find('ul', class_='mainSongs unstyled songsListen songs').find_all('li', class_='item')

        try:
            for item in page_items:
                mp3_link = item.find("li", class_="play").get("data-url")
                mp3_title = item.find("span", class_="track").text.strip()

                track_data = mp3_link + ":::" + mp3_title
                mp3s_of_author.append(track_data)
            
            return mp3s_of_author
        except Exception as e:
            print("get_mp3s_of_author_page()", e)
            return


    def create_author_dir(self, author_path):
        '''
        СОЗДАЕТ ПАПКУ С ИМЕНЕМ ПОИСКА
        ПРИМЕР: https://muzofond.fm/search/alison krauss cox family
        Я ИСКАЛ ПО "Alison krauss cox family", ЗНАЧИТ ПАПКА, КУДА БУДУТ СОХРАНЯТЬСЯ НАЙДЕННЫЕ ПО ЭТОМУ 
        ПОИСКУ ТРЕКИ, БУДЕТ "DIR" + "поисковая фраза"; пример - G:/Desktop/MP3/Alison krauss cox family"
        '''

        if os.path.exists(author_path):
            print(f"{author_path} exists")

        else:
            os.makedirs(author_path, mode=0o777)
            print(f"{author_path} is already created")


    def download_file(self):
        '''
        Сохраняет все найденные в поиске файлы мп3 с именем, как на сайте:
        G:/Desktop/MP3/Alison krauss cox family/Another Day, Another Dollar (The Cox Family 1992)
        G:/Desktop/MP3/Alison krauss cox family/Never Will Give Up (I Know Who Holds Tomorrow 1994) и тд
        '''

        author_name_as_it_was_searched = self.get_author_name_as_it_was_searched()
        author_mp3s = self.get_mp3s_of_author_page()
        headers = Headers(headers=True).generate()

        self.create_author_dir(f"{DIR}/{author_name_as_it_was_searched}")
        
        for author_mp3 in author_mp3s:
            mp3_link = author_mp3.split(":::")[0]

            mp3_title = author_mp3.split(":::")[1]
            # deleting forbidden chars
            FORBIDDEN_CHARS = re.escape(punctuation)
            mp3_title = re.sub('['+FORBIDDEN_CHARS+']', '', mp3_title).replace('"', "")
            mp3_title = unidecode(mp3_title) 

            self.r = requests.get(
                mp3_link,
                headers=headers, 
                stream=True
            )
            
            sleep(1)
            mp3 = self.r.raw.read()
            open(f"{DIR}/{author_name_as_it_was_searched}/{mp3_title}.mp3", "wb").write(mp3)  
            self.clear_mp3_metadata(f"{DIR}/{author_name_as_it_was_searched}/{mp3_title}.mp3") 

            print(f"Successful: {mp3_title}")       


    def clear_mp3_metadata(self, mp3_path):
        try:
            mp3 = MP3(mp3_path)
            mp3.delete()
            mp3.save()

        except Exception as e:
            print("clear_mp3_metadata --->", e)
            sys.exit()


s = Saver()
s.download_file()
