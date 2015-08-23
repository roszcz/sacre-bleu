#!/home/yo/.virtualenvs/sacrebleu/bin/python
import time
from random import random
import os
import sys
from sacrecommon import *
from cloudsmovement import last_hour_plot
from colorhistogram import make_histogram

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
if (struct.tm_min%20==2 and random() < 0.05):
    plotname = last_hour_plot(dirname)
    post_to_wall(plotname, ' ')
    os.remove(plotname)

# Make pretty histograms of popular colors 
if (random() < 0.05 and struct.tm_min%20==13):
    picpath = dirname + '/' + picname
    plotname = make_histogram(picpath)
    post_to_wall(plotname, ' ')
    os.remove(plotname)
