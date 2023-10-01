import requests, re
import os
import shutil
import logging
from time import sleep
import wget
import string
import random


FORMAT = '%(message)s'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
}

model = "Ульяна Ашурко"

BASE_PATH = "G:/Desktop/py/female_model/"

dir_ = BASE_PATH + model


if os.path.exists(dir_):
    print(dir_, "exists")
       
if not os.path.exists(dir_):
    os.makedirs(dir_, mode=0o777)

logging.basicConfig(
    filename= BASE_PATH + model + "/" + model + ".log",
    level=logging.INFO,
    format=FORMAT
)
         
access_token = "vk1.a.QSAIP_YL05_K3BEyuBJqeW-QLp8YIY7nTZzlOdlTWyeAdnimBHmNCBnKzJCLFwZnXQFTYPGBXXaeEJNfnZfhkljuElP_1XiekmW9gI2BpJ9dOeY6mdxuRUSMpyENcOaK89_cCjnmoyXXySIzPs2YsD2b5gD2BEyVLmZhRdzahg9odUEOHDpmBzkt6F6zsrPw"

def request_fotos():
    r = requests.post(f"https://api.vk.com/method/photos.get?owner_id=-107647545&album_id=231376753&count=500&access_token={access_token}&v=5.150")

    last_urls = re.findall('"type":"z"(.*?)type=album', r.text)
    print(len(last_urls))

    for i in last_urls:
        i = i + "type=album"
        pure_url = re.search('"url":"(.*?)alb', i).group(1).replace("\/", "/").strip() + "album"
        
        print(pure_url)
        
        logging.info(pure_url)


def id_generator(size=8, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def download():
    index = 1

    print("DOWNLOADING BEGAN...")
    f = open(BASE_PATH + model + "/" + model + ".log", "r")
    for link in f.readlines():
        title = id_generator()

        p = BASE_PATH + model + "/"
        session = requests.Session()
        r = requests.get(link, stream=True)
        image = r.raw.read()
        print(p + title, " -- foto #: ", index)
        index += 1
        open(p + "/" + title + ".jpg", "wb").write(image)


request_fotos()
download()
