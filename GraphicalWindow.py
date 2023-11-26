import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from matplotlib.animation import FuncAnimation
import random

class GraphicalWindow():
    def __init__(self, dataConnection):
        #pass in serial connection object
        fig, ax = plt.subplots()
        xdata, ydata = [], []
        ln, = ax.plot([], [], 'ro')
        # ydata is intialized w/ integers
        self.ydata = [0.0,2.0,4.0,8.0,10.0,12.0,14.0]
        self.dataConnection = dataConnection

        def init():
            ax.set_xlim(0, 2*np.pi)
            ax.set_ylim(0, 14)
            return ln,

        def update(i):
            xdata=[0,1,2,3,4,5,6]
            #xdata.append(frame)
            #ydata.append(np.sin(frame))
            ydata = self.ydata
            ydata = ydata[1:]
            # actually using ydata to get latest value
            ydata.append(self.dataConnection.getLatestValue())
            self.ydata = ydata
            ln.set_data(xdata, ydata)
            return ln,

        ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 128),
                            init_func=init, blit=True)
        plt.show()
