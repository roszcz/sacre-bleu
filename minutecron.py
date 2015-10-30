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
pic_a = take_photo(_exposure_time)
time.sleep(27)
pic_b = take_photo(_exposure_time)

# Begin cronjobish definitions
if (_c_hour == 4 and _c_minute == 20)
