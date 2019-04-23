#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 12:41:52 2018

@author: nikhilkonijeti
"""

from skimage import io, img_as_float
import matplotlib.image as mpimg
import os
import pandas as pd
import numpy as np

def load_images(n):
    images = []
    data = []
    for dirs in n:
        for filename in os.listdir(dirs):
            img = mpimg.imread(os.path.join(dirs, filename))
            img = img_as_float(img)
            if img is not None:
                images.append(img)
            if(np.mean(img) < 0.1):
                print filename
                data.append((dirs, filename))
                df = pd.DataFrame(data, columns=['Folder', 'File'])
    return df

from glob import glob
folder = glob("/home/nikhilkonijeti/Desktop/Proj/Spectacular/training_set")
df = load_images(folder)