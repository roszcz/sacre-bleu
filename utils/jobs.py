from utils import camerableu as cam
from utils import common as uc
from utils import settings as us
from community import posters as cp
from datascience import ising as di
from datascience import analysis as da
from datascience import plotters as dp
from datetime import datetime as dt
import wolframalpha as wa
import random
from glob import glob
import os

# FIXME this needs a new name
def take_pictures():
    """ Just that """
    pictures = cam.take_photos(2, 0)
    da.perform_anal(pictures)

def post_fresh_picture():
    """ Posts most recent picture taken by the sacrebleu """
    paths = uc.get_jpgs(us.picture_path())
    path = paths[-1]

    cp.post_on_wall(path, '')

def clean_up():
    """ Delete everything from the day """
    paths = [us.picture_path(), us.plot_path(),\
             us.ising_path()]
    paths = [path + '/*' for path in paths]

    for path in paths:
        for file in glob(path):
            if os.path.isfile(file):
                os.remove(file)

    # TODO remake this so you have to specify all paths to clear
    # Clean mpg file
    moviepath = 'img/ising.mpg'
    os.remove(moviepath)

    # Ising pickle file
    picklepath = 'data/ising.pickle'
    os.remove(picklepath)

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
    # Title is not for fb, but for yt and must be poped
    att = {
            'name'	    : 'Ising stress test',
	    'title'	    : '2D Ising Model Simulation',
            'caption'	    : 'fully automatic',
            'description'   : 'metropolis simulation'
    }

    cp.post_timelapse(us.ising_path(), att)

def post_day_movie():
    """ Create timelapse, post to yt, post link on facebook """
    # Attachment facebook info:
    # Title is not for fb, but for yt and must be poped
    title = dt.now().strftime('%Y %B %d in super slow motion')
    att = {
	    'title'	    : title,
            'name'	    : 'Ising stress test',
            'caption'	    : 'fully automatic',
            'description'   : 'metropolis simulation'
    }

    cp.post_timelapse(us.picture_path(), att)

def post_sunrise_rgb():
    """ Simple rgb plot from last few hours """
    plotpath = dp.last_five_hours_rgb()

    # Prepare message
    # Load wolfram
    with open('wolfram.secret','r') as fin:
        secret = fin.read().strip('\n')
    client = wa.Client(secret)
    res = client.query('sunrise in Krakow Polska')

    # Parse sunrise hour string
    msg = 'sunrise time estimate: ' + ' '.join(res.pods[1].text.split()[0:2])

    # Post on facebook!
    cp.post_on_wall(plotpath, msg)
    os.remove(plotpath)
