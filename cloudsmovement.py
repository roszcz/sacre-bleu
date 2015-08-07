from glob import glob
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pickle
import time
import os
import cv2

# Get sorted files
files = glob('2015_08_07/*.jpg')
# Should remember this
files.sort(key=os.path.getmtime)

def diffImg(t0, t1, t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_and(d1, d2)

# tic toc mechanism
t = time.time()

if False:
    movements = []
    # FIXME ugly loop | not really
    N = len(files)
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

file = open('move.pickle','rb')
movements = pickle.load(file)

with plt.xkcd():
    # Based on "Stove Ownership" from XKCD by Randall Monroe
    # http://xkcd.com/418/

    fig = plt.figure()
    ax = fig.add_axes((0.1, 0.2, 0.8, 0.7))
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    plt.xticks([])
    plt.yticks([])
    miny = min(movements)
    maxy = max(movements)
    mean = (maxy + miny)/3.
    ax.set_ylim([miny, maxy])
    plt.annotate(\
	'mucha?',\
	xy=(190, mean), arrowprops=dict(arrowstyle='->'), xytext=(250, 1.6*mean))

    plt.plot(movements, 'm')

    plt.xlabel('time')
    plt.ylabel('movement\ndetection')

fig.savefig('movements.png')
