import requests
from bs4 import BeautifulSoup as bs
import re, os
from time import sleep
from progress.bar import Bar


#counter progress bar
counter = [1,2]
bar = Bar('Countdown', max = len(counter))

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

                all_items_url = 'https://reddevol.com' + theme_a['href']
                title = theme_a.text

                if '"' or ':' or ',' or '?' in title:
                    title_normalized = title.replace('"', '') \
                                            .replace(':', '') \
                                            .replace(',', '') \
                                            .replace('?', '')
                else:
                    title_normalized = theme_a.text

                # create dirs for every theme
                self.create_directory(title_normalized)

                # get all items of theme
                themes_soup = self.get_soup(all_items_url)

                # get all posts of item
                all_posts_of_theme = themes_soup.find_all('div', attrs={'class': 'ui items'})
                
                for post_of_theme in all_posts_of_theme:
                    post_of_theme_titles = post_of_theme.find_all('h2', class_='header')
                    post_of_theme_urls = post_of_theme.find_all('h2', class_='header')

                    # creating subdirs by name post_of_theme_title.text
                    # in super dir of theme
                    for post_of_theme_title in post_of_theme_titles:

                        # normalize post_of_theme_title.text
                        # ", : not allowed at for naming a dir in Win
                        if '"' or ':' or ',' or '?' in post_of_theme_title.text: 
                            post_of_theme_title_normalized = post_of_theme_title.text.replace('"', '') \
                                                                                     .replace(':', '') \
                                                                                     .replace(',', '') \
                                                                                     .replace('?', '')
                        else:
                            post_of_theme_title_normalized = post_of_theme_title.text

                        self.create_directory(title_normalized, post_of_theme_title_normalized)
                    
                    for post_of_theme_url in post_of_theme_urls:
                        # get soup of post
                        u = 'https://reddevol.com' + post_of_theme_url.a['href']
                        self.get_soup(u)

                        # data of post
                        data_ = self.get_post_data(u)
                        
                        self._write(
                            title, 
                            post_of_theme_title_normalized, 
                            data_
                        )

                        # countdown (sleep() 10 seconds)
                        for item in counter:
                            bar.next()
                            sleep(1)
                        bar.finish()


    def get_post_data(self, url):
        soup = self.get_soup(url)
        
        title = soup.find('div', class_='inner-text').h1.text
        text = soup.find('div', attrs={'class': 'thirteen wide column'}).get_text()
        text_normalized = re.sub(r'<.*?>', '', text).strip() \
                            .replace('Comments System WIDGET PACK', '') \
                            .replace('Предыдущая статья', '') \
                            .replace('Следующая статья', '') \
                            .replace('\n\n\n\n\n\n\n\n', '') \
                            .replace('\n\n\n\n\n', '')
        
        data = (title + '\n\n' + url + '\n\n' + text_normalized + '\n')
        return data


    def create_directory(self, theme='', theme_item=''):
        path_ = home + theme + '/' + theme_item
        if os.path.exists(path_):
            print(f'{path_} EXISTS')
        else:
            os.mkdir(path_)
            print(f'{path_} CREATED')


    def _write(self, theme:str, subtheme:str, data, home=home):
        f = open((home + theme + '/' + subtheme + '/' + subtheme + '.txt'), 'w', encoding='utf-8')
        f.write(data)
        f.close()

r = RDV()
# print(r.get_post_data())
#r._write('Blue Origin', 'Жизнь и смерть космического туризма', 'gsdsd')
r.get_themes()

