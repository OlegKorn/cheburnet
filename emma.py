#/usr/bin/env python3
import requests, sys, os, time
from bs4 import BeautifulSoup as bs


class Emma:

    HOME_DIR = '/home/o/Документы/PYTHON_SCRIPTS/ero/emmastoneweb/'
    INI_URL = 'https://emmastoneweb.com/gallery/index.php'
    SITE_ROOT = 'https://emmastoneweb.com/gallery/'

    headers = {
           'access-control-allow-origin' : '*',
           'Request Method' : 'GET',
           'Status Code' : '200',
           'Remote Address' : '64.233.163.101:443',
           'Referrer Policy' : 'no-referrer-when-downgrade',
           'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }

   
    def get_soup(self, url):
        self.session = requests.Session()
        self.request = self.session.get(url)
        self.soup = bs(self.request.content, 'html.parser')
        return self.soup

    
    def get_categories(self):

        self.categories = HOME_DIR + 'categories.txt'

        self.soup = self.get_soup(Emma.INI_URL)
        
        try: 
            self.categories_links = open(self.categories, 'w')

            for self.imgset in self.soup.find_all('span', class_='catlink'):
                self.category = Emma.SITE_ROOT + self.imgset.a.get('href')
                
                self.categories_links.write(self.category + '\n')

                #print(self.category)
               
        except Exception as e:
            print(e)
            pass

        self.categories_links.close()
        del self.soup

      

    def get_subcats(self):
        self.subcats = HOME_DIR + 'subcats.txt'
        
        try: 
            self.subcats_links = open(self.subcats, 'w')
            self.categories = open(HOME_DIR + 'categories.txt', 'r')

            for cat in self.categories:
                cat = cat.strip()
                self.soup = self.get_soup(cat)

                for self.cat_album in self.soup.find_all('span', class_='catlink'):
                    self.album_name = self.cat_album.a.text
                    self.album_link = Emma.SITE_ROOT + self.cat_album.a['href']
                    print(self.album_name, self.album_link, sep = ': ')
                    self.subcats_links.write(self.album_link + '\n')

                del self.soup
               
        except Exception as e:
            print(e)
            pass



    def get_albums_urls(self):
        self.albums = HOME_DIR + 'albums.txt'
       
        try: 
            self.albums_links = open(self.albums, 'w')
            self.subcats = open(HOME_DIR + 'subcats.txt', 'r')

            for subcat in self.subcats:
                subcat = subcat.strip()
                self.soup = self.get_soup(subcat)

                for self.album in self.soup.find_all('a', class_='albums'):
                    self.albums_links.write(Emma.SITE_ROOT + self.album['href'].strip() + '\n')
                    print(Emma.SITE_ROOT + self.album['href'])

                del self.soup
               
        except Exception as e:
            print(e)
            pass



    def save_img(self):
        self.counter = 1
        self.albums = open(HOME_DIR + 'albums.txt', 'r')

        for album in self.albums:
            try:
                album = album.strip()
                self.soup = self.get_soup(album)

                for foto in self.soup.find_all('img', attrs={'image thumbnail'}):
                    self.foto_url = Emma.SITE_ROOT + foto['src'].replace('thumb_', '')
                    self.foto_title = self.foto_url[39::].replace('/', '_').replace('%', '_')
                    
                    # if a file does not exists - download it
                    if not os.path.exists(HOME_DIR + self.foto_title):
                        self.foto_title = self.foto_url[75::].replace('/', '_').replace('%', '_')
                        self.session = requests.Session()
                        self.r = requests.get(self.foto_url, stream=True)
                        self.image = self.r.raw.read()
                        print(self.foto_url, self.counter, sep = "    ")
                        open(Emma.HOME_DIR + self.foto_title, "wb").write(self.image)

                        del self.session

                        self.counter += 1
                    
                    # if a file already exists - skip action and iterate to the next one
                    else: 
                        print(f'{self.foto_title} EXISTS', self.counter, sep = "    ")
                        self.counter += 1
                        pass

                del self.soup
                
            except Exception:
                print('error')
                continue
        



e = Emma()
#print(e.INI_URL)
#e.get_categories()
#e.get_subcats()
#e.get_albums_urls()
e.save_img()

