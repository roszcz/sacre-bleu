#!/home/yo/.virtualenvs/sacrebleu/bin/python
import time
import random
import os
import sys
from sacrecommon import *

long_exposure = 0
if len(sys.argv) > 1:
    long_exposure = 6 

api = get_api()

picname = take_photo(long_exposure)

msg = 'tania przestrzen reklamowa'

# FIXME - post every 20 minutes only, this should be prettier
clock = picname[12:18]
struct = time.strptime(clock, '%H%M%S')

# Post periodically
if ((struct.tm_min%60)==0):
    print 'dupa'
    post_to_album(api, picname, msg)


# FIXME - Uncomment this before there is no more space pls
#if len(sys.argv) > 1:
#os.remove(picname)
