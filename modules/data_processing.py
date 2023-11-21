import numpy as np

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
        self.values = np.zeros((num_points, 3), dtype='f')

    def update(self, xyz):
        p1 = np.array([0, 0, 0])
        p2 = np.array(xyz)
        self.values = np.linspace(p1, p2, self.num_points, endpoint=True)

    def get_render_data(self):
        return self.values