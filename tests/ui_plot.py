import matplotlib.pyplot as plt
import numpy as np
import time

# Initialize the plot
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot(xdata, ydata, 'r-')

def update_line(x, y):
    ln.set_data(x, y)
    ax.relim()  # Recalculate limits
    ax.autoscale_view(True, True, True)  # Rescale view
    plt.draw()
    plt.pause(0.01)  # Pause to update the plot

# Main loop to update the line
while True:
    # Your code to get new x, y data
    # Example: appending new data
    xdata.append(np.random.random())
    ydata.append(np.random.random())

    update_line(xdata, ydata)

    # Ensure loop runs at about 100Hz
    time.sleep(0.01)