import serial
import struct
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

# Initial line points (default values)
line_points = [0.0, 0.0, 1.0, 1.0] #, 2.0, 3.0]

def draw_line():
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_LINES)
    glVertex2f(line_points[0], line_points[1])
    glVertex2f(line_points[2], line_points[3])
    # glVertex2f(line_points[2], line_points[3])
    # glVertex2f(line_points[4], line_points[5])
    glEnd()
    glutSwapBuffers()

def keyboard(key, x, y):
    global running
    if key == b'q' or key == b'Q':  # Press 'q' or 'Q' to quit
        ser.close()
        running = False
        glutLeaveMainLoop()  # Only works if freeglut is installed

def update_line(_):
    global line_points

    # Read data from the serial port
    if ser.in_waiting > 0:
        data_bytes = ser.read(4 + 11 * 4)
        data = Data.from_bytes(data_bytes)
        line_points[2] = data.ox
    #     line_points[3] = data.ay

        glutPostRedisplay()
        glutTimerFunc(10, update_line, 0)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"OpenGL Line Update from Serial Data")

    # Set up basic OpenGL settings
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Set background color
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-10, 10, -10, 10, -1, 1)       # Define the coordinate system
    glMatrixMode(GL_MODELVIEW)


    glutDisplayFunc(draw_line)
    glutKeyboardFunc(keyboard)  # Register keyboard event handler
    glutTimerFunc(10, update_line, 0)
    glutMainLoop()

if __name__ == "__main__":
    main()