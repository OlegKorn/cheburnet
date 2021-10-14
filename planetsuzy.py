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
        self.soup = bs(self.request.content, 'html.parser')

        return self.soup


    def get_soup_via_TOR(self, url):
        proxies = {
            'http': 'socks5h://127.0.0.1:9150', 
            'https': 'socks5h://127.0.0.1:9150'
        }

        session = requests.Session()
        r = session.get(url, proxies=proxies)
        soup = bs(r.content, 'html.parser')
        
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

    
    def write_all_pages_urls_of_model(self, url):
        self.model_name=self.get_name(initial_url)

        f = open(HOME_DIR + self.model_name + '/' + self.model_name + '.txt', 'w')
            
        self.pages_num = self.get_last_page(url)
        self.model_name = self.get_name(url)

        for i in range(1, int(self.pages_num) + 1): 
            self.url_ = url.replace('p1', 'p' + str(i)) 
            print(self.url_)
            
            f.write(self.url_.strip())
            f.write('\n')
        f.close()
     
    '''
    def normalize(self):
        self.model_name=self.get_name(initial_url)

        f = open(HOME_DIR + self.model_name + '/' + self.model_name + '.txt', 'r')
        txt_normalized = open(HOME_DIR + self.model_name + '/' + 'normalized.txt', 'w')

        for i in f:

            if "vintage-erotica-forum" in i:
                pass
            elif "turboimagehost" in i:
                pass
            else:
                normalized = re.search('"(.*?)"', i).group(1).replace('http://', 'https://')
                txt_normalized.write(normalized + '\n')

        f.close()
        txt_normalized.close()
    '''

    def get_all_fotos_url_of_model(self):
        self.model_name=self.get_name(initial_url)

        logging.basicConfig(
            filename=f'{HOME_DIR}{self.model_name}/{self.model_name}_links.txt.log', 
            level=logging.INFO, format=FORMAT
        )

        f = open(HOME_DIR + self.model_name + '/' + self.model_name + '.txt', 'r')
        
        for url in f:
            print(url)

            regex = re.compile('.*post_message_.*')
            self.soup = self.get_soup(url)
            self.all_posts = self.soup.find_all('div', attrs={'id': regex})
            
            for i in self.all_posts:
                try:
                    print(i['id'], end='\n')
                    a_ = i.find_all('a', attrs={'target': '_blank'})
                    if not a_ is None:
                        for i_ in a_:
                            self.im = i_['href'] 
                            if 'pimpandhost' in self.im:
                                pass
                            else:
                                # getting the dinamically changed url
                                self.r = Request(self.im)
                                try:
                                    webpage = urlopen(self.r)
                                
                                    print(webpage.geturl())
                                    _ = webpage.geturl()
                                    
                                    logging.info(_)

                                except:
                                    print('ERROR')
                                    pass
                except:
                    pass
        f.close()

    '''
    def main(self, model_name = None):

        control_file = DD.HOME_DIR + self.model_name + '/' + 'control.txt'
        control_f = open(control_file, 'w')

        self.model_name = model_name

        txt_normalized = open(DD.HOME_DIR + self.model_name + '/' + 'normalized.txt', 'r')
    
        for link in txt_normalized:
            try:
                foto_post = link.strip()
                self.soup = self.get_soup(foto_post)

                if 'imagevenue' in foto_post:            
                    img = self.soup.find('img', attrs={'src': re.compile('.*imagevenue.*')})
                    if img is not None:
                        img_link = img['src']
                        print('========================')
                        print(f'post: {foto_post}')
                        print(f'img: {img_link}')
                        print('========================')
                        self.download_image(img_link)
                        self.timer(1)


                if 'imagebam' in foto_post:            
                    img = self.soup.find('img', attrs={'src': re.compile('.*imagebam.*')})
                    if img is not None:
                        img_link = img['src']
                        print('========================')
                        print(f'post: {foto_post}')
                        print(f'img: {img_link}')
                        print('========================')
                        self.download_image(img_link)
                        self.timer(1)


                if 'pimpandhost' in foto_post:            
                    img = self.soup.find('img', attrs={'src': re.compile('.*pimpandhost.*')})
                    if img is not None:
                        img_link = img['src'].replace('//ist', 'https://www.ist')
                        print('========================')
                        print(f'post: {foto_post}')
                        print(f'img: {img_link}')
                        print('========================')
                        self.download_image(img_link)
                        self.timer(1)


                if 'imgbox' in foto_post:            
                    img = self.soup.find('img', attrs={'src': re.compile('.*imgbox.*')})
                    if img is not None:
                        img_link = img['src']
                        print('========================')
                        print(f'post: {foto_post}')
                        print(f'img: {img_link}')
                        print('========================')
                        self.download_image(img_link)
                        self.timer(1)

                else:
                    pass         

                control_f.write(foto_post + '\n')
            
            except Exception as e:
                print(e)
                continue

        txt_normalized.close()
        control_f.close()


    def timer(self, number):
        for i in range(number, 0, -1):  
            sys.stdout.write(str(i) + ' ')  
            sys.stdout.flush()  
            time.sleep(1)
    

    def download_image(self, url):
        # pass thumbs of video 
        if not 'avi_' in url:
            self.filename = url[-13:]
            self.r = requests.get(url, stream=True)

            if self.r.status_code == 200:
                self.path = DD.HOME_DIR + self.model_name + '/' + self.filename

                with open(self.path,'wb') as f:
                    shutil.copyfileobj(self.r.raw, f)
                    time.sleep(1.5)
                    shutil.copyfileobj(self.r.raw, f, 50000)

    '''



ps = PlanetS()
# ps.write_all_pages_urls_of_model(initial_url)
ps.get_all_fotos_url_of_model()
