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
import settings as st
import blotters.plotters as plt
from utils import common as uc
from datetime import datetime as dt
from datastorage import databasing as dbb
from datascience import analysis as anal # trolololo

# Modules like picamera make sense only on rpi
# and for developement purposes we emulate them here
if not _DEBUG:
    from utils.camerableu import take_photos
else:
    from debug.camerableu import take_photos

# Prepare time markers
_current_time = time.localtime()
_c_minute = _current_time.tm_min
_c_hour   = _current_time.tm_hour
_c_day    = _current_time.tm_wday

# Today's directory
_dirname = time.strftime(st.YMD_FORMAT, _current_time)

# Post sunrise photos - this is time of plot,
# so consider some offset
_sunrise_hour = (6, 20)

# This function is run multiple times during this script
# TODO should this migrate to the anal?
def analyze_picture(pic):
    """ Perform anal and update base """
    # pic[0] = picname, pic[1] = picpath
    # Read picture as np.array of BGR
    fullpath = pic[1] + '/' + pic[0]
    img = cv2.imread(fullpath)

    # Create db container FIXME - timestamp must be read from picname
    time = dt.strptime(pic[0], st.TIME_FORMAT)
    data = dbb.SacreData(time)
    data.set_rgb(anal.rgb_distribution(img))
    data.set_hsv(anal.hsv_distribution(img))
    data.set_movement(anal.find_movement(pic))
    data.save()

    # FIXME arrange some pytables here
    print 'RGB:', data.red, data.green, data.blue
    print 'HSV:', data.hue, data.saturation, data.value
    print 'Movement:', data.movement

    # weekly analysis? (0 - monday)
    if _c_day is 0:
        print 'wtf', uc.fname()

# This is run once per minute
def plot_plots():
    post_sunrise_rgb()
    post_daily_brightness()

def post_sunrise_rgb():
    """ Fold descriptor """
    base = dbb.get_base()
    sd = base['sacredata']
    # Get desired time-span
    end = dt.now()
    # Let's say sunrise begun 2h ago
    start = end - datetime.timedelta(hours=2)

    # Convert to strings recognazible by pandas
    starts = start.strftime('%x %X')
    ends = end.strftime('%x %X')
    # Load from the database
    rgb_series = sd.loc[starts:ends, ['red', 'green', 'blue']]
    print rgb_series
    # Convert from pandas format
    rgb_time = rgb_series.index
    rgb_vals = rgb_series.values

    # TODO Implement this - new fb storing model
    # should be designed, allowing for easier
    # history plots and videos browsing
    print uc.fname(),\
          'fake posting a picture:',\
          plt.make_rgb_plot(rgb_time, rgb_vals)
    print 'deleting will be here also'
    base.close()

def post_daily_brightness():
    """ Dawn to dusk plot of total radiance on the pictures """
    base = dbb.get_base()
    sd = base['sacredata']

    # Get today as a pandas locator
    starts = dt.now().strftime('%x')

    bright_series = sd.loc[starts, 'value']
    bright_time = bright_series.index
    bright_vals = bright_series.values

    print uc.fname(),\
          'fake posting a plot:',\
          plt.make_brightness_plot(bright_time, bright_vals)
    base.close()

def main():
    """ This happens regularry """
    # Container for pic names [0] - picname, [1] - picpath (just dir)
    pictures = take_photos(st._sampling_rate)

    # Perform a shitload of datascience
    for pic in pictures:
        analyze_picture(pic)

    # TODO Plotting and posting must be done here
    plot_plots()

    # Begin cronjobish definitions
    if not _DEBUG:
        # Maybe post picture
        if st._pic_post_hours.count((_c_hour, _c_minute)) is not 0:
            print 'fake posting in progress'

if __name__ == '__main__':
    """ RUNME """
    main()
    # Container for pic names [0] - picname, [1] - picpath (just dir)
    pictures = take_photos(st._sampling_rate)

    # Perform a shitload of datascience
    for pic in pictures:
        analyze_picture(pic)

    # TODO Plotting and posting must be done here
    plot_plots()

    # Begin cronjobish definitions
    if not _DEBUG:
        # Maybe post picture
        if st._pic_post_hours.count((_c_hour, _c_minute)) is not 0:
            print 'fake posting in progress'
