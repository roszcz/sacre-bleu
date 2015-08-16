from glob import glob
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import dates
import pickle
import random
import time
import datetime
import os
import cv2

def diffImg(t0, t1, t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_and(d1, d2)

def get_files(foldername):
    # Get sorted files
    files = glob(foldername + '/*.jpg')
    # Should remember this
    files.sort(key=os.path.getmtime)

    return files;

def make_diff_movie(foldername):

    files = get_files(foldername)

    for it in range(1,len(files)):
	t0 = cv2.imread(files[it-1])
	t1 = cv2.imread(files[it])
	g0 = cv2.cvtColor(t0, cv2.COLOR_BGR2GRAY)
	g1 = cv2.cvtColor(t1, cv2.COLOR_BGR2GRAY)
	g0 = cv2.GaussianBlur(g0, (21, 21), 0)
	g1 = cv2.GaussianBlur(g1, (21, 21), 0)
	delta = cv2.absdiff(g0,g1)
	thresh = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1]
	thresh = cv2.dilate(thresh, None, iterations=2)
	cv2.imwrite('crap/' + files[it], thresh)
	print it, files[it]



def last_hour_plot(foldername, calculate = True,\
                   plotname = 'movements.png',\
                   N = 120):

    files = get_files(foldername)
    # Randomly expand time
    N += random.randint(0,90)

    # Get file creation times for x-axis
    times = []
    for file in files:
        t = os.path.getmtime(file)
        dtime = datetime.datetime.fromtimestamp(t)
        times.append(dtime)

    # Cut files to last N files
    files = files[-N:]
    times = times[-N:]

    # tic toc mechanism
    t = time.time()

    if calculate:
        movements = []
        for it in range(1, N-1):
            img0 = cv2.imread(files[it-1])
            gray0 = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)
            img1 = cv2.imread(files[it])
            gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            img2 = cv2.imread(files[it+1])
            gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
            if (it%20==3):
                print it, time.time() - t

            movimage = diffImg(img0, img1, img2)
            movements.append(movimage.sum())
    else:
        # FIXME - no saving mechanism
        file = open('move.pickle','rb')
        movements = pickle.load(file)


    with plt.xkcd():
        # Based on "Stove Ownership" from XKCD by Randall Monroe
        # http://xkcd.com/418/

        fig = plt.figure()
        ax = fig.add_axes((0.1, 0.2, 0.8, 0.7))
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
    #    plt.xticks([times[0],times[-1]])
        miny = min(movements)*0.9
        maxy = max(movements)*1.1
        mean = (maxy + miny)/3.
        plt.yticks([])
        ax.set_ylim([miny, maxy])

	# random color
	colors = ['m', 'b', 'c', 'r', 'k', 'g']
	clr = random.choice(colors)

        plt.plot(times[1:-1], movements, clr)

        plt.xlabel('time')
        plt.title('RECENT CELESTIAL ACTIVITY')
        plt.ylabel('action')

        # number of ticks?
        formater = dates.DateFormatter('%H:%M')
        hours = dates.HourLocator()
        minutes = dates.MinuteLocator(interval = 15)
        ax.xaxis.set_major_locator(minutes)
        ax.xaxis.set_minor_locator(minutes)
        ax.xaxis.set_major_formatter(formater)
        ax.tick_params(axis='x', which='both', bottom='off', top='off')

    #plt.show()
    fig.savefig(plotname)
    return plotname
