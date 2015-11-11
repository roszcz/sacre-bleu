from glob import glob
import os

def get_files(foldername):
    # Get sorted files
    files = glob(foldername + '/*.jpg')
    # Should remember this
    files.sort(key=os.path.getmtime)

    return files;
