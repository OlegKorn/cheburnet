'''
let a = document.querySelectorAll(".post__image-link")

arr_ = []

for (i=0; i<a.length; i++) {
    link = a[i]["href"]     
    arr_.push(link)        
}

arr_
'''
from bs4 import BeautifulSoup as bs
import requests
import wget


txt = "G:/Desktop/py/нигершы/1.txt"
home = "G:/Desktop/py/нигершы/"

def save_img():
    with open(txt, 'r') as f:
        for url in f.readlines():
            url_normalized = url.split(": ")[1].replace('"', "").rstrip()   
            file_format = "." + url_normalized.split(".")[2]
            
            print(repr(url_normalized))
            
            wget.download(url_normalized, home)


save_img()
