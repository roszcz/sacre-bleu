import configobj as co
from datetime import datetime as dt

def load_cfg(setupath = 'setup.ini'):
    """ Loader """
    cfg = co.ConfigObj(setupath)

    return cfg

def is_debug():
    """ Globally used to check the sacrebleu mode """
    cfg = load_cfg()
    out = 'DEBUG' in cfg['mode']
    return out

def is_facebook():
    """ Checker """
    cfg = load_cfg()
    out = 'YES' in cfg['facebook']
    return out

def db_path():
    """ Database file path """
    cfg = load_cfg()
    return cfg['db_file']

def ising_path():
    """ Where ising snapshots are held """
    cfg = load_cfg()
    return cfg['ising_img']

def picture_path():
    """ """
    cfg = load_cfg()
    return cfg['img_path']

def plot_path():
    """ """
    cfg = load_cfg()
    return cfg['plot_path']

def minute_actions():
    """ Read jobs scheduled for any minute """
    # Get current timestamp
    now = dt.now()

    # Load configuration
    cfg = load_cfg()

    # Prepare container for actions
    actions = []

    # Check if now is in the range for every-minute action
    minutely = cfg['minute']
    start = minutely['start']
    # Convert to a dt.timestamp within the same day as *now*
    start = dt.strptime(start, '%H:%M')
    start = now.replace(hour = start.hour, minute = start.minute)

    stop = minutely['stop']
    stop = dt.strptime(stop, '%H:%M')
    stop = now.replace(hour = stop.hour, minute = stop.minute)

    if start < now < stop:
        actions += minutely['actions']

    return actions

def daily_actions():
    """ Same for once per day actions """
    # Get current timestamp
    now = dt.now()

    # Load configuration
    cfg = load_cfg()

    # Prepare container for actions
    actions = []

    # Check if now is in the range for every-minute action
    daily = cfg['daily']

    for event in daily:
        when = daily[event]['when']
        when = dt.strptime(when, '%H:%M')
        when = now.replace(hour = when.hour, minute = when.minute)

        if when == now:
            actions += daily[event]['actions']
            print actions

    return actions

def get_actions():
    """ Find out what actions are to be performed right now """
    actions = []

    actions += minute_actions()
    actions += daily_actions()

    return actions
