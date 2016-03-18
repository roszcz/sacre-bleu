import glob
import time
import subprocess as sp
import os
from utils import upload_video as uv

def make_video_on_yt(foldername, title):
    """ Creates mpg file and uploads to youtube """
    # Takes date / folder and creates a mpg 
    moviename = foldername + '.mpg'
    print moviename

    # Settings FIXME - why is this hardcoded here, bitch
    framerate = 15

    # Dunno how to make the movie smoother?
    # Must provide a full path to ffmpeg or cron bash won't know
    # Where to find it? 
    command = '/usr/local/bin/ffmpeg -framerate ' + str(framerate) + ' '\
            '-i ' + foldername + '/100%04d.jpg '\
            '-c:v libx264 -r 30 '\
            '-pix_fmt yuv420p ' + moviename
    sp.call(command, shell=True)

    ID = push_video(moviename, title)

    return ID

def push_video(moviepath, title):
    """ Load to youtube and retrieve unique ID """
    description = 'This video is a part of sacrebleu project:\n' +\
        'https://www.facebook.com/pages/sacre-bleu/119890141687062'

    # TODO - make this listed somewhen
    privacyStatus = 'unlisted'

    details = {\
            'file' : moviepath,\
            'title' : title,\
            'description' : description,\
            'privacyStatus' : privacyStatus\
            }

    ID = uv.upload_video(details)

    return ID

