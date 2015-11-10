""" Fake methods for debugging without all
    of the facebook api crap """

# TODO - we need to contain datetime picture naming convention
# throughout the project, so this is a good place to check
# while in debug mode

def post_to_wall(pic, message):
    picpath = pic[1] + '/' + pic[0]
    print "post_to_wall DEBUG version run with:", picpath, message

def post_to_album(pic, message):
    picpath = pic[1] + '/' + pic[0]
    print "post_to_album DEBUG version run with:", picpath, message
