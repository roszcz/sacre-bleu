import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import dates

class Plot(object):
    def __init__(self, times, data):
        self.times = times
        self.data = data
        self.savename = 'plot.png'
        self.ylabel = 'VALUES'
        # In case You forget
        self.legend = ''
        self.colors = ['r', 'g', 'b']

        # Inits
        self.init_date_formatter()

    def init_date_formatter(self):
        # Divide cleverly
        # Get datetime.timedelta duration:
        timed = self.times[-1] - self.times[0]

        # Calculate hours and minutes
        hours, remainder = divmod(timed.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        # Switch-like haxor solution
        if hours < 1:
            # Shortest possible in the time domain
            formater = '%M'
            major = dates.MinuteLocator(interval = 10)
            minor = dates.MinuteLocator(interval = 3)
        elif hours < 3:
            formater = '%H:%M'
            major = dates.MinuteLocator(interval = 20)
            minor = dates.MinuteLocator(interval = 10)
        elif hours < 10:
            formater = '%H'
            major = dates.HourLocator(interval = 2)
            minor = dates.HourLocator(interval = 1)
        elif hours < 20:
            formater = '%H'
            major = dates.HourLocator(interval = 2)
            minor = dates.HourLocator(interval = 1)
        else:
            formater = '%H'
            major = dates.HourLocator(interval = 1)
            minor = dates.HourLocator(interval = 1)

        self.formater = dates.DateFormatter(formater)
        self.major_formatter = major
        self.minor_formatter = minor

    def set_ylabel(self, label):
        self.ylabel = label

    def set_legend(self, legend):
        self.legend = legend

    def set_colors(self, colors):
        self.colors = colors

    def make_figure(self, filename):
        with plt.xkcd():
            # This is common for all 2d plots
            fig = plt.figure()
            ax = fig.add_axes((0.1, 0.2, 0.8, 0.7))
            ax.spines['right'].set_color('none')
            ax.spines['top'].set_color('none')
            plt.xticks([])

            # data might be 2D so we have to go deeper ...
            miny = round(self.data.min()) * 0
            maxy = round(self.data.max())
            mean = (maxy + miny)/2
            # ... to set proper axis limits
            ax.set_ylim([miny, maxy * 1.1])
            plt.yticks([miny, mean, maxy])

            # This might come in handy for some awful jokes
            # plt.annotate(\
            #         'ZACHOD\nSLONCA',\
            #         xy=(600, mean),
            #         arrowprops=dict(arrowstyle='->'),
            #         xytext=(250, 0.6*mean))

            colors = ['m', 'b', 'c', 'r', 'k', 'g']

            # Single line case:
            if len(self.data.shape) is 1:
                # For single line plots we want a random color 
                clr = random.choice(colors)
                plt.plot(self.times, self.data, clr)

            else:
                # We need to iterate over columns, so transpose
                for it, line in enumerate(self.data.transpose()):
                    plt.plot(self.times, line, self.colors[it])

                # Provide legend
                plt.legend(self.legend, loc = 'upper left')

            # Label the labels
            plt.xlabel('TIME')
            plt.ylabel(self.ylabel)

            # number of ticks should depend on
            # covered time span
            ax.xaxis.set_major_locator(self.major_formatter)
            ax.xaxis.set_minor_locator(self.minor_formatter)
            # TODO minor_formatter might also look cool
            ax.xaxis.set_major_formatter(self.formater)
            ax.tick_params(axis='x', which='both', bottom='off', top='off')
            ax.tick_params(axis='y', which='both',
                           bottom='off', top='off',
                           left='off', right='off')

        fig.savefig(filename)

def make_rgb_plot(times, vals):
    """ Takes data and returns filename """
    filename = 'rgb.png'
    plot = Plot(times, vals)
    plot.set_colors(['r', 'g', 'b'])
    plot.set_legend(['Red', 'Green', 'Blue'])
    plot.set_ylabel('VALUE\nPER PIXEL')

    plot.make_figure(filename)

    return filename

def make_hsv_plot(times, vals):
    """ this is proper folding comment for method description """
    filename = 'hsv.png'
    plot = Plot(times, vals)
    plot.set_colors(['m', 'c', '#007071'])
    plot.set_legend(['Hue', 'Saturation', 'Value'])
    plot.set_ylabel('VALUE\nPER PIXEL')

    plot.make_figure(filename)

    return filename

def make_brightness_plot(times, vals):
    """ Takes data and returns a filename """
    filename = 'brighness.png'
    plot = Plot(times, vals)
    plot.set_legend('Brightness')
    plot.set_ylabel('VALUE\nPER PIXEL')

    plot.make_figure(filename)

    return filename
