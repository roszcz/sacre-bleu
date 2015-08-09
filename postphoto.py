#!/home/yo/.virtualenvs/sacrebleu/bin/python
import time
from random import random
import os
import sys
from sacrecommon import *
from cloudsmovement import last_hour_plot

long_exposure = 0
if len(sys.argv) > 1:
    long_exposure = 6 


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
if (struct.tm_min==0 and random() > 0.4):
    plotname = last_hour_plot(dirname)
    post_to_wall(plotname, ' ')
