import requests, sys, os,time, shutil, time
from bs4 import BeautifulSoup as bs
import wget, re


URL = [
    # 'https://hq-pictures.com/index.php?cat=227'
    'https://hq-pictures.com/index.php?cat=422'
]

root = 'https://www.hq-pictures.com/'
home = 'G:/Desktop/py/hq-pictures/'


def get_albums(URL):

    try: 
        session = requests.Session()
        request = session.get(URL)
        soup = bs(request.content, 'html.parser')

        name = soup.find('td', class_='tableh1').find_all('a')[3].text

        if not os.path.exists(home + name.strip()):
            os.mkdir(home + name.strip(), mode=0o777)

        pics_txt = home + f'{name}/{name}.txt'
        f = open(pics_txt, 'w')

        # get urls of all albums
        for album in soup.find_all('tr', attrs={'class': 'tableb tableb_alternate'}):
            
            alb_links = album.find_all('a', class_='albums')
            
            for i in alb_links:

                album_link = root + i.get('href')
                print(album_link + '&page=1', end='\n\n')
                
                session = requests.Session()
                request = session.get(album_link + '&page=1')
                soup = bs(request.content, 'html.parser')

                nav = soup.find_all('td', class_='navmenu')

                # if 1 page in album - download pics
                # url of item: https://hq-pictures.com/displayimage.php?album=969&pid=243474
                # url of fullsize: https://hq-pictures.com/displayimage.php?pid=243474&fullsize=1
                if not nav:
                    print('=========')
                    print(i)
                    print('=========')

                    imgs = soup.find_all('table')[1]
                    for i in imgs.find_all('a'):
                        session = requests.Session()
                        request = session.get(album_link + f'&page={i}')
                        soup = bs(request.content, 'html.parser')
                            
                        imgs = soup.find_all('table')[1]
                        for i in imgs.find_all('a'):
                            pid = re.search('&(.*)', i['href']).group(1)
                                
                            img_link = root + 'displayimage.php?' + str(pid) + '&fullsize=1'
                            session = requests.Session()
                            request = session.get(img_link)
                            soup_ = bs(request.content, 'html.parser')

                            img_src = root + soup_.find('img')['src']
                            print(img_src)

                            f.write(img_src + '\n')

                else:
                    last_page = int(nav[-2].text)
                    
                    for i in range(1, (last_page+1)):

                        print('=========')
                        print(album_link + f'&page={i}')
                        print('=========')

                        session = requests.Session()
                        request = session.get(album_link + f'&page={i}')
                        soup = bs(request.content, 'html.parser')
                            
                        imgs = soup.find_all('table')[1]
                        for i in imgs.find_all('a'):
                            pid = re.search('&(.*)', i['href']).group(1)
                                
                            img_link = root + 'displayimage.php?' + str(pid) + '&fullsize=1'
                            session = requests.Session()
                            request = session.get(img_link)
                            soup_ = bs(request.content, 'html.parser')

                            img_src = root + soup_.find('img')['src']
                            print(img_src)
 
                            f.write(img_src + '\n')

    except Exception as e:
        print(e)
        pass

    f.close()


def downl():

    home = 'G:/Desktop/py/hq-pictures/'

    try:
        session = requests.Session()
        request = session.get(URL[0])
        soup = bs(request.content, 'html.parser')

        name = soup.find('td', class_='tableh1').find_all('a')[3].text
        pics_txt = home + f'{name}/{name}.txt'
        
        if not os.path.exists(home + name.strip()):
            os.mkdir(home + name.strip(), mode=0o777)
    
        f = open(pics_txt, 'r')
        file = f.readlines()
        
        for album_url in file:
            album_url_normalized = album_url.replace('\n', '')
            print(album_url_normalized)
            wget.download(album_url_normalized, (home + f'{name}/'))

    except Exception:
        print('error')
        pass
        
    f.close()



for i in URL:
    # get_albums(i)
    downl()
