#/usr/bin/env python3
import requests, sys, os,time, shutil, time
from bs4 import BeautifulSoup as bs
import webbrowser as w


urls = [
    'http://www.electbabe.com/pornstar/masha-c'
]
 

class Ebabes:
    
    headers = {
            'Request URL': 'http://www.electbabe.com',
            'Request Method': 'GET',
            'Status Code': '200', 
            'Remote Address': '173.194.221.102:80',
            'Referrer Policy': 'no-referrer-when-downgrade',
            'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }

   
    def __init__(self, url):
        self.url = url
        self.model_name = self.url.replace('http://www.electbabe.com/pornstar', '').replace('/', '')
        self.home = '/home/o/Документы/PYTHON_SCRIPTS/ero/electbabe/' + self.model_name + '/'
        
        if not os.path.exists(self.home):
            os.mkdir(self.home, mode=0o777)           
            print('Folder __{}__ created'.format(self.home))

        else: 
            print('{} already exists'.format(self.home))
	    
        self.fi = self.home + self.model_name + '.txt'
        self.fi1 = self.home + self.model_name + '_links.txt'


    def get_soup(self):
        self.session = requests.Session()
        self.request = self.session.get(self.url) #headers = Ebabes.headers)
        self.soup = bs(self.request.content, 'html.parser')
        return self.soup

        
    def get_posts(self):
        self.f = open(self.fi, 'w')
    
        try: 
            self.posts = self.soup.find('div', attrs={'id': 'pornstar'}).find_all('a', attrs={'class': 'preview'})
            for self.post in self.posts:
                self.post_link = self.post.get('href')
                print(self.post_link)
                self.f.write(self.post_link + '\n')

        except Exception as e:
            print(e)
            pass

        self.f.close() 
        
    
    def save_urls(self):

        self.f = open(self.fi, 'r')
        print(self.f)
        self.file = self.f.readlines()
        self.f1 = open(self.fi1, 'w')
        
        for self.img_url in self.file:

            self.img_url_replaced = self.img_url.replace('\n', '')
            self.session = requests.Session()
            self.request = self.session.get(self.img_url_replaced)
            self.soup = bs(self.request.content, 'html.parser')
            
            #image link
            for self.image in self.soup.find_all('img'):
                try:
                    self.link = self.image['src']
                    print(self.link)
                    self.f1.write(self.link)
                    self.f1.write('\n')

                except Exception:
                    pass

            print(self.img_url_replaced + '\n')

        self.f.close()
        self.f1.close()


    def save_img(self):

        self.f = open(self.fi1, 'r')
        for self.i in self.f:
            try:
        
                self.i = self.i.strip()
           
                self.filename = self.i.replace('/', '_')

                self.session = requests.Session()
                self.r = requests.get(self.i, stream=True)
                self.image = self.r.raw.read()
                print(self.i)
                open(self.home + self.filename, "wb").write(self.image)
        
            except Exception:
                print('error')
                continue
        
            del self.session
        
        self.f.close()




for url in urls:
    e = Ebabes(url)
    print(url)

    # если такая уже есть
    if os.listdir(e.home):
        print(f'Папка {e.home} не пустая')
        #e.get_soup()
        #e.get_posts()
        #e.save_urls()
        e.save_img()

    if not os.listdir(e.home):
        pass
        #e.get_soup()
        #e.get_posts()
        #e.save_urls()    
        #e.save_img()

