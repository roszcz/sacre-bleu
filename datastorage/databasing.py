""" This should be visible only as db.update_base(key, val)? """
import numpy as np
import pandas as pd
from datetime import datetime as dt
import os
import settings as s

# Struct for basic data, TODO - come up with advanced data
class SacreData(object):
    def __init__(self, timestamp):
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

    # Set of setters
    def set_rgb(self, rgb):
        self.red = rgb[0]
        self.green = rgb[1]
        self.blue = rgb[2]

    def set_hsv(self, hsv):
        self.hue = hsv[0]
        self.saturation = hsv[1]
        self.value = hsv[2]

    def set_movement(self, movement):
        self.movement = movement

    def save(self):
        store = get_base()
        # This seems pretty low on style
        datadict = self.__dict__
        now = datadict.pop('timestamp')
        df = pd.DataFrame(data=datadict, index=[now])
        store['sacredata'] = store['sacredata'].append(df)
        store.close()

def get_data(column, start, stop):
    # Start and stop must be datetime strings?
    # returns totally plotable lists
    base = get_base()
    sacredata = base['sacredata']

    serie = sacredata.loc[start:stop, column]

    # Convert from pd.Series to t, y(t) vectors
    return serie.index.tolist(), serie.values


def get_base():
    # Everything is set in the settings module
    filename = s.DBFILE

    if os.path.isfile(filename):
        # Open existing file and append
        store = pd.HDFStore(filename, 'a')
    else:
        # Initialize pandas dataframe with all zeros first row
        columns = s.COLUMNS
        df = pd.DataFrame(np.zeros([1,len(columns)]),
                          index = [pd.to_datetime(dt.now())],
                          columns = columns)
        # Create db file
        store = pd.HDFStore(filename)
        store['sacredata'] = df

    # Call store.close() after using this?
    return store
