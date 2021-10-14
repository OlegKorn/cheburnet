import requests, os, time, sys
from bs4 import BeautifulSoup as bs
import re
import shutil 
from urllib.request import Request, urlopen  # https://qna.habr.com/q/167569
import logging 


FORMAT = '%(message)s'

HOME_DIR = 'G:/Desktop/py/planetsuzy/'
initial_url = 'http://www.planetsuzy.org/t360180-p1-elizabeth-ryan-lizzie-ryan-avia-lizzie.html'


class PlanetS:
    '''
    Without banned like pimpandhost
    '''
    def download_from_file(self):
        f = open("G:/Pictures/deni moor/porncoven.txt", "r")

        data = f.readlines()

        for i in data:
            counter = 0

            link = i.split(': "')[1].replace('"', '').strip()
            if not ".zip" in i:
                filename = link[-10::].replace("/", "")
                soup = self.get_soup(link)
            
                try:
                    if "imagevenue" in link:
                        url = soup.find("div", class_="card-body").div.div.a.img['src']
                        if url:
                           self.download_file(url, filename)
                    
                    if "imgbox" in link:
                        url = soup.find("div", class_="image-container").img['src']
                        if url:
                           self.download_file(url, filename)

                    if "imagebam" in link:
                        url = soup.find("div", class_="view-image").find_all("img")[1]['src']
                        if url:
                           self.download_file(url, filename)

                    print(filename, " ", counter, " ", link, ' -> ', url, end='\n')
                    counter += 0

                except Exception as e:
                    print(link, '->', e)
                    break

                   
    def download_file(self, url, filename):
        self.r = requests.get(url, stream=True)

        if self.r.status_code == 200:
            self.path = f"G:/Pictures/deni moor/{filename}.jpg"

        with open(self.path,'wb') as f:
            shutil.copyfileobj(self.r.raw, f)
            time.sleep(1.5)
            shutil.copyfileobj(self.r.raw, f, 50000)
   

    def get_name(self, url, create_dir=False,):
        self.model_name = re.search(r'\d+\-.*[0-9].(.*).html', url).group(1)

        if create_dir:
            if not os.path.exists(HOME_DIR):
                os.mkdir(HOME_DIR, mode=0o777)
                print(HOME_DIR + ' created')
            if not os.path.exists(HOME_DIR + self.model_name):
                os.mkdir(HOME_DIR + self.model_name, mode=0o777)
                print(f'{HOME_DIR + self.model_name} created')
            else:
                print(f'{HOME_DIR + self.model_name} exists')

        return self.model_name


    def get_soup(self, url):
        self.session = requests.Session()
        self.request = self.session.get(url)
        self.sc = self.request.status_code
        self.soup = bs(self.request.content, 'html.parser')

        return self.soup

    
    def get_r_via_TOR(self, url):
        proxies = {
            'http': 'socks5h://127.0.0.1:9150', 
            'https': 'socks5h://127.0.0.1:9150'
        }
        session = requests.Session()
        r = session.get(url, proxies=proxies)
        return r


    def get_soup_via_TOR(self, url):
        proxies = {
            'http': 'socks5h://127.0.0.1:9150', 
            'https': 'socks5h://127.0.0.1:9150'
        }

        session = requests.Session()
        r = session.get(url, proxies=proxies)
        self.soup = bs(r.content, 'html.parser')

        print(r.status_code)
        
        return self.soup

    
    def get_last_page(self, url):
        self.soup = self.get_soup(url)

        try:
            self.last_page = self.soup.find('div', attrs={'class' : 'pagenav awn-ignore'}).find('td', attrs={'nowrap': 'nowrap'}).a
            self.last_page = re.search(r'page=(\d+)', self.last_page['href']).group(0).replace('page=', '')
        except Exception as e:
            self.last_page = re.search(r'of (\d*)', self.soup.find('div', class_='pagenav awn-ignore') \
                               .find_all('td')[0].text) \
                               .group(0) \
                               .replace('of ', '')

        return self.last_page



ps = PlanetS()
# ps.write_all_pages_urls_of_model(initial_url)
# ps.get_all_fotos_url_of_model()
ps.download_from_file()
