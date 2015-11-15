""" Analyze analyze analyze
    Decision about updateing the database
    must be done within live running methods """
import numpy as np
import cv2
import utils.common as uc

# Every function should take cv2.image to avoid 
# reading files from disk too often
def rgb_distribution(img):
    # RGB spectroscopy
    # Normalize per pixel
    norm = img.shape[0] * img.shape[1]
    b, g, r = 1.0*np.sum(np.sum(img, axis=0), axis=0)/norm

    return r, g, b

# FIXME - those are not distributions!!! or are they
def hsv_distribution(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Normalize per pixel
    norm = img.shape[0] * img.shape[1]
    h, s, v = 1.0*np.sum(np.sum(hsv, axis=0), axis=0)/norm

    return h, s, v

def three_img_diff(t0, t1, t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_and(d1, d2)


def find_movement(pic):
    # Get sorted files
    files = uc.get_files(pic[1])

    # Get file index in the directory
    # WTF with the \\ instead of / ?
    idx = files.index(pic[1] + '\\' + pic[0])

    # There must be more than 2 files to perform
    # any motion detection, otherwise no movement
    if idx < 2:
        return 0
    else:
        # Measurement is for the last image
        im0 = cv2.imread(files[idx-2])
        im1 = cv2.imread(files[idx-1])
        im2 = cv2.imread(files[idx])
        # TODO - some other monochromatization might be better
        # for the sky related research
        gr0 = cv2.cvtColor(im0, cv2.COLOR_BGR2GRAY)
        gr1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
        gr2 = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

        diff = three_img_diff(gr0, gr1, gr2)

        # Normalize per pixel
        norm = im0.shape[0] * im0.shape[1]

        score = 1.0 * diff.sum()/norm

    return score
