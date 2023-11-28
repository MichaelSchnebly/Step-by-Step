import numpy as np
import glm
from scipy.spatial.transform import Rotation as R
from OpenGL.arrays import vbo

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



class PolylineData:
    def __init__(self, num_points, width = 0.002, color = np.ones(4, dtype=np.float32), scale = [1, 1, 1], translate = [0, 0, 0]):
        self.vertices = np.zeros((num_points, 3), dtype=np.float32)
        self.vertices[:, 0] = np.linspace(-1, 1, num_points)
        self.vertices[:, 1] = np.zeros(num_points)
        self.vertices[:, 2] = np.zeros(num_points)

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


class LineData2D:
    def __init__(self, num_points):
        self.values = np.zeros((num_points, 2), dtype=np.float32)
        self.values[:, 0] = np.linspace(-1, 1, num_points)
        self.values[:, 1] = np.zeros(num_points)

    def update(self, y):
        self.values[1:, 1] = self.values[:-1, 1]
        self.values[0, 1] = y

    def get_render_data(self):
        return self.values
    

class LineData3D:
    def __init__(self, num_points):
        self.num_points = num_points
        self.values = np.zeros((num_points, 3), dtype=np.float32)
        self.rotation = R.from_quat([0, 0, 0, 1]) #np.eye(3)

    def update(self, xyz):
        # self.rotation, _ = R.align_vectors([[0, 0, 1]], [xyz])
        # xyz = self.rotate(xyz)

        p1 = np.array([0, 0, 0], dtype=np.float32)
        p2 = np.array([xyz[1], xyz[0], xyz[2]], dtype=np.float32)
        self.values = np.linspace(p1, p2, self.num_points, endpoint=True, dtype=np.float32)
        self.values[:,:2] *= -0.1
        self.values[:,:2] += 0.9

    def rotate(self, vector):
        return self.rotation.apply(vector)

    def get_render_data(self):
        return self.values
    

    