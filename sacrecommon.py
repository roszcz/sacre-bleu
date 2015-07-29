import facebook
from fractions import Fraction
import time
import picamera

def get_secrets(filenames):
	with open(filenames[0], 'r') as myfile:
		token = myfile.read().replace('\n','')

	with open(filenames[1], 'r') as idfile:
	    page_id = idfile.read().replace('\n','')

	return token, page_id

def get_api():
    cfg = make_cfg()
    graph = facebook.GraphAPI(cfg['access_token'], version='2.4')
    #  Get page token to post as the page. You can skip
    #  the following if you want to post as yourself.
    resp = graph.get_object('me/accounts')
    page_access_token = None
    for page in resp['data']:
	if page['id'] == cfg['page_id']:
	    page_access_token = page['access_token']
	    graph = facebook.GraphAPI(page_access_token, version='2.4')
    return graph
# You can also skip the above if you get a page token:
#http://stackoverflow.com/questions/8231877/facebook-access-token-for-pages
# and make that long-lived token as in Step 3

def make_cfg():
    token, pageid = get_secrets(['token.secret', 'pageid.secret'])
    cfg = {
	    'page_id' : '119890141687062',
	    'access_token' : token
	    }
    
    return cfg

def get_album_id(api, picname):
    # XXX Possible date string fuckup
    date = picname[0:10]
    time_struct = time.strptime(date, '%Y_%m_%d')
    album_name = time.strftime('%Y %B %d', time_struct)
    albums = api.get_object('me/albums')['data']

    # Iterate through albums untill the proper one is found
    # TODO some better search mechanism might be desired
    id = None
    for bum in albums:
	print bum['name']
	if album_name in bum['name']:
	    id = bum['id']

    # Create album is nothing were found
    if id is None:
	resp = api.put_object(parent_object = 'me',\
			      connection_name = 'albums',\
			      message = 'Album',\
			      name = album_name)
	id = resp['id']
    
    return id

def take_photo(long = False):
    picname = time.strftime('%Y_%m_%d__%H%M%S') + '.jpg'
    with picamera.PiCamera() as camera:
	camera.resolution = (666, 420)
	if long:
	    camera.framerate = Fraction(1,6)
	    camera.shutter_speed = 6 * 1000000 
	    camera.exposure_mode = 'off'
	camera.start_preview()
	# Camera warm up
	time.sleep(2)
	camera.capture(picname)
    return picname

def post_to_album(api, picname, message):
    # Get desired album id
    id = get_album_id(api, picname)
    api.put_photo(image = open(picname),\
		  message = message,\
		  album_path = id + '/photos')

