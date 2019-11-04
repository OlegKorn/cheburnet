import requests, os
from bs4 import BeautifulSoup as bs
import re



headers = {'access-control-allow-origin' : '*',
           'Request Method' : 'GET',
           'Status Code' : '200',
           'Remote Address' : '64.233.163.101:443',
           'Referrer Policy' : 'no-referrer-when-downgrade',
           'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}



class Downloader:

    url = 'https://www.erosberry.com/model/Nansy_A.html'
    url_root = 'https://www.erosberry.com'
    root_dir = '/home/o/Документы/LINUXOLEG/py/ero/erosberry.com/'

    model_name = re.search('model/(.*).html', url).group(1) 
    print(model_name)   
    model_dir = root_dir + model_name

    posts_file = model_name + '_posts.txt' 
    #imgs_file =  model_dir + '/' + '_imgs2.txt'


    def __init__(self):
        if not os.path.exists(Downloader.model_dir):
            os.mkdir(Downloader.model_dir)
            print('Folder "{}" created'.format(Downloader.model_dir))
        else: 
            print('{} already exists'.format(Downloader.model_dir))



    def get_request(self, x):
        self.req = requests.get(x, stream=True)
        return self.req



    def get_soup(self, url):
        self.session = requests.Session()
        self.request = self.session.get(url, headers=headers)
        self.soup = bs(self.request.content, 'html.parser')
        
        return self.soup



    def get_posts(self):
        self.f_posts = open(Downloader.posts_file, 'w')

        for post in self.soup.find('div', attrs={'girl_thumbs'}).find_all('div', attrs={'container'}):
            post_link = Downloader.url_root + post.a.get('href').strip()
            self.f_posts.write(post_link + '\n')

        self.f_posts.close()



    def get_imgs(self):

        self.f_posts = open(Downloader.posts_file, 'r')

        for post in self.f_posts:
            x = re.search('com/(.*)', post)
            marker = x.group(1)     #iveta-the-front-office-by-mpl-studios
 
            self.imgs = self.get_soup(post.strip())
                
            for i in self.imgs.find('div', id='photo').find_all('div', attrs={'container'}):
                #там в контейнерах есть другие модели. проверяем соответствие
                must_match = i.a.get('href')
                print(f'marker: {marker}, i:{must_match}')
                
                if marker in must_match:
                    img = 'http://' + i.img['src'].strip().replace('//', '')
                     
                    #скачиваем картинку
                    self.r = self.get_request(img)
                    self.image = self.r.raw.read()

                    print(Downloader.model_dir + '/' + img[44:-4].replace('/', '_') + '.jpg')
                    open(Downloader.model_dir + '/' + img[44:-4].replace('/', '_') + '.jpg', "wb").write(self.image)

            del self.imgs


          


d = Downloader()
d.get_soup(Downloader.url)
d.get_posts()
d.get_imgs()

