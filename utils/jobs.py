from utils import camerableu as uc
from utils import settings as us
from datascience import ising as di
from datastorage import databasing as db
from datetime import datetime as dt
from glob import glob
import os

def take_pictures():
    """ Just that """
    uc.take_photos(2)

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
    for _ in range(4):
        Ising.run()
