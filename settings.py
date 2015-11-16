""" This file holds used constants and settings of any sort """

# Year Mont Day
YMD_FORMAT = '%Y_%m_%d'

# Hour Minute Second
HMS_FORMAT = '%H%M%S'

# STRP Time format for picname -> datetime transformation
TIME_FORMAT = YMD_FORMAT + '__' + HMS_FORMAT + '.jpg'

# Database settables
COLUMNS = ['red', 'green', 'blue',
           'hue', 'saturation', 'value',
           'movement']

DBFILE = 'db.h5'
