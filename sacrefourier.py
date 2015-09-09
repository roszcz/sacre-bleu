import numpy as np
import cv2
import glob
import os
from sacrecommon import post_to_wall


foldername = '2015_09_09'
files = glob.glob(foldername + '/*jpg')

# Read last file
img = cv2.imread(files[-1])
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

f = np.fft.fft2(gray)
fshift = np.fft.fftshift(f)

rows, cols = gray.shape
crow,ccol = rows/2 , cols/2

# remove the low frequencies by masking with a rectangular 
# window of size 2h x 2h
h = 10
fshift[crow-h : crow+h, ccol-h : ccol+h] = 0

# shift back (we shifted the center before)
f_ishift = np.fft.ifftshift(fshift)

# inverse fft to get the image back 
filtered = np.fft.ifft2(f_ishift)

filtered = np.abs(filtered)

# Convert gray to rgb so you can ..
#filtered_c = cv2.cvtColor(filtered, cv2.COLOR_GRAY2BGR)
# Joint two images
vis = np.concatenate((gray, filtered), axis=0)

# Save on hdd
savepath = 'dupa.png'
cv2.imwrite(savepath, vis)

post_to_wall(savepath, 'high pass filter and original image')
os.remove(savepath)
