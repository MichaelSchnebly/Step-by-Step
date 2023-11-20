import serial
import struct
import threading
import queue
import time

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
        unpacked_data = struct.unpack('B11f', data_bytes)
        return self(*unpacked_data)

class SerialReader:
    def __init__(self, port, baud_rate):
        self.ser = serial.Serial(port, baud_rate)
        self.data_queue = queue.Queue()
        self.frame_count = 0
        self.last_time = time.time()
        self.thread = threading.Thread(target=self.read_serial, daemon=True)
        self.thread.start()

    def read_serial(self):
        while True:
            if self.ser.in_waiting > 0:
                data_bytes = self.ser.read(4 + 11 * 4)
                self.data_queue.put(data_bytes)
            else:
                time.sleep(0.005)

    def get_data(self):
        if not self.data_queue.empty():
            self.frame_count += 1
            return Data.from_bytes(self.data_queue.get()), self._report_fps()
        return None, self._report_fps()
    
    def _report_fps(self):
        current_time = time.time()
        if current_time - self.last_time >= 1.0:  # Every second
            fps = self.frame_count / (current_time - self.last_time)
            # print(f"FPS: {fps:.2f}")
            self.last_time = current_time
            self.frame_count = 0
            return fps
        return None
    
    def close(self):
        self.ser.close()
        print("Serial connection closed.")
        return