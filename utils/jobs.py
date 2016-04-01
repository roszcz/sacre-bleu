from utils import camerableu as cam
from utils import common as uc
from utils import settings as us
from community import posters as cp
from datastorage import databasing as db
from datascience import ising as di
from datascience import analysis as da
from datascience import plotters as dp
from datetime import datetime as dt
from datetime import timedelta
import numpy as np
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
    # Delete every-minute pictures
    path = us.picture_path() + '/*'
    for file in glob(path):
	if os.path.isfile(file):
	    os.remove(file)

    # Delete full timelapse
    timelapse = 'img/pics.mpg'
    os.remove(timelapse)

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

    # Cleanup after week of isinging
    path = us.ising_path() + '/*'
    for file in glob(path):
	if os.path.isfile(file):
	    os.remove(file)

    # Clean mpg file
    ising_mpg = 'img/ising.mpg'
    os.remove(ising_mpg)

    # Ising pickle file
    picklepath = 'data/ising.pickle'
    os.remove(picklepath)

def post_day_movie():
    """ Create timelapse, post to yt, post link on facebook """
    # Attachment facebook info:
    # Title is not for fb, but for yt and must be poped
    title = dt.now().strftime('%Y %B %d in super slow motion')
    att = {
	    'title'	    : title,
            'name'	    : title,
            'caption'	    : 'fully automatic',
            'description'   : 'timelapse'
    }

    cp.post_timelapse(us.picture_path(), att)

def post_sunrise_rgb():
    """ Simple rgb plot from last few hours """
    plotpath = dp.last_hours_rgb(2)

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

def compare_week_brightness():
    """ Post a plot that shows change in days brigthness over a week """
    now = dt.now()

    # We assume this will be run after sunset
    aend = now
    # Sunrise must be after this hour
    astart = now.replace(hour = 1)

    astarts = astart.strftime('%x %X')
    aends = aend.strftime('%x %X')

    # Other series of data must come from a 7 days ago
    bstart = astart - timedelta(days=7)
    bend = aend - timedelta(days=7)

    bstarts = bstart.strftime('%x %X')
    bends = bend.strftime('%x %X')

    # Get the data from the database
    base = db.get_base()
    sd = base['sacredata']

    aseries = sd.loc[astarts:aends, ['value']]
    bseries = sd.loc[bstarts:bends, ['value']]

    times = aseries.index

    avals = aseries.values
    bvals = bseries.values

    # This temporarily fixes issues with daylight 
    # changes and number of samples per day or whatnot
    if len(avals) is not len(bvals):
	alen, blen = len(avals), len(bvals)
	if alen > blen:
	    avals = avals[-blen::]
	    times = bseries.index
	else:
	    bvals = bvals[-alen::]

    vals = np.concatenate((avals, bvals), axis=1)
    
    plot = dp.Plot(times, vals)
    plot.set_colors(['c', 'g'])
    plot.set_legend(['Today', 'A week ago'])
    plot.set_ylabel('brightness [a.u.]')

    filepath = 'dupa.png'
    plot.make_figure(filepath)

    cp.post_on_wall(filepath, '')

    os.remove(filepath)
