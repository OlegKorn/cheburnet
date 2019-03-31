import requests, time
from bs4 import BeautifulSoup as bs


URL = 'https://xuk.ooo/erotic/page'

headers = {'access-control-allow-origin' : '*',
           'Request Method' : 'GET',
           'Status Code' : '200',
           'Remote Address' : '64.233.163.101:443',
           'Referrer Policy' : 'no-referrer-when-downgrade',
           'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}

home = '/home/o/python/ero/'
entries_links = '/home/o/python/ero/entries_links.txt' #на данном сайте 2410 страниц, примерно на 1400 произойдет ошибка

#запоминаем число, перезапускаем get_entries_urls(запомненное_число), переписываем строку 16 на entries_links_2.txt
#вторая ошибка будет на 400, делаем аналогично
#итого будет 3 файла (внизу)

files = ['/home/o/python/ero/entries_links.txt',
         '/home/o/python/ero/entries_links_2.txt',
         '/home/o/python/ero/entries_links_3.txt'
]

#f = open(entries_links, 'w')


def get_entries_urls(n:int):

    try:
        
        print(n)
        while n != 1:

            session = requests.Session()
            request = session.get(URL + str(n), headers=headers)
            soup = bs(request.content, 'html.parser')

            for i in soup.find('div', attrs={'class':'items justified'}).find_all('div', class_='photo-item'):
                link = i.a.get('href')
                f.write(link)
                f.write('\n')
            f.write('\n')
            get_entries_urls(n-1)

    except Error as e:
        print(e)
        input('Error. Let"s try to continue from {}'.format(n))
        get_entries_urls(n)

    f.close()


def save_files():

    for i in files:

            f = open(i, 'r')

            f1 = f.readlines()

            for entry_url in f1:

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

                        print(end_link.replace('\n', ''))

                        r = requests.get(end_link, stream=True)
                        image = r.raw.read()
                        open(home + end_link[60:], "wb").write(image)

                    except Exception as e:
                        print(e)
                        input('Error. Enter to continue')
                        pass


get_entries_urls(2410)

save_files()


