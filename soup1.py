#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2

list = ['coffee']
foc=[]
pkg=''    
for i in list:   
    pkg = pkg + i + ','    
pkg=pkg[:-1]
    
url = "https://www.allrecipes.com/search/results/?ingIncl=" + pkg + '&sort=p'
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
data = opener.open(url).read()        

soup=BeautifulSoup(data)
t=soup.find_all('span',{'fixed-recipe-card__title-link'})
for link in t:
    foc.append(link.next)
    
for i in range(0,3):
    foc[i]=foc[i].replace(" ","-")

recommended_url_head="https://www.allrecipes.com/recipe/22233/"
recommended_url_tail="/?internalSource=hub%20recipe&referringContentType=Search"

main_url=[]
recommended={}
for i in range(0,3):
    main_url.append(recommended_url_head + foc[i] + recommended_url_tail)   
    
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
for i in range(0,3):
    roc=[]
    data = opener.open(main_url[i]).read()  
    soup=BeautifulSoup(data)
    t=soup.find("h3", {"slider-card__h3"})
    for link in t:
        roc.append(link.next)
        break
    print("The recommended item for " + foc[i])   
    recommended[foc[i]]=roc