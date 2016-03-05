import numpy as np
import cv2 as cv

def take_photo(savepath, long = 0):
    """ Fake picture generation """
    # Possible resolutions
    low_hd = (128, 72)
    full_hd = (108, 192)

    # Set
    resolution = full_hd

    pic = 256 * np.random.random(resolution)
    pic = cv.resize(pic, (0,0), fx=10, fy=10)
    cv.imwrite(savepath, pic)

    return True
