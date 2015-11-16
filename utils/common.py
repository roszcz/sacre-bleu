from glob import glob
import os
import inspect

def get_files(foldername):
    # Get sorted files
    files = glob(foldername + '/*.jpg')
    # Should remember this
    files.sort(key=os.path.getmtime)

    return files;

# Imitate cpp's __func__
def fname():
    return inspect.stack()[1][3]
