import glob
import subprocess as sp
import os

def arrange_images(foldername):
    # Assumes that script is run from the
    # one level higher folder
    query = foldername + '/*.jpg'
    files = glob.glob(query)

    # Sort files by creation date
    files.sort(key=os.path.getmtime)

    for (it, file) in enumerate(files):
	new_name = foldername + '/movieme' + str(it + 1000000) + '.jpg'
	os.rename(file, new_name)

def make_video():
    command = 'ffmpeg -framerate 8 -i movie/movieme100%04d.jpg -c:v libx264 -r 30 -pix_fmt yuv420p out2.mpg'
    sp.call(command, shell=True)
