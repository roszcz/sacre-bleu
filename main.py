from utils import camerableu as cam
from utils import settings as us

def perform_action(action):
    """ Specialized cronish scheduler for sacrebleu """
    if 'TAKE_PICTURES' in action:
        print 'woohoo'
    if 'PERFORM_ANAL' in action:
        print 'anal now'

def main():
    """ This is run every minute for proper sacrebleuing """
    actions = us.get_actions()

    for action in actions:
        perform_action(action)

if __name__ == '__main__':
    main()
