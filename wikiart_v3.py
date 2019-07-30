import requests, os
from bs4 import BeautifulSoup as bs
import re


#page url
SITE_ROOT = 'https://www.wikiart.org'
url = 'https://www.wikiart.org/ru/artists-by-art-movement/sotsialisticheskiy-realizm-sotsrealizm/'
ALL_ARTISTS = url + 'text-list'
ROOT_FOLDER = '/home/o/Изображения/ART/'


art_movement_folder_postfix = re.search('movement/(.*)text-list', ALL_ARTISTS).group(1)    #all between movements/ and #!#
MOVEMENT_FOLDER = ROOT_FOLDER + art_movement_folder_postfix
print('Art movement is: {}, MOVEMENT_FOLDER is {}'.format(art_movement_folder_postfix, MOVEMENT_FOLDER))



def create_folder():
    if not os.path.exists(MOVEMENT_FOLDER):
        os.mkdir(MOVEMENT_FOLDER)
        print('Folder "{}" created'.format(MOVEMENT_FOLDER))
    else: 
        print('{} already exists'.format(MOVEMENT_FOLDER))



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
                       .find_all('a') if artist_link.get('href')
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

            if 'ivan-vladimirov' in link:
                print('IV')
                pass

            else:
                print(link)
                artist_all_works = link + '/all-works/text-list'   #iterate thru artists           
                #print(artist_all_works)

                session = requests.Session()
                request = session.get(artist_all_works)
                
                #get the soup of all paints of an artist
                soup = bs(request.content, 'html.parser')
                
                try: #if Error == 'NoneType' object has no attribute 'get'
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

                        print(pre_image_name, artist, image_finish_url)

                        #WRITE IMAGES IN A FOLDER OF ARTIST
                        IMAGE_NAME = (pre_image_name + '.jpg') 
                        try:
                            r = requests.get(image_finish_url, stream=True)
                            image = r.raw.read()
                            open(MOVEMENT_FOLDER + artist + '/' + IMAGE_NAME, "wb").write(image)
                        except OSError as e:
                            print(e)
                            pre_image_name = pre_image_name[0:-80] #delete last 80 symbols

                except Exception as e:
                    print(e)
                    input('NEXT')
                    pass
                   
        #del session'''
                
    except Exception as e:
        print(e)
        


def main():
    #create_folder()
    #get_description_info_txt()
    #create_artists_folders()
    #create_artists_descr()
    #save_artist_image()
    save_images()

main()

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
