#!/usr/bin/python
""" ignorance is hell """

import time

# Prepare time markers
_current_time = time.localtime()
_c_minute = _current_time.tm_min
_c_hour   = _current_time.tm_hour

# Begin with taking 2 photos
# TODO - some different mechanism will be
# required for live monitoring

# Set exposure time (0 - automatic)
_exposure_time = 0
_pic_time_distance = 27

# Set number of photos taken per minute
_sampling_rate = 2

# Container for pic names
picnames = []

# Photoshoot
for it in range(_sampling_rate):
    # Don't wait before the first picture
    if it is not 0:
	time.sleep(_pic_time_distance)

    # click
    picnames.append(take_photo(_exposure_time))


# Begin cronjobish definitions
if (_c_hour == 4 and _c_minute == 20)
