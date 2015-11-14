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
import settings as s
from datascience import analysis as anal # trolololo

# Modules like picamera make sense only on rpi
# and for developement purposes we emulate them here
if not _DEBUG:
    from utils.camerableu import take_photos
else:
    from debug.camerableu import take_photos

# Set number of photos taken per minute
_sampling_rate = 2

# Prepare time markers
_current_time = time.localtime()
_c_minute = _current_time.tm_min
_c_hour   = _current_time.tm_hour
_c_day    = _current_time.tm_wday

# Today's directory
_dirname = time.strftime(s.YMD_FORMAT, _current_time)

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

def analyze_picture(pic):
    # pic[0] = picname, pic[1] = picpath
    # Get time from os.timestamp (easier than from filename)
    # calc values
    fullpath = pic[1] + '/' + pic[0]
    t = os.path.getmtime(fullpath)
    time = datetime.datetime.fromtimestamp(t)
    img = cv2.imread(fullpath)

    # Create db container
    data = BasicData()
    data.set_rgb(anal.rgb_distribution(img))
    data.set_hsv(anal.hsv_distribution(img))
    data.set_movement(anal.find_movement(pic))

    # FIXME arrange some pytables here
    print 'RGB:', data.red, data.green, data.blue
    print 'HSV:', data.hue, data.saturation, data.value
    print 'Movement:', data.movement

    # Updating the database
    if _c_day is 0:
        print 'wtf'

if __name__ == '__main__':
    # Container for pic names [0] - picname, [1] - picpath (just dir)
    pictures = take_photos(3)

    # Perform a shitload of datascience
    for pic in pictures:
        analyze_picture(pic)

    # Begin cronjobish definitions
    if not _DEBUG:
        # Maybe post picture
        if _pic_post_hours.count((_c_hour, _c_minute)) is not 0:
            print 'fake posting in progress'
