import requests
from bs4 import BeautifulSoup as bs
import re, os


URL = 'https://reddevol.com/themes'

home = 'G:/Desktop/py/lj/rdvl/'
lj_text = home + 'reddevol.txt'
links_by_month = home + '_get_posts_by_theme.txt'
all_posts = home + '_all_posts.txt'



class RDV:

    def __init__(self):
        if not os.path.exists(home):
            os.mkdir(home, mode=0o777)


    def get_soup(self, url=URL):
        try: 
            session = requests.Session()
            request = session.get(url)
            soup = bs(request.content, 'html.parser')
            return soup
        except Exception as e:
            print(e)
            pass


    def get_themes(self):
        soup = self.get_soup()
        
        for theme in soup.find_all('div', attrs={'class': 'ui horizontal list'}):
            
            for theme_a in theme.find_all('a'):

                url = theme_a['href']
                title = theme_a.text

                if '"' in title:
                    title = title.replace('"', '')

                # create dirs for every theme
                self.create_directory(title)


    def get_post_data(self, url='https://reddevol.com/articles/zhizn_i_smert_kosmicheskogo_turizma'):
        soup = self.get_soup(url)
        
        title = soup.find('div', class_='inner-text').h1.text
        text = soup.find('div', attrs={'class': 'thirteen wide column'}).get_text()
        text_normalized = re.sub(r'<.*?>', '', text).strip() \
                            .replace('Comments System WIDGET PACK', '') \
                            .replace('Предыдущая статья', '') \
                            .replace('Следующая статья', '') \
                            .replace('\n\n\n\n\n\n\n\n', '') \
                            .replace('\n\n\n\n\n', '')
        
        print(title, text_normalized, sep='\n')


    def create_directory(self, theme='', theme_item=''):
        path_ = home + theme + '/' + theme_item
        if os.path.exists(path_):
            print(f'{path_} EXISTS')
        else:
            os.mkdir(path_)
            print(f'{path_} CREATED')



r = RDV()
r.get_post_data()
# r.get_themes()

