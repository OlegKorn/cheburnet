import requests, os
from bs4 import BeautifulSoup as bs
import re




class Downloader:

    url = 'https://www.erocurves.com/models/melisa-mendiny/'
    root_dir = '/home/o/Документы/LINUXOLEG/py/ero/erocurves/'

    model_name = re.search('models/(.*)/', url).group(1)    
    model_dir = root_dir + model_name

    posts_file = model_dir + '_posts.txt' 
    imgs_file =  model_dir  + '_imgs.txt'


    def __init__(self):
        if not os.path.exists(Downloader.model_dir):
            os.mkdir(model_dir)
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
        self.f_imgs = open(Downloader.imgs_file, 'w')

        for post in self.f_posts:
            self.imgs = self.get_soup(post.strip())
            
            for i in self.imgs.find_all('dt', attrs={'gallery-icon portrait'}):
                img = i.a.get('href').strip()
                
                #скачиваем картинку
                self.r = self.get_request(img)
                self.image = self.r.raw.read()
                print(Downloader.model_dir + '/' + img[45:-4].replace('/', '_') + '.jpg')
                open(Downloader.model_dir + '/' + img[45:-4].replace('/', '_') + '.jpg', "wb").write(self.image)

            del self.imgs



d = Downloader()
#d.get_soup(Downloader.url)
#d.get_posts()
d.get_imgs()
#d.get_all_img()



def get_description_info_txt():
    #description of the given branch of art
    try: 
        session = requests.Session()
        request = session.get(url)
        soup = bs(request.content, 'html.parser')

        try:
            descr_title = soup.find('div', class_='title').text.replace('направление', '').replace('\n', '').strip()
            descr_text = soup.find('p', class_='dictionary-description-text').text
                        
            art_movement_description_file = MOVEMENT_FOLDER + '/' + art_movement_folder_postfix.replace('/', '') + '.txt'
            
            f = open(art_movement_description_file, 'w')
            f.write(descr_title)
            f.writelines(str(descr_text))

        except AttributeError as e:
            print(e)
            pass

        f.close()

    except Exception as e:
        print(e)
        pass




def create_artists_folders():
    try: 
        session = requests.Session()
        request = session.get(ALL_ARTISTS)
        soup = bs(request.content, 'html.parser')
        artist_names = soup.find('div', class_='masonry-text-view masonry-text-view-all')

        for link in artist_names.find_all('a'):
            artist_name = link.text
            artist_link = SITE_ROOT + link['href']
            
            artist_folder = MOVEMENT_FOLDER + '/' + artist_name.strip()

            if not os.path.exists(artist_folder):
                os.mkdir(artist_folder)

    except Exception as e:
        print(e)
        pass




def create_artists_descr():
    try:
        session = requests.Session()
        request = session.get(ALL_ARTISTS)
        soup = bs(request.content, 'html.parser')

        artist_links = [SITE_ROOT + artist_link.get('href') for artist_link in soup
                       .find('div', class_='masonry-text-view masonry-text-view-all')
                       .find_all('a')
        ]

        artist_descr_files = [MOVEMENT_FOLDER + artist_name.text + '/' + artist_name.text + '.txt' for artist_name in soup
                             .find('div', class_='masonry-text-view masonry-text-view-all')
                             .find_all('a')
        ]
        
        #create a list like [artist =_link : artist_file]
        artists_links_and_descr_files = list(zip(artist_links, artist_descr_files))

        for i, j in enumerate(artists_links_and_descr_files):
            artist_link = j[0]
            artist_file = j[1]

            #grab the info of every artist
            session = requests.Session()
            request = session.get(artist_link)
            soup = bs(request.content, 'html.parser')

            try:
                artist_info = soup.find('div', class_='wiki-layout-artist-info').text.strip().replace('Подробнее:', '')
                print('Writing to {}'.format(artist_file))
                
                with open(artist_file, 'w') as f:
                    f.write(artist_info)
                print('Done\n')

            except AttributeError as e:
                print(e)
                pass

        del session

    except Exception as e:
        print(e)
        pass      





