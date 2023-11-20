import serial
import struct
import time
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo


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

    def print(self):
        print("CHANNEL: ", self.channel, " ",
                "AX: ", f"{self.ax: 4.2f}", " ")
                # "AY: ", f"{self.ay: 4.2f}", " ",
                # "AZ: ", f"{self.az: 4.2f}", " ",
                # "A: ", f"{self.a: 4.2f}", " ",
                # "GX: ", f"{self.gx: 4.2f}", " ",
                # "GY: ", f"{self.gy: 4.2f}", " ",
                # "GZ: ", f"{self.gz: 4.2f}", " ",
                # "G: ", f"{self.g: 4.2f}", " ",
                # "OX: ", f"{self.ox: 4.2f}", " ",
                # "OY: ", f"{self.oy: 4.2f}", " ",
                # "OZ: ", f"{self.oz: 4.2f}")
        

    @classmethod
    def from_bytes(self, data_bytes):
        # Unpack the received bytes according to the data structure
        unpacked_data = struct.unpack('B11f', data_bytes)
        return self(*unpacked_data)

# Serial port setup
SERIAL_PORT = '/dev/cu.usbmodem14601'  # Update this with your serial port
BAUD_RATE = 115200              # Update this with your baud rate
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)


# Number of points in the sine wave
NUM_POINTS = 100

global x, y, t, n
x = np.linspace(-1, 1, NUM_POINTS)
y = np.zeros(NUM_POINTS)
t = time.time()
n = 0

# Initialize VBO with dummy data
sine_wave_vbo = vbo.VBO(np.zeros((NUM_POINTS, 2), dtype='f'))

def init_gl():
    """ Initialize OpenGL state """
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Set clear color

def update_sine_wave(phase):
    """ Update the sine wave points for the VBO """
    # y = np.sin(2 * np.pi * x + phase)
    y[1:] = y[:-1]
    if ser.in_waiting > 0:
        data_bytes = ser.read(4 + 11 * 4)
        data = Data.from_bytes(data_bytes)
        y[0] = data.ax

        global n, t
        n += 1
        if n == 100:
            print("Hz:", 100/(time.time()-t))
            t = time.time()
            n = 0

    data = np.column_stack((x, y))
    sine_wave_vbo.set_array(data.astype('f'))

    

def display():
    """ Display callback for GLUT """
    glClear(GL_COLOR_BUFFER_BIT)

    sine_wave_vbo.bind()
    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointer(2, GL_FLOAT, 0, sine_wave_vbo)
    glDrawArrays(GL_LINE_STRIP, 0, NUM_POINTS)
    glDisableClientState(GL_VERTEX_ARRAY)
    sine_wave_vbo.unbind()

    glutSwapBuffers()

def timer(value):
    """ Timer callback for GLUT """
    update_sine_wave(value / 20.0)  # Update phase based on time
    glutPostRedisplay()
    glutTimerFunc(16, timer, value + 1)  # Aim for ~60 FPS

def keyboard(key, x, y):
    global running
    if key == b'q' or key == b'Q':  # Press 'q' or 'Q' to quit
        ser.close()
        print("Serial connection closed.")
        running = False
        glutLeaveMainLoop()  # Only works if freeglut is installed

def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Oscillating Sine Wave with VBO")

    init_gl()

    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)  # Register keyboard event handler
    glutTimerFunc(16, timer, 0)  # Start the timer for the first time

    glutMainLoop()

if __name__ == "__main__":
    main()