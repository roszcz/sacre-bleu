#!/home/yo/.virtualenvs/sacrebleu/bin/python
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

post_to_album(api, picname, msg)


# FIXME - Uncomment this before there is no more space pls
#if len(sys.argv) > 1:
os.remove(picname)
