

import requests, sys, os,time, shutil, time
from bs4 import BeautifulSoup as bs




URL = 'https://www.elitebabes.com/model/nastya-k/'

MODEL_NAME = URL.replace('https://www.elitebabes.com/model/', '').replace('/', '')

home = 'G:/Desktop/py/' + MODEL_NAME + '/'
fi = home + MODEL_NAME + '.txt'
fi1 = home + MODEL_NAME + '_links.txt'



def main():
    
    if not os.path.exists(home):
        os.mkdir(home, mode=0o777)

    f = open(fi, 'w')

    try: 
        session = requests.Session()
        request = session.get(URL)
        soup = bs(request.content, 'html.parser')

            #download images from every section (0,1,2,...34)
        for imgset in soup.find('ul', attrs={'gallery-a b'}).find_all('li'):
            set_link = imgset.a.get('href')
            print(set_link)
            if not "video" in set_link:
                f.write(set_link + '\n')

    except Exception as e:
        print(e)
        pass

    f.close()



def save_urls():
    
    f = open(fi, 'r')
    file = f.readlines()
    f1 = open(fi1, 'w')
    
    for img_url in file:

        img_url_replaced = img_url.replace('\n', '')

        session = requests.Session()
        request = session.get(img_url_replaced)
        soup = bs(request.content, 'html.parser')
            
        #image link
        for image in soup.find('ul', class_='list-gallery a css').find_all('li'):

            try:

                link = image.a.get('href')
                print(link)
                f1.write(link)
                f1.write('\n')

            except Exception:
                pass

        print(img_url_replaced + '\n')

    f.close()
    f1.close()



def save_img():

    f = open(fi1, 'r')
    
    for i in f:
        
        try:
        
            i = i.strip()

            _title = i.replace('/', '_')

            t_len = len(_title) - 20
            
            session = requests.Session()
            r = requests.get(i, stream=True)
            image = r.raw.read()
            print(i)
            open(home + _title[t_len:], "wb").write(image)
        
        except Exception:
            print('error')
            continue
        
        del session
        
    f.close()

main()
save_urls()
save_img()
