from utils import settings as us

if us.is_facebook():
    from community import realface as cf
else:
    from community import fakeface as cf

if us.is_youtube():
    from community import realmovie as cm
else:
    from community import fakemovie as cm

def post_on_wall(picpath, message = 'hi'):
    """ Hello """
    cf.post_to_wall(picpath, message)

def post_to_album(picpath, album_name, message = 'hi'):
    """ It's me """
    cf.post_to_album(picpath, album_name, message)

def post_timelapse(foldername, attachment):
    """ Create and post a video """
    # Create ising video
    title = attachment.pop('title')
    video_id = cm.make_video_on_yt(foldername, title)

    # TODO outsorce everything beside the link
    # Declare facebook post
    link = 'https://www.youtube.com/watch?v=' + str(video_id)
    attachment.update({'link' : link})

    cf.attach_to_wall(attachment)
