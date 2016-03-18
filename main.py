#!/usr/bin/python
from utils import camerableu as cam
from utils import settings as us
from utils import jobs as uj

def perform_action(action):
    """ Specialized cronish scheduler for sacrebleu """
    if 'TAKE_PICTURES' in action:
        print 'taking pictures'
        uj.take_pictures()
    if 'PERFORM_ANAL' in action:
        print 'anal now'
        uj.perform_anal()
    if 'POST_PLOTS' in action:
        print 'post'
    if 'CLEAN_UP' in action:
        print 'cleaning'
        uj.clean_up()
    if 'MAKE_ISING' in action:
        print 'making ising'
        uj.iterate_ising()
    if 'POST_ISING_PIC' in action:
        print 'posting ising pic'
	uj.post_ising_pic()
    if 'POST_ISING_VID' in action:
        print 'posting ising vid'
        uj.post_ising_vid()
    if 'POST_SUNRISE_RGB' in action:
        print 'posting sunrise rgb plot'
        uj.post_sunrise_rgb()

def main():
    """ This is run every minute for proper sacrebleuing """
    actions = us.get_actions()

    for action in actions:
        perform_action(action)

if __name__ == '__main__':
    main()
