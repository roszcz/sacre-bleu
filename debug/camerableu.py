""" Fake picamera methods for developement without
    actual RPI dedicated camera"""

import os
import time
import glob
import numpy as np
import cv2
import settings as s

def take_photos(howmany = 1, exposure = 0):
    print 'Fake photos are being taken'
    pictures = []
    for it in range(howmany):
        pictures.append(take_photo(exposure))
        time.sleep(1)

    return pictures

def take_photo(long = 0):
    # For now just generate a random image with requiered
    # size and name, TODO - for image processing think about
    # using photos from local storage

    resolution = [1080, 1920, 3]

    # Date string confusion
    datestr = time.strftime(s.YMD_FORMAT)
    hourstr = time.strftime(s.HMS_FORMAT)
    # FIXME - shouldn't it be png??
    picname = datestr + '__' + hourstr + '.jpg'
    savepath= datestr
    savename = savepath + '/' + picname

    # Create date directory if doesn't exist
    if not os.path.exists(savepath):
        os.makedirs(savepath)

    # Generate rgb noise
    random_picture = np.random.random(resolution)

    # Renormalize
    random_picture *= 256

    # Add some trace information
    print 'Fake photo in:', savename
    print 'With shape:', random_picture.shape

    # Save to disk
    cv2.imwrite(savename, random_picture)

    return picname, savepath
