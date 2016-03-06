from utils import settings as us

if us.is_facebook():
    from community import realface as cf
else:
    from community import fakeface as cf

def post_on_wall(picpath, message = 'hi'):
    """ Hello """
    cf.post_to_wall(picpath, message)

def post_to_album(picpath, album_name, message = 'hi'):
    """ It's me """
    cf.post_to_album(picpath, album_name, message)
