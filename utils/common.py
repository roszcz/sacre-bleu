from glob import glob
import os
import inspect

def get_files(foldername):
    """ Get pictures sorted by harddrive time """
    # Get sorted files
    files = glob(foldername + '/*.jpg')
    # Should remember this
    files.sort(key=os.path.getmtime)

    return files;

def fname():
    """ Imitates cpp's __func__ """
    return inspect.stack()[1][3]
