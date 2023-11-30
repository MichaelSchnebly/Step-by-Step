import numpy as np
from scipy.spatial.transform import Rotation as R
from OpenGL.arrays import vbo

from modules.data_stream import Stream

# Function to create a translation matrix
def translation_matrix(tx, ty, tz):
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [tx, ty, tz, 1]
    ], dtype=np.float32)

# Function to create a scaling matrix
def scaling_matrix(sx, sy, sz):
    return np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)

class Polyline:
    def __init__(self, width = 0.002, color = np.ones(4, dtype=np.float32), scale = [1, 1, 1], translate = [0, 0, 0]):
        self.width = width
        self.color = color
        self.transform = np.eye(4, dtype=np.float32)
        self.transform = np.dot(self.transform, scaling_matrix(scale[0], scale[1], scale[2]))
        self.transform = np.dot(self.transform, translation_matrix(translate[0], translate[1], translate[2]))
        self.vbo = vbo.VBO(self.vertices)

    def update(self, value):
        self.vertices[1:, 1] = self.vertices[:-1, 1]
        self.vertices[0, 1] = value
        self.vbo.set_array(self.vertices)

class IMUPlot:
    '''A class to represent information about an IMU plot.
        -The plot is a collection of polylines.
        -The polylines are updated by frames returned from a stream (serial port or file).
        -The polylines are stored as a list.
        -The polylines are rendered by a renderer.
        -The renderer is stored as a LineRenderer object.
    '''
    def __init__(self):
        self.polylines = [Polyline(0.002, np.array([1, 1, 1, 1]), [1, 1/3, 1], [0, 2/3, 0]),      #acceleration.x
                          Polyline(0.002, np.array([1, 1, 1, 1]), [1, 1/3, 1], [0, 0, 0]),        #acceleration.y
                          Polyline(0.002, np.array([1, 1, 1, 1]), [1, 1/3, 1], [0, -2/3, 0]),     #acceleration.z
                          Polyline(0.002, np.array([1, 1, 1, 1]), [1, 1, 1], [0, 0, 0])           #acceleration.mag
                          ]
        self.renderer = PolylineRenderer(self.polylines)

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
        self.plot = IMUPlot()

        self.stream = Stream('/dev/cu.usbserial-028574DD', 1000000, record=False, read_file=False)

        # self.polylines = [Polyline(0.002, np.array([1, 1, 1, 1]), [1, 1/3, 1], [0, 2/3, 0]),      #acceleration.x
        #                   Polyline(0.002, np.array([1, 1, 1, 1]), [1, 1/3, 1], [0, 0, 0]),        #acceleration.y
        #                   Polyline(0.002, np.array([1, 1, 1, 1]), [1, 1/3, 1], [0, -2/3, 0]),     #acceleration.z
        #                   Polyline(0.002, np.array([1, 1, 1, 1]), [1, 1, 1], [0, 0, 0])           #acceleration.mag
        #                   ]

    def update(self, frame):
        self.labels[1:, :] = self.labels[:-1, :]
        self.data[1:, :] = self.data[:-1, :]
        self.data[0, :] = frame