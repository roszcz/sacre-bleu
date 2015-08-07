#!/home/yo/.virtualenvs/sacrebleu/bin/python
from sacrecommon import post_video, get_api
from moviecommon import push_video
import os

dirs = [f for f in os.listdir(os.getcwd()) if os.path.isdir(f)]
newest = max(dirs, key = os.path.getmtime)

api = get_api()

# FIXME - temp change for testing
video_id = push_video(newest)
post_video(api, video_id, 'moc pozdrowien')
