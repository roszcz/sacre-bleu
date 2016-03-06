from utils import camerableu as cam
from utils import common as uc
from utils import settings as us
from community import posters as cp
from datascience import ising as di
from datastorage import databasing as db
from datetime import datetime as dt
import random
from glob import glob
import os

def take_pictures():
    """ Just that """
    cam.take_photos(2)

def clean_up():
    """ Delete everything from the day """
    paths = [us.picture_path(), us.plot_path(),\
             us.ising_path()]
    paths = [path + '/*' for path in paths]

    for path in paths:
        for file in glob(path):
            if os.path.isfile(file):
                os.remove(file)

def perform_anal():
    """ Regularly, save results in the database """
    # Clear microseconds
    now = dt.now()
    data = db.SacreData(now)
    data.set_rgb([1,2,3])
    data.set_hsv([6,6,6])
    data.set_movement(123)
    data.save()
    print 'done anal'

def iterate_ising():
    """ This is a stress test """
    Ising = di.PersistentIsing()
    # Take 4 steps
    for _ in range(2):
        Ising.run()

def post_ising_pic():
    """ Put random ising picture on the facebook wall! """
    # Get path to random picture
    paths = uc.get_jpgs(us.ising_path())
    path = random.choice(paths)

    cp.post_on_wall(path)

def post_ising_vid():
    """ Create timelapse, post to yt, post link on facebook """
    # Attachment facebook info:
    att = {
            'name' : 'Ising stress test',
            'caption' : 'fully automatic',
            'description' : 'metropolis simulation'
    }

    cp.post_timelapse(us.ising_path(), att)

