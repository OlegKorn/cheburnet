from bs4 import BeautifulSoup as bs
import requests
import re
from time import sleep


url = 'https://porncoven.com/threads/56828-Carli-Banks-(USA)'
url_root = 'https://porncoven.com'

poststxt = 'G:/Desktop/py/porncoven/carli_b/posts.txt'
imgstxt = 'G:/Desktop/py/porncoven/carli_b/links.txt'
home = 'G:/Desktop/py/porncoven/carli_b/'


def get_last_page_number():
    try:
        session = requests.Session()
        request = session.get(url)
        soup = bs(request.content, 'html.parser')
        last_page = soup.find('span', attrs={'class':'first_last'}).a.get('href')
        last_page_number = int(re.search('page*\d[\d]?', last_page).group().replace('page', ''))       
    except Exception as e:
        print(e)
        pass
    return last_page_number


def get_links_of_imgs(last_page_number = get_last_page_number()): # /page2 /page3 etc
    
    f = open(imgstxt, 'w')

    for i in range(1, last_page_number + 1):
        
        if i == 1:
            print(url + '/page' + str(i))
            print('\n')
            session = requests.Session()
            request = session.get(url)     # url + '/page' + str(i)
            soup = bs(request.content, 'html.parser')
            posts = soup.find_all('div', attrs={'class':'content'})
            for post in posts:
                links = post.find_all('a')[1:]
                
                for link in links:
                    img_link = link['href']
                    print(img_link)  
                    f.write(img_link + '\n')

        else:
            print('\n')
            print(url + '/page' + str(i))
            session = requests.Session()
            request = session.get(url + '/page' + str(i))     # url + '/page' + str(i)
            soup = bs(request.content, 'html.parser')
            posts = soup.find_all('div', attrs={'class':'content'})
            for post in posts:
                links = post.find_all('a')[1:]
                
                for link in links:
                    img_link = link['href'] 
                    print(img_link)
                    f.write(img_link + '\n')
    
    f.close()





def save_img():
    with open(imgstxt, 'r') as f:
        try:
            for url in f.readlines():
                url = url.rstrip()
                print(repr(url))
                # imagebam
                if 'imagebam' in url:
                    print("'imagebam' in url")
                    session = requests.Session()  
                    # sleep(5)                  
                    request = session.get(url, verify=False)      # verify=False ----> https://stackoverflow.com/questions/23013220/max-retries-exceeded-with-url-in-requests
                    soup = bs(request.content, 'html.parser')
                    
                    img = soup.find('img', class_='image')
                    if img:
                        src = img.get('src').strip()

                        print('==============================\n')
                        print(src)
                        print('\n=============================\n')

                        session = requests.Session()
                        request = session.get(src)
                        r = requests.get(src, stream=True)
                        image = r.raw.read()
                        index = (len(src) - 15)
                        open(home + src[index:], "wb").write(image)

                    if img is None:
                        img_link = soup.find('a', title='Continue to your image').get('href')
                        request = session.get(img_link)
                        soup = bs(request.content, 'html.parser')
                        src = soup.find('img', class_='image').get('src').strip()
                        
                        print('==============================')
                        print(src)
                        print('============================')

                        r = requests.get(src, stream=True)
                        image = r.raw.read()
                        index = (len(src) - 15)
                        open(home + src[index:], "wb").write(image)

                if 'pimpandhost' in url:
                    print("'pimpandhost' in url")
                    session = requests.Session()                    
                    request = session.get(url, verify=False)      # verify=False ----> https://stackoverflow.com/questions/23013220/max-retries-exceeded-with-url-in-requests
                    soup = bs(request.content, 'html.parser')
                    img = soup.find('div', class_='img-wrapper')

                    if img:
                        src = img.find('img').get('src').replace('//ist', 'ist')
                        if '%20' in src:
                            src = src.replace('%20', ' ')

                        print('==============================')
                        print(src)
                        print('=============================')
                    
                        r = requests.get(src, stream=True)
                        image = r.raw.read()
                        index = (len(src) - 15)
                        open(home + src[index:], "wb").write(image)

                    if img is None:
                        print('problem in pimpandhost, maybe "continue to..."')
                        
                else:
                    print(url)


                #session = requests.Session()
                #request = session.get(url.strip())
                #soup = bs(request.content, 'html.parser')
                #img = soup.find('img', class_='photomodel-image').get('src')
                
                #print(img)
                #r = requests.get(img, stream=True)
                #image = r.raw.read()
                #open(home + img[70:], "wb").write(image)

        except Exception as e:
            print(e)
            pass


# get_links_of_imgs()
save_img()


'''
session = requests.Session()
request = session.get(url)
soup = bs(request.content, 'html.parser')
'''
