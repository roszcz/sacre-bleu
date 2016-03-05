from utils import camerableu as cam
from utils import settings as us
from utils import jobs as uj

def perform_action(action):
    """ Specialized cronish scheduler for sacrebleu """
    if 'TAKE_PICTURES' in action:
        uj.take_pictures()
    if 'PERFORM_ANAL' in action:
        print 'anal now'
    if 'POST_PLOTS' in action:
        print 'post'

def main():
    """ This is run every minute for proper sacrebleuing """
    actions = us.get_actions()

    for action in actions:
        perform_action(action)

if __name__ == '__main__':
    main()
