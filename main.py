import requests, time
from bs4 import BeautifulSoup as bs
import webbrowser as w


###################################TESTED SECTION BEGIN
###################################TESTED SECTION BEGIN
###################################TESTED SECTION BEGIN

URL = 'https://xuk.ooo/erotic/page'
 

headers = {'access-control-allow-origin' : '*',
           'Request Method' : 'GET',
           'Status Code' : '200',
           'Remote Address' : '64.233.163.101:443',
           'Referrer Policy' : 'no-referrer-when-downgrade',
           'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}

home = '/home/o/python/ero/'
entries_links = '/home/o/python/ero/entries_links_2.txt'
file_links = []

f = open(entries_links, 'w')

def get_entries_urls(n:int):

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

    f.close()
    return entries_links

###################################TESTED SECTION END
###################################TESTED SECTION END
###################################TESTED SECTION END
       

def get_files_urls():

    for entry_url in entries_links:
        session = requests.Session()
        request = session.get(entry_url, headers=headers)
        soup = bs(request.content, 'html.parser')

        for i in soup.find_all('ul', attrs={'class':'gallery-b a'}): 
            entries = i.find_all('li')

        for entry in entries:
            file_link = entry.a.get('href')
            file_links.append(file_link)



def save():
    x = 1
    for file_link in file_links:
        try:
            print(file_link)
            filename = file_link.split('/')[-1] 
            where = home + str(x) +filename 
            r = requests.get(file_link, stream=True)
            image = r.raw.read()
            f = open(where, "wb")
            f.write(image)
            x += 1
        except:
            pass



get_entries_urls(1442)
        

# download the url contents in binary format
#r = requests.get(url, stream=True)
#image = r.raw.read()

#print(r.status_code)

# open method to open a file on your system and write the contents
#if r.status_code == 200:

#    open("/home/o/Загрузки/dd.jpg", "wb").write(image)
