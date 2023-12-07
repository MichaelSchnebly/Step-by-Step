import threading
import time
import queue
import numpy as np
import serial

class IMUStream:
    def __init__(self, port, baud_rate, file_name="data/recordings/imu.bin", record=False, read_file=False):
        self.port = port
        self.baud_rate = baud_rate
        self.file_name = file_name
        self.record = record
        self.read_file_flag = read_file
        self.data_queue = queue.Queue()
        self.frame_count = 0
        self.last_time = time.time()

        self.running = False

    def start(self):
        if not self.running:
            self.running = True
            if self.read_file_flag:
                self.thread = threading.Thread(target=self.read_file, daemon=True)
            else:
                self.thread = threading.Thread(target=self.read_serial, daemon=True)
            self.thread.start()

    def stop(self):
        if self.running:
            self.running = False
            self.thread.join()

    def read_serial(self):
        if self.record:
            self.file = open(self.file_name, 'wb')
        with serial.Serial(self.port, self.baud_rate) as ser:
            while self.running:
                if ser.in_waiting > 0:
                    data_bytes = ser.read(36)
                    if self.record:
                        self.file.write(data_bytes)
                    self.data_queue.put(data_bytes)
                else:
                    time.sleep(0.005)
        if self.record:
            self.file.close()

    def read_file(self):
        with open(self.file_name, 'rb') as file:
            while self.running:
                data_bytes = file.read(36)
                if not data_bytes:
                    break
                self.data_queue.put(data_bytes)
                time.sleep(0.01)

    def get_frame(self):
        if not self.data_queue.empty():
            self.frame_count += 1
            frame = np.frombuffer(self.data_queue.get(), dtype=np.float32).reshape(3, 3)
            return frame.copy(), self._report_fps()
        return None, self._report_fps()
    
    def _report_fps(self):
        current_time = time.time()
        if current_time - self.last_time >= 1.0:
            fps = self.frame_count / (current_time - self.last_time)
            self.last_time = current_time
            self.frame_count = 0
            return fps
        return None