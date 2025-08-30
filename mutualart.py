#  cd /home/oleg/Изображения/mutualart && avenv
'''
imgs = document.querySelector(".artwork-poc-container").querySelectorAll(".grid-item-container")

for (i = 0; i < imgs.length; i++) {
    link = "https://www.mutualart.com" + imgs[i].firstChild.dataset.link 
	console.log(link)
'''

from bs4 import BeautifulSoup as bs
import requests
import re, os, sys
from time import sleep
import shutil
from fake_headers import Headers
import wget
import random
import time


BASE_DIR = '/home/oleg/Изображения/mutualart/'
MIN_SIZE = 300000
artist = 'charles schwab'

def download_file(url, post_url, filename):
    resp = requests.get(url, stream=True)

    if int(resp.headers.get("Content-Length")) < MIN_SIZE:
        print("Not Downloaded: ", post_url)

    if int(resp.headers.get("Content-Length")) > MIN_SIZE:
        print("Downloaded: ", post_url)
        content = resp.content
        with open(f"{BASE_DIR}/{artist}/{filename}.jpg", 'wb') as f:
            f.write(content)


def get_soup(url):
    session = requests.Session()
        
    try:
        request = session.get(
            url, 
            headers=Headers(headers=True).generate()
        )
            
        if request.status_code != 200:
            return False
            
        soup = bs(request.content, 'html.parser')
        return soup
        
    except Exception as ex:
        return False

    
def get_img_of_a_post(url):
    s = get_soup(url)

    if not s:
        return False
        
    try:
        img = s.find('img', class_='object-fit-contain')['data-src']
        return img

    except (Exception, TypeError, AttributeError) as ex:
        return False



f = open(BASE_DIR + artist + "/1.txt", "r")
for link in f.readlines():
    post_url = link.strip()
    title = link.split('/')[4] + str(random.randint(1, 1000))
    img_url = get_img_of_a_post(post_url)

    try:
        download_file(img_url, post_url, title)
    except Exception as e:
        print(e)
        time.sleep(3)
        continue
