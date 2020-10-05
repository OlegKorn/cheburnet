import requests, os, time, re
from bs4 import BeautifulSoup as bs

URL = 'https://nude-gals.com/model_page.php?model_id=586'

class NG:

    def __init__(self):
        soup = self.get_soup(URL)

        self.name = soup.find_all('span', attrs={'itemprop': 'name'})[2].text \
                        .replace(' ', '_')
        print(self.name)

        self.home = 'G:/Desktop/py/nudegals/' + self.name + '/'
        if not os.path.exists(self.home):
            os.mkdir(self.home, mode=0o777)

        self.all_posts_txt = self.home + self.name + '_all_posts.txt'
        self.all_fotos_txt = self.home + self.name + '_all_fotos.txt'


    def get_soup(self, url):
        try: 
            session = requests.Session()
            request = session.get(url)
            soup = bs(request.content, 'html.parser')
            
            return soup
        
        except Exception as e:
            print(e)
            pass


    def get_last_page(self):
        self.last_page_href = self.get_soup(URL) \
                             .find('a', attrs={'class': 'number btn btn-inverse last btn-md'})['href']
        
        self.last_page = re.search(('(?<=&pp=)(.*)'), self.last_page_href).group()
        return self.last_page


    def get_all_posts(self):
        f = open(self.all_posts_txt, 'w')

        for i in range(1, int(self.get_last_page())+1):
            url = URL + '&pp=' + str(i)
            self.soup = self.get_soup(url) 

            self.posts = self.soup.find('div', attrs={'id': 'galleries', 'class': 'tab-pane'}) \
                                  .find_all('div', attrs={'class': 'col-lg-3 col-md-3 col-sm-3 col-xs-6 text-center'})

            for elem in self.posts:
                self.link = 'https://nude-gals.com/' + elem.a['href']
                print(self.link)

                f.write(self.link)
                f.write('\n')  

        f.close()


    def get_all_fotos(self):
        posts = open(self.all_posts_txt, 'r')
        fotos = open(self.all_fotos_txt, 'w')
 
        for post in posts:
            url_normalized = post.strip() 
            self.soup = self.get_soup(url_normalized)

            self.fotos = self.soup.find('div', class_='row row_margintop') \
                                  .find('div', class_='col-lg-12') \
                                  .find_all('img')

            for img in self.fotos:
                img = 'https://nude-gals.com/' + (img['src'].replace('thumbs/th_', ''))
                print(img)

                fotos.write(img)
                fotos.write('\n')

        posts.close()
        fotos.close()


    def save_images(self):
        fotos = open(self.all_fotos_txt, 'r').readlines()
        
        for img in fotos:
            url_normalized = img.strip() 
            print(url_normalized)
            # img_title = re.search('\d\d\_\d\d\_\d\d_(.*)', url_normalized).group(1)
            
            r = requests.get(url_normalized, stream=True)
            image = r.raw.read()
            
            image_title = url_normalized[len(url_normalized)-15:len(url_normalized)]

            if '\\' or '/' in image_title:
                image_title = image_title.replace('/', '_').replace('\\', '_')

            open(self.home + image_title, "wb").write(image)



ng = NG()
# ng.get_all_fotos()
ng.save_images()
