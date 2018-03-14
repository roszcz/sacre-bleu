import os
import cv2
import time
import picamera as cam
from fractions import Fraction

def take_photo(savepath, long = 0):
    """ Takes a picture, resolution and exposure can be controlled
        returns picpath and picname
    """

    # Possible resolutions
    low_hd = (1280, 720)
    full_hd = (1920, 1080)

    # Set
    resolution = full_hd

    # Picture taking
    with cam.PiCamera() as camera:
	camera.resolution = resolution

	# Long exposure is possible
	if long is not 0:
            camera.framerate = Fraction(1,6)
            camera.shutter_speed = long * 1000000
            camera.exposure_mode = 'off'
	camera.start_preview()
	# Camera warm up
	time.sleep(2)

	# FIXME - add ABW control
	gains = (Fraction(383, 256), Fraction(41, 32))
	camera.awb_mode = 'off'
	camera.awb_gains = gains
	camera.capture(savepath)

    return True

class PhotoTaker(object):
    def take_picture(self, long = 0):
	""" Takes a picture, resolution and exposure can be controlled
	    returns picpath and picname
	"""

	# Possible resolutions
	low_hd = (1280, 720)
	full_hd = (1920, 1080)

	# Set
	resolution = low_hd

	# Picture taking
	with cam.PiCamera() as camera:
	    camera.rotation = 90
	    camera.resolution = resolution

	    # Long exposure is possible
	    if long is not 0:
		camera.framerate = Fraction(1,6)
		camera.shutter_speed = long * 1000000
		camera.exposure_mode = 'off'
	    camera.start_preview()
	    # Camera warm up
	    time.sleep(2)

	    # FIXME - add ABW control
	    gains = (Fraction(383, 256), Fraction(41, 32))
	    camera.awb_mode = 'off'
	    camera.awb_gains = gains
	    savepath = 'tmp.png'
	    camera.capture(savepath)
	    img = cv2.imread(savepath)

	    out = img.tolist()

	print img.shape

	return out

    def __enter__(self):
	return self

    def __exit__(self, exception_type, exception_value, traceback):
	print("in __exit__")
