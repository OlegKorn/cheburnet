import requests, sys, os
from bs4 import BeautifulSoup as bs
import re


headers = {'access-control-allow-origin' : '*',
           'Request Method' : 'GET',
           'Status Code' : '200',
           'Remote Address' : '64.233.163.101:443',
           'Referrer Policy' : 'no-referrer-when-downgrade',
           'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}

#page url
url = 'https://www.wikiart.org/ru/artists-by-art-movement/akademizm#!#resultType:masonry'
#home folder
ROOT = '/home/o/Изображения/ART/'

#two types of url: with '#!#' and w/o
if '#!#' in url: #with #!#
    art_movement_folder_postfix = re.search('movement/(.*)#!#', url).group(1)     #all between movements/ and #!#

if not '#!#' in url: #w/o #!#
	art_movement_folder_postfix = re.search('movement/(.*)', url).group(1)        #all between movements/ and #!#

art_movement_folder_postfix = art_movement_folder_postfix.replace('-', ' ')
print('Art movement is: ', art_movement_folder_postfix)

MOVEMENT_FOLDER = ROOT + art_movement_folder_postfix


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

            art_movement_description_file = MOVEMENT_FOLDER + '/' + art_movement_folder_postfix + '.txt'
            
            f = open(art_movement_description_file, 'w')
            f.write(descr_title)
            f.writelines(str(descr_text))

        except Exception as e:
            print(e)
            pass

        f.close()

    except Exception as e:
        print(e)
        pass


def create_artists_folders():
    try: 
        session = requests.Session()
        request = session.get(url)
        soup = bs(request.content, 'html.parser')

        for artist_name in soup.find_all('div', class_='artist-name'):
                
            artist_folder = MOVEMENT_FOLDER + '/' + artist_name.a.text.strip()

            if not os.path.exists(artist_folder):
                os.mkdir(artist_folder)

    except Exception as e:
        print(e)
        pass

    
def create_artists_descr():
    try:
        session = requests.Session()
        request = session.get(url)
        soup = bs(request.content, 'html.parser')

        for artist_name in os.listdir(MOVEMENT_FOLDER):   #list of folders of artists of the given art movement
            print(artist_name)
            artist_descr = MOVEMENT_FOLDER + '/' + artist_name + '/' + artist_name + '.txt'
            f = open(artist_descr, 'w')

    except Exception as e:
        print(e)
        pass


def write_artist_descr():
    try:
        session = requests.Session()
        request = session.get(url)
        soup = bs(request.content, 'html.parser')

        for artist in soup.find_all('div', class_='title-block'):
            artist_name = str(artist.find('div', class_='artist-name').text.strip())
            artist_descr = artist.text.strip()
            
            #creating a txt file in a folder according to the list of artists
            artist_descr_file = MOVEMENT_FOLDER + '/' + artist_name + '/' + artist_name + '.txt'
            f = open(artist_descr_file, 'w')
            f.write(artist_descr)


    except Exception as e:
        print(e)
        pass



def save_artist_image():
    try:
        session = requests.Session()
        request = session.get(url)
        soup = bs(request.content, 'html.parser')

       
        for artist in soup.find_all('div', class_='title-block'):
            artist_name = str(artist.find('div', class_='artist-name').text.strip())
            artist_descr = artist.text.strip()
            
            #creating a txt file in a folder according to the list of artists
            artist_descr_file = MOVEMENT_FOLDER + '/' + artist_name + '/' + artist_name + '.txt'
            f = open(artist_descr_file, 'w')
            f.write(artist_descr)


    except Exception as e:
        print(e)
        pass




write_artist_descr()







def save_img():
    f = open(fi1, 'r').readlines()

    for i in f:

        link_replaced = i.replace('\n', '')

        try:

            z = link_replaced[50:].replace('/', '_')

            session = requests.Session()
            request = session.get(link_replaced, headers=headers)

            print(link_replaced)
            
            r = requests.get(link_replaced, stream=True)
            image = r.raw.read()
            
            open(home+z, "wb").write(image)

        except Exception:
            pass


#create_folder()
#get_description_info_txt()








# download the url contents in binary format
#r = requests.get(url, stream=True)
#image = r.raw.read()

#print(r.status_code)

# open method to open a file on your system and write the contents
#if r.status_code == 200:

#open("/home/o/Загрузки/dd.jpg", "wb").write(image)
