import picamera
import time
import settings as s
import cv2

def take_photos(howmany = 1, exposure = 0):
    """ Wrapper for taking multiple photos at one cron-run"""
    pictures = []
    for it in range(howmany):
        # Pictures must be distributed evenly within each minute
        if it is not 0:
            time.sleep(60/howmany)

        # [0] - filename, [1] - filepath
        pictures.append(take_photo(exposure))

    return pictures

def take_photo(long = 0):
    """ Takes a picture, resolution and exposure can be controlled
        returns picpath and picname
    """

    # Possible resolutions
    low_hd = (1280, 720)
    full_hd = (1920, 1080)

    # Set
    resolution = full_hd

    # Date string confusion
    datestr = time.strftime(s.YMD_FORMAT)
    hourstr = time.strftime(s.HMS_FORMAT)
    # FIXME - shouldn't it be png??
    picname = datestr + '__' + hourstr + '.jpg'
    savepath= datestr

    # Picture taking
    with picamera.PiCamera() as camera:
	camera.resolution = resolution

	# Long exposure is possible
	if long is not 0:
            camera.framerate = Fraction(1,6)
            camera.shutter_speed = long * 1000000
            camera.exposure_mode = 'off'
	camera.start_preview()
	# Camera warm up
	time.sleep(2)
	savename = savepath + '/' + picname

	# Check dir existance
	if not os.path.isdir(savepath):
            os.makedirs(savepath)

	# FIXME - add ABW control
	gains = (Fraction(383, 256), Fraction(41, 32))
	camera.awb_mode = 'off'
	camera.awb_gains = gains
	camera.capture(savename)

        # Add clock for the timelapse experience
        add_cock(savename)

    return picname, savepath

def add_cock(filepath):
    """ Print clock on the image for better timelapse experience """
    img = cv2.imread(filepath)
    #print img.shape
    x = 0
    y = img.shape[0] - 16
    timestr = time.strftime('%H:%M')
    cv2.putText(img, timestr, (x,y),\
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0),\
                thickness=8)
    cv2.imwrite(filepath, img)
