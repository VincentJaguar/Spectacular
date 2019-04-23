#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import os,urllib2

def download_file(url):
    local_filename = url.split('/')[-1] + ".jpeg"
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
    count=0
    for link in soup.findAll('img'):
        count+=1
        image_links = link.get('src')
        if not image_links.startswith('http'):
            image_links = url + '/' + image_links
        if count<=17:
            newpath = r'/home/nikhilkonijeti/Desktop/Proj/Spectacular/training_set/{}'.format(li) 
            if not os.path.exists(newpath):
                os.makedirs(newpath)
                os.chdir(newpath)
                download_file(image_links)
            else:
                download_file(image_links)
        elif count>17: 
            newpath1 = r'/home/nikhilkonijeti/Desktop/Proj/Spectacular/test_set/{}'.format(li) 
            if not os.path.exists(newpath1):
                os.makedirs(newpath1)
                os.chdir(newpath1)
                download_file(image_links)
            else:
                download_file(image_links)
            
list=['rawchicken','egg','rawtomato','mango','']
path1=r'/home/nikhilkonijeti/Desktop/Proj/Spectacular/training_set'
for li in list:
    os.chdir(path1)
    Download_Image_from_Web("https://www.google.co.in/search?q={}&source=lnms&tbm=isch&sa=X&ved=0ahUKEwj1xOK8sKXeAhVIWX0KHfGqA30Q_AUIDigB&biw=1317&bih=669".format(li),li)
    
#Convolutional neural networks
# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense

# Initialising the CNN
classifier = Sequential()

# Step 1 - Convolution
classifier.add(Conv2D(32, (3, 3), input_shape = (64, 64, 3), activation = 'relu'))

# Step 2 - Pooling
classifier.add(MaxPooling2D(pool_size = (2, 2)))

# Adding a second convolutional layer
classifier.add(Conv2D(32, (3, 3), activation = 'relu'))
classifier.add(MaxPooling2D(pool_size = (2, 2)))

# Step 3 - Flattening
classifier.add(Flatten())

# Step 4 - Full connection
classifier.add(Dense(units = 128, activation = 'relu'))
classifier.add(Dense(units = 64, activation = 'relu'))
classifier.add(Dense(units = 3, activation = 'softmax'))

# Compiling the CNN
classifier.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])

# Part 2 - Fitting the CNN to the images
from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1./255)
os.chdir(r'/home/nikhilkonijeti/Desktop/Proj/Spectacular/')

training_set = train_datagen.flow_from_directory('training_set',
                                                 target_size = (64, 64),
                                                 batch_size = 1,
                                                 class_mode = 'categorical')

test_set = test_datagen.flow_from_directory('test_set',
                                            target_size = (64, 64),
                                            batch_size = 1,
                                            class_mode = 'categorical')

classifier.fit_generator(training_set,
                         steps_per_epoch = 51,
                         epochs = 50,
                         validation_data = test_set,
                         validation_steps = 9)

import numpy as np
from keras.preprocessing import image
test_image = image.load_img('prediction/chicken18.jpeg', target_size = (64, 64))
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis = 0)
result = classifier.predict(test_image)
training_set.class_indices
if result[0][0] == 1:
    prediction = 'Egg'
elif result[0][1] == 1:
    prediction = 'Raw Chicken'  
else:
    prediction='tomato'
print(prediction) 
   
'''
#getting the recipe name and youtube recommendations
list = ['orange','tomato']
foc=[]
pkg=' '    
for i in list:   
    pkg = pkg + i + '%20'
url = "https://cookpad.com/us/search/recipes%20made%20using%20" + pkg
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
data = opener.open(url).read()        

soup=BeautifulSoup(data)
t=soup.find_all('span',{'data-clamp':'2'})
for link in t:
    foc.append(link.next) 
    
for i in range(0,len(foc)):
    print(foc[i])      
'''

list = ['onion','tomato']
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

recommended_url_head="https://www.allrecipes.com/recipe/228293/"
recommended_url_tail="/?clickId=right%20rail0&internalSource=rr_feed_recipe_sb&referringId=255355%20referringContentType%3Drecipe%20"

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
        break;
    print("The recommended item for " + foc[i])   
    recommended[foc[i]]=roc

#Youtube recomendation
videolist=[]    
base = "https://www.youtube.com/results?search_query="
for ingredient in foc:
	qstring = ingredient
	r = requests.get(base+qstring)
	page = r.text
	soup=BeautifulSoup(page,'html.parser')
	vids = soup.findAll('a',attrs={'class':'yt-uix-tile-link'})
	for v in vids:
	    tmp = 'https://www.youtube.com' + v['href']
	    if(len(tmp) == 43):
	    	# print(len(tmp))
	    	videolist.append(tmp)
	    if (len(videolist) == 2):
	    	break
	for i in range(2): 
		print (videolist[i])    