import pandas as pd
from datetime import datetime as dt
import os

def get_base():
    """ This is supposed to initialize the database file """
    filename = 'db.h5'

    if os.path.isfile(filename):
        # Open existing file and append
        store = pd.HDFStore(filename, 'a')
    else:
        # Initialize pandas dataframe with all zeros first row
        columns = ['red', 'green', 'blue',
                   'hue', 'saturation', 'value',
                   'movement']
        df = pd.DataFrame(np.zeros([1, len(columns)]),
                          index = [pd.to_datetime(dt.now())],
                          columns = columns)
        # Create db file
        store = pd.HDFStore(filename)
        store['sacredata'] = df

    return store
