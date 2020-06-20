#/usr/bin/env python3
import requests, sys, os, time
from bs4 import BeautifulSoup as bs
import re


class DD:

    HOME_DIR = '/home/o/Документы/PYTHON_SCRIPTS/ero/dd/'


    urls = [
        'http://vintage-erotica-forum.com/t19047-lynne-austin.html'
    ]
    

    headers = {
           'access-control-allow-origin' : '*',
           'Request Method' : 'GET',
           'Status Code' : '200',
           'Remote Address' : '64.233.163.101:443',
           'Referrer Policy' : 'no-referrer-when-downgrade',
           'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }

   
    def get_name(self, url):
        self.model_name = re.search(r'\d+\-(.*).html', url).group(1)
        print(self.model_name)

        if not os.path.exists(DD.HOME_DIR + self.model_name):
            os.mkdir(DD.HOME_DIR + self.model_name, mode=0o777)
        else:
        	print(f'{DD.HOME_DIR + self.model_name} exists')

        return self.model_name


    def get_soup(self, url):
        self.session = requests.Session()
        self.request = self.session.get(url)
        self.soup = bs(self.request.content, 'html.parser')
        return self.soup


    def get_last_page(self):
        for url in DD.urls:
            self.get_soup(url)
            self.model_name = self.get_name(url)
            self.soup = self.get_soup(url)

            self.last_page = self.soup.find('div', class_='pagenav awn-ignore').find('td', attrs={'nowrap': 'nowrap'}).a
            self.last_page = re.search(r'page=(\d+)', self.last_page['href']).group(0).replace('page=', '')
            print(self.last_page)

        return self.last_page

    
    def write_all_pages_urls_of_model(self):

        for url in DD.urls:
            self.model_name = self.get_name(url)
            f = open(DD.HOME_DIR + self.model_name + '/' + self.model_name + '.txt', 'w')
            
            self.pages_num = self.get_last_page()
            for i in range(1, int(self.pages_num) + 1): 
                self.url_ = url.replace(self.model_name, 'p' + str(i) + '-' + self.model_name) 
                print(self.url_)
                f.write(self.url_)
                f.write('\n')

        f.close()


    def save_img(self):
        self.counter = 1
        self.albums = open('/home/o/Документы/PYTHON_SCRIPTS/ero/emmastoneweb/albums.txt', 'r')

        for album in self.albums:
            try:
                album = album.strip()
                self.soup = self.get_soup(album)

                for foto in self.soup.find_all('img', attrs={'image thumbnail'}):
                    self.foto_url = Emma.SITE_ROOT + foto['src'].replace('thumb_', '')
                    self.foto_title39 = self.foto_url[39::].replace('/', '_').replace('%', '_')
                    self.foto_title75 = self.foto_url[75::].replace('/', '_').replace('%', '_')
                    
                    # if a file does not exists - download it
                    if not os.path.exists('/home/o/Документы/PYTHON_SCRIPTS/ero/emmastoneweb/' + self.foto_title39):
                        if not os.path.exists('/home/o/Документы/PYTHON_SCRIPTS/ero/emmastoneweb/' + self.foto_title75):

                            self.foto_title = self.foto_url[75::].replace('/', '_').replace('%', '_')
                            self.session = requests.Session()
                            self.r = requests.get(self.foto_url, stream=True)
                            self.image = self.r.raw.read()
                            print(self.foto_title, self.counter, sep = "  ")
                            open(Emma.HOME_DIR + self.foto_title, "wb").write(self.image)

                            del self.session

                            self.counter += 1
                    
                    # if a file already exists - skip action and iterate to the next one
                    else: 
                        print(f'{self.foto_title75} EXISTS', self.counter, sep = "    ")
                        self.counter += 1
                        pass

                del self.soup
                
            except Exception:
                print('error')
                continue
        



dd = DD()
#print(e.INI_URL)
#e.get_categories()
#e.get_subcats()
#e.get_albums_urls()
dd.write_all_pages_urls_of_model()

