#!/home/yo/.virtualenvs/sacrebleu/bin/python
import random
import os
from sacrecommon import *

api = get_api()

picname = take_photo()

msg = 'this is a random number: ' + str(random.random())

api.put_photo(image = open(picname), message = msg)

os.remove(picname)
