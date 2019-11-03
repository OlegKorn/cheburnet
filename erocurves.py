import requests, os
from bs4 import BeautifulSoup as bs
import re





class Downloader:

    '''
    как достать все: 
    инспектор кода - network - xhr
    при прокрутке появляются страницы
    только вручную наверно

    url = 'https://www.erocurves.com/models/melisa-mendiny/page/2' и тд
    https://www.erocurves.com/models/melisa-mendiny/page/3
    '''

    url = 'https://www.erocurves.com/models/melisa-mendiny/page/3'
    root_dir = '/home/o/Документы/LINUXOLEG/py/ero/erocurves/'

    model_name = re.search('models/(.*)/page/3', url).group(1) 
    print(model_name)   
    model_dir = root_dir + model_name

    posts_file = model_name + '_posts3.txt' 
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
        self.request = self.session.get(url)
        self.soup = bs(self.request.content, 'html.parser')
        
        return self.soup



    def get_posts(self):
        self.f_posts = open(Downloader.posts_file, 'w')

        for post in self.soup.find_all('div', attrs={'home_tall_box'}):
            post_link = post.a.get('href').strip()
            self.f_posts.write(post_link + '\n')

        self.f_posts.close()



    def get_imgs(self):

        self.f_posts = open(Downloader.posts_file, 'r')

        for post in self.f_posts:
            self.imgs = self.get_soup(post.strip())
            
            self.case_one_found = self.imgs.find_all('dt', attrs={'gallery-icon portrait'})
            self.case_two_found = self.imgs.find_all('div', attrs={'single_inside_content'})

            #print(f'case1:{len(self.case_one_found)}, case2:{len(self.case_two_found)}')
                            
            if len(self.case_one_found) > 0:
                print('case1')
                
                for i in self.imgs.find_all('dt', attrs={'gallery-icon portrait'}):
                    img = i.a.get('href').strip()
                    
                    #скачиваем картинку
                    self.r = self.get_request(img)
                    self.image = self.r.raw.read()
                    print(Downloader.model_dir + '/' + img[45:-4].replace('/', '_') + '.jpg')
                    open(Downloader.model_dir + '/' + img[45:-4].replace('/', '_') + '.jpg', "wb").write(self.image)

                del self.imgs

            elif len(self.case_two_found) > 0:
                print('case2')
                
                for i in self.imgs.find_all('div', attrs={'single_inside_content'}):
                    img = i.div.p.a.get('href').strip()
                    
                    #скачиваем картинку
                    self.r = self.get_request(img)
                    self.image = self.r.raw.read()
                    print(Downloader.model_dir + '/' + img[20:-4].replace('/', '_') + '.jpg')
                    open(Downloader.model_dir + '/' + img[20:-4].replace('/', '_') + '.jpg', "wb").write(self.image)

                del self.imgs




d = Downloader()
d.get_soup(Downloader.url)
d.get_posts()
d.get_imgs()

