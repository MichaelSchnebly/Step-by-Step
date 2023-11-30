import numpy as np
from scipy.spatial.transform import Rotation as R
from OpenGL.arrays import vbo

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
        self.timepoints = np.arange(n_frames, dtype=np.float32)
        self.data = np.zeros((n_frames, 3), dtype=np.float32)
        self.labels = np.zeros((n_frames, 2), dtype=np.uint8)
        self.labels[:, 0] = 1
        
    def update(self, frame):
        self.update_data(frame)

    def update_data(self, frame):
        self.data[1:, :] = self.data[:-1, :]
        self.data[0, :] = frame

    def update_labels(self):
        self.labels[1:, :] = self.labels[:-1, :]
