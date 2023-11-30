import queue
import threading
import time
import serial
import numpy as np


class IMUStream:
    '''A class to represent a stream of data.
        -The stream is a queue of sensor values.
        -This queue is updated by a thread that reads from the serial port.
        -Optionally, the thread can write to a file.
        -Instead of reading from the serial port, the thread can read from a previously recorded file.
        '''
    def __init__(self, port, baud_rate, file_name="tmp.bin", record=False, read_file=False):
        self.port = port
        self.baud_rate = baud_rate
        self.file_name = file_name
        self.record = record
        self.data_queue = queue.Queue()
        self.frame_count = 0
        self.last_time = time.time()

        if read_file:
            self.thread = threading.Thread(target=self.read_file, daemon=True)
        else:
            self.thread = threading.Thread(target=self.read_serial, daemon=True)

        self.thread.start()

    def read_serial(self):
        '''Reads from the serial port and writes to a file if recording is enabled.'''
        if self.record:
            self.file = open(self.file_name, 'wb')
        with serial.Serial(self.port, self.baud_rate) as ser:
            while True:
                if ser.in_waiting > 0:
                    data_bytes = ser.read(36)
                    if self.record:
                        self.file.write(data_bytes)
                    self.data_queue.put(data_bytes)
                else:
                    time.sleep(0.005)

    def read_file(self):
        '''Reads from a previously recorded file. Sleeps to simulate real-time 100Hz.'''
        with open(self.file_name, 'rb') as file:
            while True:
                data_bytes = file.read(36)
                if not data_bytes:
                    break
                self.data_queue.put(data_bytes)
                time.sleep(0.01)

    def get_frame(self):
        '''Returns the next data frame from the stream.'''
        if not self.data_queue.empty():
            self.frame_count += 1
            frame = np.frombuffer(self.data_queue.get(), dtype=np.float32).reshape(3, 3)
            return frame.copy(), self._report_fps()
        return None, self._report_fps()
    
    def _report_fps(self):
        '''Reports the current frames per second.'''
        current_time = time.time()
        if current_time - self.last_time >= 1.0:
            fps = self.frame_count / (current_time - self.last_time)
            self.last_time = current_time
            self.frame_count = 0
            return fps
        return None
    
    def close(self):
        '''Closes the serial connection and file.'''
        self.ser.close()
        print("Serial connection closed.")
        if self.record:
            self.file.close()
            print("File closed.")
        