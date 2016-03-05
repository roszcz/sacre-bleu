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

def picture_path():
    """ """
    cfg = load_cfg()
    return cfg['img_path']

def minutely_jobs():
    """ Read jobs scheduled for any minute """
    pass

def get_actions():
    """ Find out what actions are to be performed right now """
    # Get current timestamp
    now = dt.now()

    # Load configuration
    cfg = load_cfg()

    # Prepare container for actions
    actions = []

    # Check if now is in the range for every-minute action
    minutely = cfg['minutely']
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
