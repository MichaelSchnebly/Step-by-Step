import serial
import time
import struct

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
# SERIAL_PORT = '/dev/cu.usbmodem14601'  # Update this with your serial port
SERIAL_PORT = '/dev/cu.usbserial-028574DD'
BAUD_RATE = 1000000              # Update this with your baud rate

ser = serial.Serial(SERIAL_PORT, BAUD_RATE)

try:
    t = time.time()
    n = 0
    while True:
        if ser.in_waiting > 0:
            data_bytes = ser.read(4 + 11 * 4)
            data = Data.from_bytes(data_bytes)
            # data.print()
            
            n += 1
            if n == 100:
                print("Hz:", 100/(time.time()-t))
                t = time.time()
                n = 0




except KeyboardInterrupt:
    ser.close()
    print("Serial connection closed.")