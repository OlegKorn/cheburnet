from bs4 import BeautifulSoup as bs
import requests
import re, os, sys
from time import sleep
from fake_headers import Headers
import time
import os
from pathlib import Path
import random


BASE_DIR = '/home/oleg/Изображения/mutualart'
MIN_SIZE = 300000
artist = 'charles schwab'


def download_file(resp, post_url, filename):
    content = resp.content
    with open(f"{BASE_DIR}/{artist}/{filename}.jpg", 'wb') as f:
        f.write(content)


def get_soup(url):
    session = requests.Session()
    try:
        cookie_url = url.replace("https://www.mutualart.com", '')

        cookies = {
            "__stripe_mid": "0f339cc9-8321-4b4e-9b4d-f3d84e1165f93853da",
            "__stripe_sid": "f47af7ab-6c55-4088-8abd-fd11560a78ba5e5887",
            "_uetsid": "220ff4a0856011f0901ab73b3c8a477d",
            "_uetvid": "84433ab0815f11f0a4e893cbda3182cd",
            ".ASPXFORMSAUTH": "6C0E4F1D979DDBD54DA9F4E966C88D9ABA7C439C34F333FF6950F0D18068AC3E40FDB5706B58003722EFCB147AFFA784FAA05044E6179F2E0419D9CB4E69C1A33955F1DA2B466FFD1EA778F957060EEB4D4983525DFF4BFBE2719EE7A44C7F9D5C2EDC2B385963DAFDAD92B3C24DAFD9D27FBA97",
            "AB": "0",
            "AfterRegUrl": "https://www.mutualart.com/Artist/Franz-von-Bayros/A0F00FC72FF99AFE/Artworks",
            "IdLocation": "64391250CC1B0CE3,20885A208DF41B60",
            "RArtistsForIdleUser": "1756095488",
            "RedirectUrl": "/Artwork/Das-Zelt--Part-I-and-II--Amsler---Ruthar/88CFDC665E9FECF8",
            "sc": "1",
            "Session": "16417c32-a606-46e7-bab2-0bd8444ad5aa",
            "t": "w",
            "u": "707E37CBF0AF7219",
            "UserGuid": "ed0718a0-a170-4632-90cd-1b90d0c0b646",
            "vd": "c5822c772a4168900260e44e3410a43c"
        }

        request = session.get(
            url, 
            headers=Headers(headers=True).generate(),
            cookies=cookies
        )

        if request.status_code != 200:
            return False
            
        soup = bs(request.content, 'html.parser')
        return soup
        
    except Exception as ex:
        print("soup : ", ex)
        return False


def file_exists(filename):
    return Path(filename + '.jpg').is_file()

    
def get_img_of_a_post(url):
    sleep(random.randint(1, 4))
    s = get_soup(url)
    # print(s)
    if not s:
        return False
        
    try:
        img = s.find('img', class_='object-fit-contain')['data-src']
        return img

    except (Exception, TypeError, AttributeError) as ex:
        print("get_img_of_a_post : ", ex)
        return False


with open(f"{BASE_DIR}/{artist}/1.txt", "r") as f:
    cock = f.readlines()
    for link in cock:
        post_url = link.strip()

        title = link.split('/')[4].lower()
        img_url = get_img_of_a_post(post_url)

        try:
            resp = requests.get(img_url, stream=True)
        except Exception:
            print(f"No image at {post_url.replace('https://www.mutualart.com/', '')}...")
            time.sleep(3)
            continue

        if not file_exists(title):
            print(f"{post_url.replace('https://www.mutualart.com/', '')}.jpg didn't exist, downloaded")
            download_file(resp, img_url, title)

        else:
            size_of_existing_file = os.path.getsize(f"{BASE_DIR}/{artist}/{title}.jpg")
            if int(resp.headers.get("Content-Length")) < size_of_existing_file:
                print(f"{post_url.replace('https://www.mutualart.com/', '')}.jpg exists in {BASE_DIR}/{artist}, wont be overwritten")
            else:
                print(f"{post_url.replace('https://www.mutualart.com/', '')}.jpg exists in {BASE_DIR}/{artist}, overwritten by {title}")
                download_file(resp, img_url, title) 
                    




