import numpy as np

class LineData:
    def __init__(self, num_points, dynamic_x=False):
        self.dynamic_x = dynamic_x
        if self.dynamic_x:
            self.x = np.zeros(num_points)
            self.y = np.zeros(num_points)
        else:
            self.x = np.linspace(-1, 1, num_points)
            self.y = np.zeros(num_points)

    def update_y(self, new_y):
        """ Update y-values for the line, shifting old data """
        self.y[1:] = self.y[:-1]
        self.y[0] = new_y

    def update_xy(self, new_x, new_y):
        """ Update both x and y values for the line """
        if not self.dynamic_x:
            raise ValueError("This LineData instance does not support dynamic x values.")
        self.x[0] = new_x
        self.y[0] = new_y

    def get_render_data(self):
        return np.column_stack((self.x, self.y)).astype('f')