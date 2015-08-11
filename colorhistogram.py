from glob import glob
from random import random
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import cv2
import pickle
from sklearn.cluster import KMeans

def centroid_histogram(clt):
    # grab the number of different clusters and create a histogram
    # based on the number of pixels assigned to each cluster
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins = numLabels)

    # normalize the histogram, such that it sums to one
    #hist = hist.astype("float")
    #hist /= hist.sum()

    # return the histogram
    return hist

def plot_colors(hist, centroids):
    # initialize the bar chart representing the relative frequency
    # of each of the colors
    bar = np.zeros((50, 300, 3), dtype = "uint8")
    startX = 0

    # loop over the percentage of each cluster and the color of
    # each cluster
    for (percent, color) in zip(hist, centroids):
            # plot the relative percentage of each cluster
            endX = startX + (percent * 300)
            cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                    color.astype("uint8").tolist(), -1)
            startX = endX

    # return the bar chart
    return bar

def make_histogram(picpath, plotname = 'colors.png', clusters = 5):
    img_full = cv2.imread(picpath)
    # Cut buildings
    img = img_full[0:800,:,:]
    small = cv2.resize(img, (0,0), fx=0.3, fy=0.3)
    small = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)
    small = small.reshape((small.shape[0] * small.shape[1],3))

    clt = KMeans(n_clusters=clusters)
    clt.fit(small)
    colors = clt.cluster_centers_
    # Normalize colors for matplotlib rgb 0-1 style
    colors = colors/255.
    hist = centroid_histogram(clt)
    paint_histo(hist, colors, plotname)

    return plotname

def paint_histo(histogram, colors, plotname):

    with plt.xkcd():
        fig = plt.figure()
        ax = fig.add_axes((0.1, 0.2, 0.8, 0.7))

        # Custom color bars
        for it, scor in enumerate(histogram):
            ax.bar([it - 0.3], scor, 0.6, color=colors[it])

        # What
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.set_xticks([])
    #    ax.set_xlim([-0.5, 1.5])
        #ax.set_ylim([0, 110])
        plt.yticks([])

        plt.title(" ")

        fig.text(
            0.5, 0.05,
            'dominant colors',
            ha='center')

    fig.savefig(plotname)
    #plt.show()
