import requests, sys
from bs4 import BeautifulSoup as bs


URL = 'https://xuk.ooo/erotic/blonde/page'

headers = {'access-control-allow-origin' : '*',
           'Request Method' : 'GET',
           'Status Code' : '200',
           'Remote Address' : '64.233.163.101:443',
           'Referrer Policy' : 'no-referrer-when-downgrade',
           'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}

home = '/home/o/python/ero/blond10_22/'

bl = '/home/o/python/ero/blond10_22/blond10_22.txt'

stop = 22

#f = open(bl, 'w')

def get_entries_urls(n:int):
    
    try:
        if n == stop:
            f.close()
            sys.exit()

        print(n)

        session = requests.Session()
        request = session.get(URL + str(n), headers=headers)
        soup = bs(request.content, 'html.parser')

        for i in soup.find('div', attrs={'class':'items justified'}).find_all('div', class_='photo-item'):
            link = i.a.get('href')
               
            f.write(link)
            f.write('\n')
        get_entries_urls(n+1)

    except Exception as e:
        print(e)
        pass

    f.close()



def save():
    
    f = open(bl, 'r').readlines()
    
    try:
        
        for entry_url in f:
            session = requests.Session()
            request = session.get(entry_url, headers=headers)
            soup = bs(request.content, 'html.parser')
            for img in soup.find('div', id='items-container').find_all('div', class_='photo-item'): 
                try:
                    img_prelink = img.a.get('href')
                    session = requests.Session()
                    request = session.get(img_prelink, headers=headers)
                    img_soup = bs(request.content, 'html.parser')
                    img_link = img_soup.find('div', class_='photo-info')
                    end_link = img_link.a.get('href')
                    print(end_link)
                    r = requests.get(end_link, stream=True)
                    image = r.raw.read()
                    open(home + end_link[60:], "wb").write(image)
                except Exception:
                    pass

    except Exception:
        pass

#get_entries_urls(10)
save()










# download the url contents in binary format
#r = requests.get(url, stream=True)
#image = r.raw.read()

#print(r.status_code)

# open method to open a file on your system and write the contents
#if r.status_code == 200:

#open("/home/o/Загрузки/dd.jpg", "wb").write(image)