def save_artist_image():

    try:
        session = requests.Session()
        request = session.get(ALL_ARTISTS)
        soup = bs(request.content, 'html.parser')

        artist_links = [SITE_ROOT + artist_link.get('href') for artist_link in soup
                       .find('div', class_='masonry-text-view masonry-text-view-all')
                       .find_all('a') 
        ]

        for link in artist_links:
            session = requests.Session()
            request = session.get(link)
            soup = bs(request.content, 'html.parser')
            
            artist_name = soup.find('div', class_='wiki-layout-artist-info').article.h3.text.strip()
            artist_img = soup.find('div', class_='wiki-layout-artist-image-wrapper').img['src'].strip()

            if '!Portrait.jpg' in artist_img:
                artist_img = artist_img.replace('!Portrait.jpg', '')
            
            print(artist_name, artist_img)

            session = requests.Session()
            #переходим по картинам
            request = session.get(artist_img)
            soup = bs(request.content, 'html.parser')
            r = requests.get(artist_img, stream=True)
            image = r.raw.read()
            open(MOVEMENT_FOLDER + '/' + artist_name + '/' + artist_name.replace('/', '') + '.jpg', "wb").write(image)

        del session

    except Exception as e:
        print(e)
        pass



def save_images():

    try:
        session = requests.Session()
        request = session.get(ALL_ARTISTS)
        soup = bs(request.content, 'html.parser')

        artist_links = [SITE_ROOT + artist_link.get('href') for artist_link in soup
                       .find('div', class_='masonry-text-view masonry-text-view-all')
                       .find_all('a') 
        ]

        for link in artist_links:

            artist_all_works = link + '/all-works/text-list'   #iterate thru artists           
            #print(artist_all_works)

            session = requests.Session()
            request = session.get(artist_all_works)
            
            #get the soup of all paints of an artist
            soup = bs(request.content, 'html.parser')

            artist_works_img_urls = [artist_works_img_url.a.get('href') for artist_works_img_url in soup.find_all('li', class_='painting-list-text-row')]
            artist_works_img_title = [artist_works_img_title.a.text for artist_works_img_title in soup.find_all('li', class_='painting-list-text-row')]

            img_titles = list(zip(artist_works_img_urls, artist_works_img_title))

            for i,j in enumerate(img_titles):
                given_artist_image_url = SITE_ROOT + str(j[0])
                given_artist_image_title = str(j[1])

                session = requests.Session()
                request = session.get(given_artist_image_url)
            
                #get the soup of every paint of an artist
                soup = bs(request.content, 'html.parser')

                pre_image_name = soup.find('div', class_='wiki-layout-artist-info wiki-layout-artwork-info').article.h3.text.strip()
                artist = soup.find('div', class_='wiki-layout-artist-info wiki-layout-artwork-info').article.h5.span.text.strip()
                image_finish_url = soup.find('div', class_='wiki-layout-artist-image-wrapper').img['src'].strip().replace('!Large.jpg', '')


 #######################################################################
                if 'camille-pissarro' in image_finish_url:
                    print(link, 'PISSARO NOT NEEDED')
                    pass
########################################################################
                
                if not 'camille-pissarro' in image_finish_url:
                    print(pre_image_name, artist, image_finish_url)

                    #WRITE IMAGES IN A FOLDER OF ARTIST
                    IMAGE_NAME = (pre_image_name + '.jpg') 
                    try:
                        r = requests.get(image_finish_url, stream=True)
                        image = r.raw.read()
                        open(MOVEMENT_FOLDER + artist + '/' + IMAGE_NAME, "wb").write(image)
                    except OSError as e:
                        print(e)
                        pre_image_name = pre_image_name[0:-80] #delete last 50 symbols

                
                   
        #del session
                
    except Exception as e:
        print(e)
        


def main():
    create_folder()
    get_description_info_txt()
    create_artists_folders()
    create_artists_descr()
    save_artist_image()
    save_images()

#main()

#write_artist_descr()


#create_folder()
#get_description_info_txt()


# download the url contents in binary format
#r = requests.get(url, stream=True)
#image = r.raw.read()

#print(r.status_code)

# open method to open a file on your system and write the contents
#if r.status_code == 200:

#open("/home/o/Загрузки/dd.jpg", "wb").write(image)
