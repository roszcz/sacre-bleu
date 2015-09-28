#!/usr/bin/python
""" #!/home/yo/.virtualenvs/sacrebleu/bin/python """
import time
from random import random
import os
import sys
from sacrecommon import *
from cloudsmovement import last_hour_plot
from colorhistogram import make_histogram
from sunsetplotter import rgb_plot
from sunsetplotter import hsv_plot

long_exposure = 0
if len(sys.argv) > 1:
    long_exposure = 8 

# Take 2 photos trick - control framerate as well
take_photo(long_exposure)
time.sleep(27)
picname = take_photo(long_exposure)
dirname = picname[0:10]

msg = 'tania przestrzen reklamowa'

# FIXME - post every 20 minutes only, this should be prettier
clock = picname[12:18]
struct = time.strptime(clock, '%H%M%S')

# Post periodically
if (struct.tm_min==20 and struct.tm_hour%3==1):
    print 'dupa'
    api = get_api()
    post_to_album(picname, msg)

# Post plot with recent movement detection
if (struct.tm_min%30==2 and random() < 0.05):
    plotname = last_hour_plot(dirname)
    post_to_wall(plotname, ' ')
    os.remove(plotname)

# Make pretty histograms of popular colors 
if (random() < 0.04 and struct.tm_min%40==13):
    picpath = dirname + '/' + picname
    plotname = make_histogram(picpath)
    post_to_wall(plotname, ' ')
    os.remove(plotname)

# Post plot with sunrise rgb
if (struct.tm_hour == 6 and struct.tm_min == 19):
    plotname = rgb_plot(dirname)
    post_to_wall(plotname, 'wschod')
    os.remove(plotname)

# Post plot with sunrise hsv
if (struct.tm_hour == 6 and struct.tm_min == 25):
    plotname = hsv_plot(dirname)
    post_to_wall(plotname, ' ')
    os.remove(plotname)
