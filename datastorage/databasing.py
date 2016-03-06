""" This should be visible only as db.update_base(key, val)? """
import numpy as np
import pandas as pd
from datetime import datetime as dt
from utils import settings as us
import os

class SacreData(object):
    """ One row of data """
    def __init__(self, timestamp):
        """ Construct """
        # Pandas table is indexed with time of measurement
        self.timestamp = timestamp

        # Some crap pseudo data that can 
        # be easily extracted from picamera pictures
        self.red = 0
        self.green = 0
        self.blue = 0
        self.hue = 0
        self.saturation = 0
        self.value = 0

        # Barely more advanced data
        self.movement = 0

    def set_rgb(self, rgb):
        """ rgb """
        self.red = rgb[0]
        self.green = rgb[1]
        self.blue = rgb[2]

    def set_hsv(self, hsv):
        """ hsv """
        self.hue = hsv[0]
        self.saturation = hsv[1]
        self.value = hsv[2]

    def set_movement(self, movement):
        """ movement """
        self.movement = movement

    def save(self):
        """ Saves """
        store = get_base()
        # This seems pretty low on style
        datadict = self.__dict__
        now = datadict.pop('timestamp')
        df = pd.DataFrame(data=datadict, index=[now])
        store['sacredata'] = store['sacredata'].append(df)
        store.close()

def get_minute_data(column, start, stop):
    """ Get some data with minutes resolution """
    # Start and stop must be datetime strings?
    # returns totally plotable lists
    base = get_base()
    sacredata = base['sacredata']

    serie = sacredata.loc[start:stop, column]

    # Convert from pd.Series to t, y(t) vectors
    return serie.index.tolist(), serie.values

# TODO this is for the future
def get_daily_data(column, start, stop):
    """ """
    # For now there is no such DataFrame,
    # But there might be for example with
    # estimated sunrise hours etc.
    base = get_base()
    dailydata = base['dailydata']

def get_base():
    """ Get pandas DataFrame from file """
    # Everything is set in the settings module
    filename = us.db_path()

    if os.path.isfile(filename):
        # Open existing file and append
        store = pd.HDFStore(filename, 'a')
    else:
        # Initialize pandas dataframe with all zeros first row
        # FIXME we need dynamic database, yo
        columns = ['red', 'green', 'blue',
                   'hue', 'saturation', 'value',
                   'movement']
        df = pd.DataFrame(np.zeros([1,len(columns)]),
                          index = [pd.to_datetime(dt.now())],
                          columns = columns)
        # Create db file
        store = pd.HDFStore(filename)
        store['sacredata'] = df

    # Call store.close() after using this?
    return store

