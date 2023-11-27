import numpy as np
from scipy.spatial.transform import Rotation as R

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

    def rotate(self, vector):
        return self.rotation.apply(vector)

    def get_render_data(self):
        return self.values
    

    