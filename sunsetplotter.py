from glob import glob
from matplotlib import dates
import gc
import time
import datetime
import random
import pickle
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import cv2


def get_files(foldername):
    # Get sorted files
    files = glob(foldername + '/*.jpg')
    # Should remember this
    files.sort(key=os.path.getmtime)

    return files;

def get_files_times(files):
    times = []
    for file in files:
	t = os.path.getmtime(file)
	dtime = datetime.datetime.fromtimestamp(t)
	times.append(dtime)

    return times

def brightness_plot(foldername, plotname = 'suntrace.png'):
    files = get_files(foldername)
    times = get_files_times(files)

    # Tic Toc
    tic = time.time()

    brightness = []
    for file in files:
	img = cv2.imread(file)
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	# TODO - should this really be 0 for brigthness?
	bright = hsv[:,:,2].sum()
	brightness.append(bright)
	if len(brightness)%20==7:
	    # This is not necessary, but we'll see
	    # what happens
	    dupa = gc.collect()
	    print int(time.time() - tic), '[s], files done:',\
		  len(brightness),'/',len(files),\
		  'brightness value:', bright

    # Save daily brightness, why not
    file = open('brightness.pickle', 'wb')
    pickle.dump(brightness, file)
	

    with plt.xkcd():
	# Based on "Stove Ownership" from XKCD by Randall Monroe
	# http://xkcd.com/418/

	fig = plt.figure()
	ax = fig.add_axes((0.1, 0.2, 0.8, 0.7))
	ax.spines['right'].set_color('none')
	ax.spines['top'].set_color('none')
	plt.xticks([])
	plt.yticks([])
	miny = min(brightness)
	maxy = max(brightness) * 1.1
	mean = (maxy + miny)/3
	ax.set_ylim([miny, maxy])

	if False:
	    plt.annotate(\
		'ZACHOD\nSLONCA',\
		xy=(600, mean), arrowprops=dict(arrowstyle='->'), xytext=(250, 0.6*mean))

	# random color
	colors = ['m', 'b', 'c', 'r', 'k', 'g']
	clr = random.choice(colors)
	
	plt.plot(times, brightness, clr)

	plt.xlabel('time')
	plt.ylabel('radiance')

        # number of ticks should depend on
	# covered time span
        formater = dates.DateFormatter('%H')
        hours = dates.HourLocator(interval = 1)
        minutes = dates.MinuteLocator(interval = 15)
        ax.xaxis.set_major_locator(hours)
        ax.xaxis.set_minor_locator(hours)
        ax.xaxis.set_major_formatter(formater)
        ax.tick_params(axis='x', which='both', bottom='off', top='off')

    fig.savefig(plotname)

    return plotname



def rgb_plot(foldername, plotname = 'rgbplot.png'):
    files = get_files(foldername)
    times = get_files_times(files)

    # Tic Toc
    tic = time.time()


    # OpenCV reads each file in BGR!
    R = []
    G = []
    B = []
    for file in files:
	img = cv2.imread(file)
	R.append(img[:,:,2].sum())
	G.append(img[:,:,1].sum())
	B.append(img[:,:,0].sum())
	if len(R)%50==5:
	    # Progress bar print
	    print int(time.time() - tic), '[s], files done:',\
		  len(R),'/',len(files)
	

    with plt.xkcd():
	# Based on "Stove Ownership" from XKCD by Randall Monroe
	# http://xkcd.com/418/

	fig = plt.figure()
	ax = fig.add_axes((0.1, 0.2, 0.8, 0.7))
	ax.spines['right'].set_color('none')
	ax.spines['top'].set_color('none')
	plt.xticks([])
	plt.yticks([])
	miny = min([min(R), min(G), min(B)])
	maxy = max([max(R), max(G), max(B)]) * 1.1
	mean = (maxy + miny)/3
	ax.set_ylim([miny, maxy])

	
	plt.plot(times, R, 'r')
	plt.plot(times, G, 'g')
	plt.plot(times, B, 'b')

	plt.legend(['Red', 'Green', 'Blue'], loc = 'upper left')

	plt.xlabel('time')
	plt.ylabel('saturation')

        # number of ticks should depend on
	# covered time span
        formater = dates.DateFormatter('%H')
        hours = dates.HourLocator(interval = 1)
        minutes = dates.MinuteLocator(interval = 15)
        ax.xaxis.set_major_locator(hours)
        ax.xaxis.set_minor_locator(hours)
        ax.xaxis.set_major_formatter(formater)
        ax.tick_params(axis='x', which='both', bottom='off', top='off')

    fig.savefig(plotname)

    return plotname
