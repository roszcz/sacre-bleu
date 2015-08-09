#!/home/yo/.virtualenvs/sacrebleu/bin/python
from sacrecommon import post_video, get_api
from moviecommon import push_video
import time
import os

# Find newest dir (hopefuly with photos)
dirs = [f for f in os.listdir(os.getcwd()) if os.path.isdir(f)]
newest = max(dirs, key = os.path.getmtime)

api = get_api()

# Upload to Youtube
video_id = push_video(newest)

# Publish with current date as a message
message = 'opublikowano ' + time.strftime('%d %B %Y, %H:%M') 
post_video(api, video_id, message)
