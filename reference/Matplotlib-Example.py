import numpy as np
import matplotlib.pyplot as plt
# FuncAnimation class allows you to make animations by repeatedly calling my function
from matplotlib.animation import FuncAnimation

# store list objects for x-values
x_data = []
# store list object for y-values
y_data = []

"""
class matplotlib.animation.FuncAnimation(fig, func, 
    frames=None, init_func=None, fargs=None, save_count=None, *, cache_frame_data=True, **kwargs)
"""

fig, ax = plt.subplots()
ax.set_xlim(0, 105)
ax.set_ylim(0, 12)

# This will be my standard point
line, = ax.plot(0, 0)

# take in any parameters, so pass in i parameter to take in any integers
def animation_frame(i):
    # append value every time we add a new value to the x_data list
    x_data.append(i * 10)
    # for y_data list, append the y value
    y_data.append(i)

    # take the line object
    # update x_data & y_data lists
    line.set_xdata(x_data)
    line.set_ydata(y_data)
    # return line, object
    return line, 

# pass this function into the FuncAnimation class
# when we increase the frame by one frame, we want to increase the value by 1
# from the x_data and y_data list, we want to append a new value every time we call the animation_frame() function

# here provide list into frames
# interval parameter is time delay between each frame
# fire every frame each 10 ms

# create animation class instance
# pass in animation_frame function into 'func' class

# going to provide a frames value into the frames parameter
# interval parameter is the time delay between each frame
# animation = FuncAnimation(fig, func=animation_frame, frames=np.arange(0, 10, 0.01), interval=10)
animation = FuncAnimation(fig, func=animation_frame, frames=np.arange(0, 10, 1), interval=10)

# lastly, we show the plot
plt.show()