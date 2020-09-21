import requests, os
import wget
from bs4 import BeautifulSoup as bs


'''
import requests, os

url = 'https://c.xme.net/11c404670.jpg'
url2 = 'https://jjgirls.com/photo/breath-takers/claudia/flexion/full/FHG_big_0008.jpg'
home = 'G:/Desktop/py/hq/Claudia/'

session = requests.Session()
r = requests.get(url2, stream=True)
image = r.raw.read()
print(url2)
open(home + '1.jpg', "wb").write(image)
'''

URL = 'https://www.hqbabes.com/babes/Claudia/'

MODEL_NAME = URL.replace('https://www.hqbabes.com/babes/', '').replace('/', '')

home = 'G:/Desktop/py/hq/' + MODEL_NAME + '/'
fi = home + MODEL_NAME + '.txt'
fi1 = home + MODEL_NAME + '_links.txt'


def main():
    
    if not os.path.exists(home):
        os.mkdir(home, mode=0o777)

    f = open(fi, 'w')

    try: 
        session = requests.Session()
        request = session.get(URL)
        soup = bs(request.content, 'html.parser').encode('utf-8')

        for imgset in soup.find('ul', attrs={'set babe'}).find_all('li'):
            set_link = imgset.find_all('a')
            
            for i in set_link:
                if not '/babes/' in i['href']:
                    _ = 'https://www.hqbabes.com' + i['href']
                    print(_)
                    f.write(_ + '\n')

    except Exception as e:
        print(e)
        pass

    #f.close()


def save_urls():
    
    f = open(fi, 'r')
    file = f.readlines()
    #f1 = open(fi1, 'w')
    
    for img_url in file:

        img_url_replaced = img_url.strip()

        session = requests.Session()
        request = session.get(img_url_replaced)
        soup = bs(request.content, 'html.parser')
        print(soup.original_encoding)
            
        for image in soup.find('ul', attrs={'class': 'set gallery'}) \
                         .find_all('li', attrs={'class': 'item i'}):
            try:
                link = ('https:' + image.a['href'])
                print(link)
                f1.write(link + '\n')

            except Exception:
                pass

    #f.close()
    #f1.close()


def save_img():
    f = open(fi1, 'r')
    
    for i in f:        
        try:
            i = i.strip()

            print(i)
            wget.download(i, home)

        except Exception:
            print('error')
            continue

    f.close()

# main()
#save_urls()
save_img()


