import numpy as np

class LineData:
    def __init__(self, num_points):
        self.x = np.linspace(-1, 1, num_points)
        self.y = np.zeros(num_points)

    def update(self, new_value):
        self.y[1:] = self.y[:-1]
        self.y[0] = new_value

    def get_render_data(self):
        return np.column_stack((self.x, self.y)).astype('f')