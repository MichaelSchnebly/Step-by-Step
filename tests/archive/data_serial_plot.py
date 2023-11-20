import serial
import time
import struct
import numpy as np
import time

import pygame
import sys

# Initialize Pygame
pygame.init()
# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Line Drawing")

x, y = np.arange(100, dtype=np.int32), np.zeros(100, dtype=np.int32)
x *= int(width/len(x))


# # Initialize the plot
# plt.ion()  # Turn on interactive mode
# fig, ax = plt.subplots()
# ax.set_ylim(-1, 1)
# ax.set_xlim(0, 100)

# ln, = plt.plot(x, y, 'r-')

def update_line(x, y):
    screen.fill((0, 0, 0))  # Clear screen with black
    points = [tuple(i) for i in zip(x, y)]
    pygame.draw.lines(screen, (255, 255, 255), False, points, 1)
    pygame.display.flip()  # Update the display



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
                "AX: ", f"{self.ax: 4.2f}", " ",
                "AY: ", f"{self.ay: 4.2f}", " ",
                "AZ: ", f"{self.az: 4.2f}", " ",
                "A: ", f"{self.a: 4.2f}", " ",
                "GX: ", f"{self.gx: 4.2f}", " ",
                "GY: ", f"{self.gy: 4.2f}", " ",
                "GZ: ", f"{self.gz: 4.2f}", " ",
                "G: ", f"{self.g: 4.2f}", " ",
                "OX: ", f"{self.ox: 4.2f}", " ",
                "OY: ", f"{self.oy: 4.2f}", " ",
                "OZ: ", f"{self.oz: 4.2f}")
        

    @classmethod
    def from_bytes(self, data_bytes):
        # Unpack the received bytes according to the data structure
        unpacked_data = struct.unpack('B11f', data_bytes)
        return self(*unpacked_data)


# Serial port configuration
SERIAL_PORT = '/dev/cu.usbmodem14601'  # Update this with your serial port
BAUD_RATE = 115200              # Update this with your baud rate

ser = serial.Serial(SERIAL_PORT, BAUD_RATE)

try:
    t = time.time()
    n = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if ser.in_waiting > 0:
                data_bytes = ser.read(4 + 11 * 4)
                data = Data.from_bytes(data_bytes)
                # data.print()
                
                n += 1
                if n == 100:
                    print("Hz:", 100/(time.time()-t))
                    t = time.time()
                    n = 0

                y[1:] = y[:-1]
                y[0] = (1-data.ox)*height/2

                if n % 10 == 0:
                    update_line(x, y)





except KeyboardInterrupt:
    pygame.quit()
    ser.close()
    print("Serial connection closed.")