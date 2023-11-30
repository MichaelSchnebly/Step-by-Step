import math
import numpy as np
import glm
from scipy.spatial.transform import Rotation as R
from OpenGL.arrays import vbo


class IMUPlot:
    '''A class to represent information about an IMU plot.
        -The plot is a collection of polylines.
        -The polylines are updated by frames returned from a stream (serial port or file).
        -The polylines are stored as a list.
        -The polylines are rendered by a renderer.
        -The renderer is stored as a LineRenderer object.
    '''
    def __init__(self, n_frames):
        self.polylines = [Polyline(n_frames, 0.001, np.array([0, 1,   1, 1]), [1, 1/12, 1], [0, -7/12, 0]),      #acceleration.x
                          Polyline(n_frames, 0.001, np.array([1, 0,   1, 1]), [1, 1/12, 1], [0, -9/12, 0]),        #acceleration.y
                          Polyline(n_frames, 0.001, np.array([1, 0.6, 0, 1]), [1, 1/12, 1], [0, -11/12, 0]),     #acceleration.z
                          Polyline(n_frames, 0.004, np.array([1, 1,   1, 1]), [1, 1/3, 1], [0, -6/12, 0])           #acceleration.mag
                          ]
    
    def update(self, data):
        self.polylines[0].update(data[0])
        self.polylines[1].update(data[1])
        self.polylines[2].update(data[2])
        self.polylines[3].update(np.linalg.norm(data))


class Polyline:
    def __init__(self, n_frames, width = 0.002, color = np.ones(4, dtype=np.float32), scale = [1, 1, 1], translate = [0, 0, 0]):
        self.vertices = np.zeros((n_frames, 3), dtype=np.float32)
        self.vertices[:, 0] = np.linspace(-1, 1, n_frames)
        self.vertices[:, 1] = np.zeros(n_frames)
        self.vertices[:, 2] = np.zeros(n_frames)

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


