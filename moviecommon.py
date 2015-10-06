import glob
import time
import subprocess as sp
import os
from upload_video import upload_video

def arrange_images(foldername):
    # Assumes that script is run from the
    # one level higher folder
    query = foldername + '/*.jpg'
    files = glob.glob(query)

    # Sort files by creation date
    files.sort(key=os.path.getmtime)

    for (it, file) in enumerate(files):
	new_name = foldername + '/movieme' + str(it + 1000000) + '.jpg'
	os.rename(file, new_name)

def make_video(foldername):
    # Takes date / folder and creates a mpg 
    moviename = foldername

    # Settings FIXME - why is this hardcoded here, bitch
    framerate = 20
    
    # Dunno how to make the movie smoother?
    # Must provide a full path to ffmpeg or cron bash won't know
    # Where to find it? 
    command = '/usr/local/bin/ffmpeg -framerate ' + str(framerate) + ' '\
	      '-i ' + foldername + '/movieme100%04d.jpg '\
	      '-c:v libx264 -r 30 '\
	      '-pix_fmt yuv420p ' + moviename + '.mpg'
    sp.call(command, shell=True)

def render_video(foldername):
    arrange_images(foldername)
    make_video(foldername)


def push_video(foldername):
    # Push to youtube
    #struct = time.strptime(foldername, '%Y_%m_%d')
    title = time.strftime('%Y %B %d in super slow motion')
    
    description = 'This video is a part of sacrebleu project:\n' +\
	    'https://www.facebook.com/pages/sacre-bleu/119890141687062'

    # TODO - make this listed somewhen
    privacyStatus = 'unlisted'

    details = {\
	    'file' : foldername + '.mpg',\
	    'title' : title,\
	    'description' : description,\
	    'privacyStatus' : privacyStatus\
	    }

    id = upload_video(details)

    return id


