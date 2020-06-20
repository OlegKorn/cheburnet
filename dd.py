#/usr/bin/env python3
import requests, os, time, sys
from bs4 import BeautifulSoup as bs
import re
import shutil 


class DD:

    HOME_DIR = '/home/o/Документы/PYTHON_SCRIPTS/ero/dd/'
    urls = [
        'http://vintage-erotica-forum.com/t19047-lynne-austin.html',
        # 'http://vintage-erotica-forum.com/t948-kirsten-imrie.html'
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


    def get_last_page(self, url):
        self.get_soup(url)
        self.soup = self.get_soup(url)

        self.last_page = self.soup.find('div', class_='pagenav awn-ignore').find('td', attrs={'nowrap': 'nowrap'}).a
        self.last_page = re.search(r'page=(\d+)', self.last_page['href']).group(0).replace('page=', '')
        print(self.last_page)

        return self.last_page

    
    def write_all_pages_urls_of_model(self, url):
        f = open(DD.HOME_DIR + self.model_name + '/' + self.model_name + '.txt', 'w')
            
        self.pages_num = self.get_last_page(url)
        for i in range(1, int(self.pages_num) + 1): 
            self.url_ = url.replace(self.model_name, 'p' + str(i) + '-' + self.model_name) 
            print(self.url_)
            f.write(self.url_.strip())
            f.write('\n')

        f.close()
    

    def get_all_fotos_url_of_model(self):
        f = open(DD.HOME_DIR + self.model_name + '/' + self.model_name + '.txt', 'r')
        f2 = open(DD.HOME_DIR + self.model_name + '/' + self.model_name + '_links.txt', 'w')
        for url in f:
            regex = re.compile('.*post_message_.*')
            self.soup = self.get_soup(url)
            self.all_posts = self.soup.find_all('div', attrs={'id': regex})
            
            for i in self.all_posts:
                try:
                    print('\n\n', i['id'], end='\n')
                    a_ = i.find_all('a', attrs={'target': '_blank'})
                    if not a_ is None:
                        for i_ in a_:
                            self.im = i_['href']
                            print(self.im)
                            
                            self.soup_of_image = self.get_soup(self.im)

                            try:
                                self.foto_url = self.soup_of_image.find_all('img')

                                for img in self.foto_url:
                                    if not 'logo_resized' in img['src']:
                                        print(img['src'])
                                
                                        self.filename = img['src'][-8:]
                                        self.r = requests.get(img['src'], stream=True)

                                        if self.r.status_code == 200:
                                            self.r.raw.decode_content = True

                                            self.path = DD.HOME_DIR + self.model_name + '/' + self.filename

                                            with open(self.path,'wb') as f:
                                                shutil.copyfileobj(self.r.raw, f)
                                                time.sleep(1.5)

                            except Exception as e:
                                print(e)
                                pass
                    
                    # timer 30 sec after every post
                    for i in range(31, 0, -1):
                        sys.stdout.write(str(i) + ' ')
                        sys.stdout.flush()
                        time.sleep(1)
                            
                except TypeError:
                    pass



        f.close()
        f2.close()
    


dd = DD()

for url in DD.urls:
    dd.get_name(url)
    dd.get_last_page(url)
    dd.write_all_pages_urls_of_model(url)
    dd.get_all_fotos_url_of_model()
