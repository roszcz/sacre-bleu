#!/usr/bin/python
""" ignorance is hell """
_DEBUG = True

import os
import datetime
import time
import cv2
import pickledb
import glob
import numpy as np
if not _DEBUG:
    from sacrecommon import take_photo

# Set number of photos taken per minute
_sampling_rate = 2

if _DEBUG:
    # Overload tak photo to read pictures from a directory
    def take_photos(exposure):
        files = glob.glob('imgs/*.jpg')
        pictures = []
        # Put 2 first pictures from some directory into
        # pictures container
        for it in range(_sampling_rate):
            pictures.append([os.path.split(files[it])[1],
                            files[it]])

        return pictures
else:
    # Real photoshoot
    def take_photos(exposure):
        pictures = []
        for it in range(_sampling_rate):
            # Don't wait before the first picture
            if it is not 0:
                time.sleep(_pic_time_distance)
            # Click
            pictures.append(take_photo(exposure))

        return pictures


# Prepare time markers
_current_time = time.localtime()
_c_minute = _current_time.tm_min
_c_hour   = _current_time.tm_hour

# Today's directory
_dirname = time.strftime("%Y_%m_%d", _current_time)

# Begin with taking 2 photos
# TODO - some different mechanism will be
# required for live monitoring

# Set exposure time (0 - automatic)
_exposure_time = 0
_pic_time_distance = 27

# Prepare hours to post photo
_pic_post_hours = [(4,20),
                   (7,20),
                   (10,20),
                   (13,20),
                   (16,20),
                   (19,20)]

# Post sunrise photos
_sunrise_hour = (6,0)

# TODO make this dependent of calendar info
_db_file = 'db.pickle'
def update_database(key, value):
    print key, value
    # bool argument seems to turn autodumping on/off WHAT
    db = pickledb.load(_db_file, False)
    # Load saved data ...
    loaded = db.get(key)
    # and insert new value
    if loaded is not None:
        loaded.append(value)
    else:
        # or create if it's the first record
        loaded = []
        loaded.append(value)
    # then save,
    db.set(key, loaded)
    # and dump onto harddrive
    db.dump()

def analyze_picture(pic):
    # pic[0] = picname, pic[1] = picpath
    # Get time from os.timestamp (easier than from filename)
    # calc values
    fullpath = pic[1] + '/' + pic[0]
    t = os.path.getmtime(fullpath)
    time = datetime.datetime.fromtimestamp(t)
    img = cv2.imread(fullpath)
    # Basic color analysis may easily be performed here
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Brightness
    brightness = hsv[:,:,2].sum();
    update_database('brightness', brightness)

    # RGB spectroscopy
    b, g, r = np.sum(np.sum(img, axis=0), axis=0)
    update_database('rgb', [r, g, b])

    # Same for movement somehow
    # TODO : we get one file info in this function,
    # but for dynamical analysis we need at least two
    return True

if __name__ == '__main__':
    # Container for pic names [0] - picname, [1] - picpath (just dir)
    pictures = take_photos(0)

    # Perform a shitload of datascience
    for pic in pictures:
        analyze_picture(pic)

    # Begin cronjobish definitions
    if not _DEBUG:
        # Maybe post picture
        if _pic_post_hours.count((_c_hour, _c_minute)) is not 0:
            post_to_album(pictures[0])

    # TODO this will be replaced by live data acquisition
    # instead of calculating everything just before posting
    if _sunrise_hour[0] == _c_hour:
        # Plot some time after actual sunrise
        if _sunrise_hour[1] == _c_minute + 30:
            plotname = rgb_plot(dirname)
            post_to_wall(plotname, 'wschod')
            os.remove(plotname)
        # Plot HSV sunrise also, but later
        if _sunrise_hour[1] == _c_minute + 33:
            plotname = hsv_plot(dirname)
            post_to_wall(plotname, 'wschod')
            os.remove(plotname)
