#!/usr/bin/python
""" ignorance is hell """
import os
import time
from sacrecommon import *

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

# Set number of photos taken per minute
_sampling_rate = 2

# Container for pic names [0] - picname, [1] - picpath
pictures = []

# Photoshoot
for it in range(_sampling_rate):
    # Don't wait before the first picture
    if it is not 0:
	time.sleep(_pic_time_distance)

    # click
    pictures.append(take_photo(_exposure_time))


# Begin cronjobish definitions

# Prepare hours to post photo
_pic_post_hours = [(4,20),
		   (7,20),
		   (10,20),
		   (13,20),
		   (16,20),
		   (19,20)]

# Maybe post picture
if _pic_post_hours.count((_c_hour, _c_minute)) is not 0:
    post_to_album(pictures[0])

# Post sunrise photos
_sunrise_hour = (6,0)

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

