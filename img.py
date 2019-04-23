#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import os

def download_file(url):
    local_filename = url.split('/')[-1]
    print("Downloading {} ---> {}".format(url, local_filename))
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    return local_filename

def Download_Image_from_Web(url,li):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    for link in soup.findAll('img'):
        image_links = link.get('src')
        if not image_links.startswith('http'):
            image_links = url + '/' + image_links
        newpath = r'/home/nikhilkonijeti/Desktop/Proj/Spectacular/{}'.format(li) 
        if not os.path.exists(newpath):
            os.makedirs(newpath)
            os.chdir(newpath)
            download_file(image_links)
        else:
            download_file(image_links)
    
list=['rawchicken','egg','rawtomato']
path1=r'/home/nikhilkonijeti/Desktop/Proj/Spectacular'
for li in list:
    os.chdir(path1)
    Download_Image_from_Web("https://www.google.co.in/search?q={}&source=lnms&tbm=isch&sa=X&ved=0ahUKEwj1xOK8sKXeAhVIWX0KHfGqA30Q_AUIDigB&biw=1317&bih=669".format(li),li)

    