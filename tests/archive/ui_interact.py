import matplotlib.pyplot as plt
from matplotlib.widgets import Button

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)  # Adjust subplot to make room for the button

def on_button_click(event):
    # Your code here, e.g., update the plot
    ax.plot([1, 2, 3], [2, 3, 4], 'ro-')  # Example action
    plt.draw()

# Create the button and position it
button_ax = plt.axes([0.7, 0.05, 0.2, 0.075])  # x, y, width, height
button = Button(button_ax, 'Click Me')
button.on_clicked(on_button_click)

plt.show()