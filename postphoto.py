#!/home/yo/.virtualenvs/sacrebleu/bin/python
import random
import os
import sys
from sacrecommon import *

long_exposure = False
if len(sys.argv) > 1:
    long_exposure = True

api = get_api()

picname = take_photo(long_exposure)

msg = 'tania przestrzen reklamowa'

post_to_album(api, picname, msg)

os.remove(picname)
