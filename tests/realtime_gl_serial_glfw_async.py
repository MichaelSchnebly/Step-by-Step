import serial
import struct
import time
import numpy as np
import glfw
from OpenGL.GL import *
from OpenGL.arrays import vbo

import threading
import queue

# Serial port setup
# SERIAL_PORT = '/dev/cu.usbmodem14601'  # Update this with your serial port
SERIAL_PORT = '/dev/cu.usbserial-028574DD'
BAUD_RATE = 1000000  # Update this with your baud rate
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)

data_queue = queue.Queue()

def read_serial():
    while True:
        if ser.in_waiting > 0:
            data_bytes = ser.read(4 + 11 * 4)
            data_queue.put(data_bytes)
        else:
            time.sleep(0.005)  # Small delay to prevent CPU overuse

# Start the serial reading in a separate thread
serial_thread = threading.Thread(target=read_serial, daemon=True)
serial_thread.start()


class Data:
    def __init__(self, channel, ax, ay, az, a, gx, gy, gz, g, ox, oy, oz):
        self.channel = channel
        self.ax = ax
        self.ay = ay
        self.az = az
        self.a = a
        self.gx = gx
        self.gy = gy
        self.gz = gz
        self.g = g
        self.ox = ox
        self.oy = oy
        self.oz = oz

    @classmethod
    def from_bytes(self, data_bytes):
        # Unpack the received bytes according to the data structure
        unpacked_data = struct.unpack('B11f', data_bytes)
        return self(*unpacked_data)


# Initialize GLFW
if not glfw.init():
    raise Exception("GLFW can't be initialized")

# Create a GLFW window
window = glfw.create_window(800, 600, "Oscillating Sine Wave with VBO", None, None)
if not window:
    glfw.terminate()
    raise Exception("GLFW window can't be created")

glfw.make_context_current(window)
# glfw.swap_interval(1)  # Disable VSync


# Number of points in the sine wave
NUM_POINTS = 400

# Initialize VBO with dummy data
sine_wave_vbo = vbo.VBO(np.zeros((NUM_POINTS, 2), dtype='f'))

x = np.linspace(-1, 1, NUM_POINTS)
y = np.zeros(NUM_POINTS)
t = time.time()
n = 0


def init_gl():
    """ Initialize OpenGL state """
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Set clear color


def update_sine_wave(phase):
    """ Update the sine wave points for the VBO """
    
    while not data_queue.empty():
        data_bytes = data_queue.get()
        data = Data.from_bytes(data_bytes)
        y[1:] = y[:-1]
        y[0] = data.ox

    render_data = np.column_stack((x, y))
    sine_wave_vbo.set_array(render_data.astype('f'))


def display():
    """ Display callback for GLFW """
    global t, n
    glClear(GL_COLOR_BUFFER_BIT)

    glLineWidth(5.0)  # Set the line width

    sine_wave_vbo.bind()
    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointer(2, GL_FLOAT, 0, sine_wave_vbo)
    glDrawArrays(GL_LINE_STRIP, 0, NUM_POINTS)
    glDisableClientState(GL_VERTEX_ARRAY)
    sine_wave_vbo.unbind()

    glfw.swap_buffers(window)


# Main loop
init_gl()
# frame_duration = 1 / 120  # Target frame duration for 100 FPS

while not glfw.window_should_close(window):
    # start_time = time.time()  # Get the start time of the frame

    glfw.poll_events()
    update_sine_wave(time.time())  # Pass the current time as the phase
    display()

    n += 1
    if n == 100:
        print("Hz:", 100 / (time.time() - t))
        t = time.time()
        n = 0

    # Calculate how long to sleep to maintain the target frame rate
    # time_to_sleep = frame_duration - (time.time() - start_time)
    # if time_to_sleep > 0:
    #     time.sleep(time_to_sleep)



ser.close()
print("Serial connection closed.")
glfw.terminate()
