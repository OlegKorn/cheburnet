from bs4 import BeautifulSoup as bs
import requests

URLS = [
    'https://xuk.name/erotic/ekaterina-5/14648',
    'https://xuk.name/erotic/ekaterina-4/13913',
    'https://xuk.name/erotic/ekaterina-3/13614',
    'https://xuk.name/erotic/other/24636',
    'https://xuk.name/erotic/other/23314',
    'https://xuk.name/erotic/other/22894',
    'https://xuk.name/erotic/ekaterina-20/19027',
    'https://xuk.name/erotic/ekaterina-18/18444',
    'https://xuk.name/erotic/ekaterina-15/18127',
    'https://xuk.name/erotic/ekaterina-9/16345',
    'https://xuk.name/erotic/other/29263',
    'https://xuk.name/erotic/ekaterina-14/17271',
    'https://xuk.name/erotic/ekaterina-10/16751',
    'https://xuk.name/erotic/ekaterina-7/15611',
    'https://xuk.name/erotic/other/31393'
]

links = 'G:/Desktop/links.txt'
home = 'G:/Desktop/ЭКОЛОГИЯ/'


def get_links():
    for url in URLS:
        try:
            session = requests.Session()
            request = session.get(url)
            soup = bs(request.content, 'html.parser')

            for i in soup.find('div', attrs={'class':'photo-items grid tiles'}).find_all('div', class_='photo-item'):
                link = i.a.get('href')
                    
                f.write(link)
                f.write('\n')

        except Exception as e:
            print(e)
            pass

    f.close()


def save_img():
    f = open(links, 'r').readlines()
    try:
        for entry_url in f:
            session = requests.Session()
            request = session.get(entry_url.strip())
            soup = bs(request.content, 'html.parser')
            img = soup.find('img', class_='photomodel-image').get('src')
            
            print(img)
            r = requests.get(img, stream=True)
            image = r.raw.read()
            open(home + img[70:], "wb").write(image)

    except Exception:
        pass


save_img()
