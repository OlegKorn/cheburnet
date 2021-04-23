'''
let posts = document.getElementsByClassName('gallery-mosaic-asset__link');
arr__ = [];
for (let i = 0; i < posts.length; i++) {
    arr__.push(posts[i]["href"]);
};
arr__;
'''


import requests, os, time, sys
from bs4 import BeautifulSoup as bs
import re
import shutil 
from urllib.request import Request, urlopen  # https://qna.habr.com/q/167569


proxies = {
    'http': 'socks5h://127.0.0.1:9150', 
    'https': 'socks5h://127.0.0.1:9150'
}

class Getty:

    ROOT_URL = 'https://www.gettyimages.com'
    URL = 'https://www.gettyimages.com/photos/jessie-buckley?family=editorial'

    model_name = re.search('photos/(\w*-\w*)?', URL).group(1)
    HOME_DIR = f'G:/Desktop/py/getty/{model_name}/'

    def __init__(self):
        if not os.path.exists(Getty.HOME_DIR):
            os.mkdir(Getty.HOME_DIR, mode=0o777)
            print(f'Dir "{Getty.HOME_DIR}" created')
        else:
            print(f'Dir "{Getty.HOME_DIR}" exists')


    def get_soup(self, url, proxies=proxies, stream=True):
        self.session = requests.Session()
        self.request = self.session.get(url)
        self.soup = bs(self.request.content, 'html.parser')
        return self.soup


    def get_last_page(self):
        soup = self.get_soup(Getty.URL)
        
        for span in soup.find_all('span'):
            match = re.search(r'PaginationRow-module__lastPage___.*', str(span))
            if match:
                last_page = span.get_text()
                
        return last_page


    def write_links(self):
        last_page = int(self.get_last_page())

        links = open(Getty.HOME_DIR + Getty.model_name + '.txt', 'w')

        for i in range(1, last_page+1):
            print(i)

            if i == 1:
                soup = self.get_soup(Getty.URL)
                imgs = soup.find_all('a', class_='gallery-mosaic-asset__link')
                for i in imgs:
                    print(Getty.ROOT_URL + i['href'])
                    links.write(Getty.ROOT_URL + i['href'])
                    links.write('\n')

            else:
                page = f'&page={str(i)}'
                soup = self.get_soup(Getty.URL)
                imgs = soup.find_all('a', class_='gallery-mosaic-asset__link')
                for i in imgs:
                    print(Getty.ROOT_URL + i['href']) 
                    links.write(Getty.ROOT_URL + i['href'])
                    links.write('\n')

        links.close()   
                 

    def download_image(self):
        # print(requests.get('https://ifconfig.me', proxies=proxies).text)
        # print(requests.get('https://ifconfig.me').text)
            
        links = open(Getty.HOME_DIR + Getty.model_name + '.txt', 'r')
        fotos_downloaded = open(Getty.HOME_DIR + Getty.model_name + '_downloaded.txt', 'w')
        
        for i in links:
            # show ip
            # with TOR: print(requests.get('https://ifconfig.me', proxies=proxies).text)
            # w\o TOR: print(requests.get('https://ifconfig.me').text)
            
            link = i.strip()
            soup = self.get_soup(link)
            img = soup.find('img', class_='asset-card__image')['src']
  
            self.session = requests.Session()
            img_r = self.session.get(img, proxies=proxies)
            con = img_r.content
            title = re.search(r'photos/(\w.*)-id\d\d\d\d', img).group(0).replace('photos/', '')

            outf = open(Getty.HOME_DIR + f'{title}.jpg', "wb")
            outf.write(con)

            fotos_downloaded.write(link)
            fotos_downloaded.write('\n')

            outf.close()

            print(
                img,
                requests.get('https://ifconfig.me', proxies=proxies).text, 
                end='\n'
            )

        fotos_downloaded.close()
        links.close()




g = Getty()
# g.get_last_page()
# g.write_links()
g.download_image()
