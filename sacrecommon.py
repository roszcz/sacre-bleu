import facebook
import cv2
import os
import subprocess
from fractions import Fraction
import time
import picamera
import settings as s

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
    hour = picname[12:14]

    # Add AM/PM albums each day at 14
    if int(hour) >= 14:
	postfix = ' p.m.'
    else:
	postfix = ' a.m.'

    # Remove postfix at least temporarly

    # Name album with the current pic date
    time_struct = time.strptime(date, '%Y_%m_%d')
    album_name = time.strftime('%Y %B %d', time_struct)

    # And add am/pm postfix
#    album_name += postfix
    albums = api.get_object('me/albums')['data']

    # Iterate through albums untill the proper one is found
    # TODO some better search mechanism might be desired
    id = None
    for bum in albums:
	#print bum['name']
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

def take_photo(long = 0):

    # Possible resolutions
    low_hd = (1280, 720)
    full_hd = (1920, 1080)

    # Set
    resolution = full_hd

    # Date string confusion
    datestr = time.strftime(s.YMD_FORMAT)
    hourstr = time.strftime(s.HMS_FORMAT)
    picname = datestr + '__' + hourstr + '.jpg'

    # Picture taking
    with picamera.PiCamera() as camera:
	camera.resolution = resolution

	# Long exposure is possible
	if long is not 0:
            camera.framerate = Fraction(1,6)
            camera.shutter_speed = long * 1000000
            camera.exposure_mode = 'off'
	camera.start_preview()
	# Camera warm up
	time.sleep(2)
	savename = datestr + '/' + picname

	# Check dir existance
	if not os.path.isdir(datestr):
	    os.makedirs(datestr)

	# FIXME - add ABW control
	gains = (Fraction(383, 256), Fraction(41, 32))
	camera.awb_mode = 'off'
	camera.awb_gains = gains
	camera.capture(savename)

        # Add clock for the timelapse experience
        add_cock(savename)

    return picname, savename

# Add clock onto the image
def add_cock(filepath):
    img = cv2.imread(filepath)
    #print img.shape
    x = 0
    y = img.shape[0] - 16
    timestr = time.strftime('%H:%M')
    cv2.putText(img, timestr, (x,y),\
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0),\
                thickness=8)
    cv2.imwrite(filepath, img)

def post_to_wall(picname, message):
    # Get facebook api
    api = get_api()

    # Pictures posted to wall are held at the main dir
    # FIXME - add some dir structure
    api.put_photo(image = open(picname),\
                  message = message)


def post_to_album(picInfo, message):
    # Get facebook api
    api = get_api()

    # Date names directories
    picname = picInfo[0]
    picpath = picInfo[1]
    datestr = picname[0:10]

    # Get desired album id
    id = get_album_id(api, picname)

    # Add clock information to post message
    cock = picname[12:18]
    struct = time.strptime(cock, '%H%M%S')
    clock_msg = time.strftime('%X', struct)

    # Extend message with clock info
    message = message + '\n\n\n' + clock_msg

    # and ip
#    ipinfo = subprocess.check_output('ifconfig |grep inet', shell=True)
 #   message = message + '\n\n\n' + ipinfo
    api.put_photo(image = open(picpath),\
		  message = message,\
		  album_path = id + '/photos')

def post_video(video_id, msg):
    # Get facebook api
    api = get_api()
    attachment =  {
	    'name': 'Chmury?',
	    'link': 'https://www.youtube.com/watch?v=' + str(video_id),
	    'caption': 'fully automatic time-lapse generator',
	    'description': 'film wygenerowany automatycznie',
    }

    api.put_wall_post(message = msg, attachment = attachment)
