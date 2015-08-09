from glob import glob
import time
import pickle
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import cv2


# Import all the photos into a list
images = []
files = glob('2015_08_08/*.jpg')
files = files[50:400]

# Should remember this
files.sort(key=os.path.getmtime)

# Load or recalculate
if False:
    t = time.time()
    brightnesses = []
    for file in files:
	img = cv2.imread(file)
	imgh = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	brightnesses.append(imgh[:,:,0].sum())
	if len(brightnesses)%20==4:
	    print time.time() -t, len(brightnesses)
    file = open('brightness.pickle', 'wb')
    pickle.dump(brightnesses, file)
else:
    file = open('brightness.pickle', 'rb')
    brightnesses = pickle.load(file)



with plt.xkcd():
    # Based on "Stove Ownership" from XKCD by Randall Monroe
    # http://xkcd.com/418/

    fig = plt.figure()
    ax = fig.add_axes((0.1, 0.2, 0.8, 0.7))
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    plt.xticks([])
    plt.yticks([])
    miny = min(brightnesses)
    maxy = max(brightnesses) * 1.1
    mean = (maxy + miny)/3
    ax.set_ylim([miny, maxy])

    plt.annotate(\
	'ZACHOD\nSLONCA',\
	xy=(600, mean), arrowprops=dict(arrowstyle='->'), xytext=(250, 0.6*mean))

    plt.plot(brightnesses)

    plt.xlabel('time')
    plt.ylabel('much light')

fig.savefig('suntrace.png')
