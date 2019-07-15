import requests, sys
from bs4 import BeautifulSoup as bs


headers = {'access-control-allow-origin' : '*',
           'Request Method' : 'GET',
           'Status Code' : '200',
           'Remote Address' : '64.233.163.101:443',
           'Referrer Policy' : 'no-referrer-when-downgrade',
           'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}

pre_link = 'https://www.imagefap.com'

home = '/home/o/Изображения/ludm/'
fi = '/home/o/Изображения/ludm/ludm.txt'
fi1 = '/home/o/Изображения/ludm/ludm_links.txt'

stop = 35
n = 0

def main(n:int):

    f = open(fi, 'w')

    while n != stop:
        try: 
            url = 'https://www.imagefap.com/pictures/5537550/Russian-teen-Ludmila?gid=5537550&page=' + str(n) + 'view=0'

            print(url)

            session = requests.Session()
            request = session.get(url, headers=headers)
            soup = bs(request.content, 'html.parser')

            #download images from every section (0,1,2,...34)
            for image in soup.find('div', attrs={'class':'expp-container', 'id':'gallery'}).find_all('td', attrs={'align':'center','style':'width:240px;height:190px;padding:2px 0;'}):
                link = pre_link + image.a.get('href')
                f.write(link)
                f.write('\n')

        except Exception as e:
            print(e)
            pass

        n += 1

    f.close()
        


def save_urls():
    
    f = open(fi, 'r').readlines()
    f1 = open(fi1, 'w')
    
    try:
        
        for img_url in f:

            session = requests.Session()
            request = session.get(img_url, headers=headers)
            soup = bs(request.content, 'html.parser')
            
            img = soup.find('img', attrs={'id':'mainPhoto'}).get('src')
            print(img)
            f1.write(img)
            f1.write('\n')



    except Exception:
        pass

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


#main(0)
save_img()











# download the url contents in binary format
#r = requests.get(url, stream=True)
#image = r.raw.read()

#print(r.status_code)

# open method to open a file on your system and write the contents
#if r.status_code == 200:

#open("/home/o/Загрузки/dd.jpg", "wb").write(image)
