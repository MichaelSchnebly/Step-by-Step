import numpy as np

class IMUData:
    '''A class to represent IMU data.
        -The data is a timeseries of sensor values.
        -This timeseries is updated by frames returned from a stream (serial port or file).
        -The timeseries is stored as a numpy array.
        -Data Indices:
            -[#, :] timepoint
            -[:, 0] acceleration x-axis
            -[:, 1] acceleration y-axis
            -[:, 2] acceleration z-axis
        -Label Indices:
            -[#, :] timepoint
            -[:, 0] no gesture
            -[:, 1] gesture
    '''
    def __init__(self, n_frames):
        self.data = np.zeros((n_frames, 3), dtype=np.float32)
        
    def update(self, frame):
        self.update_data(frame)

    def update_data(self, frame):
        self.data[1:, :] = self.data[:-1, :]
        self.data[0, :] = frame
