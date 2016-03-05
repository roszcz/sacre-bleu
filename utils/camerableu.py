import time
import cv2
from utils import settings as us

if us.is_debug():
    from utils import fakecam as cam
else:
    from utils import realcam as cam

def take_photos(howmany = 1, exposure = 0):
    """ Wrapper for taking multiple photos at one cron-run"""
    pictures = []
    for it in range(howmany):
        # Pictures must be distributed evenly within each minute
        if it is not 0:
            time.sleep(60/howmany)

        savepath = us.picture_path() + '/{}.png'.format(it)
        # Write pictures
        cam.take_photo(savepath)

        # Return filenames
        pictures.append(savepath)

    return pictures

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
