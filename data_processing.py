import numpy as np

class LineData2D:
    def __init__(self, num_points):
        self.x = np.linspace(-1, 1, num_points)
        self.y = np.zeros(num_points)

    def update(self, new_value):
        self.y[1:] = self.y[:-1]
        self.y[0] = new_value

    def get_render_data(self):
        return np.column_stack((self.x, self.y)).astype('f')
    

class LineData3D:
    def __init__(self, num_points):
        self.x = np.zeros(num_points)
        self.y = np.zeros(num_points)
        self.z = np.zeros(num_points)

    def update(self, new_x, new_y, new_z):
        self.x[0] = new_x
        self.y[0] = new_y
        self.z[0] = new_z

     


    def create_quad_vertices(self, start_point, end_point, quad_width):
        # Calculate direction vector of the line segment
        direction = end_point - start_point
        direction = direction / np.linalg.norm(direction)  # Normalize

        # Calculate a perpendicular vector (simplified, assumes a certain view direction)
        perpendicular = np.array([-direction[1], direction[0], direction[2]])
        half_width_vector = perpendicular * quad_width / 2

        # Calculate four corners of the quad
        v0 = start_point - half_width_vector
        v1 = start_point + half_width_vector
        v2 = end_point - half_width_vector
        v3 = end_point + half_width_vector

        # Two triangles to form the quad
        return np.array([v0, v1, v2, v2, v1, v3])
    
    def get_render_data(self):
        # return np.column_stack((self.x, self.y, self.z)).astype('f')
        start = np.array([0, 0, 0])
        end = np.array([self.x[0], self.y[0], self.z[0]])

        return self.create_quad_vertices(start,end, 0.1)
   

    # # Example usage
    # start = np.array([0.0, 0.0, 0.0])
    # end = np.array([1.0, 1.0, 0.0])
    # quad_width = 0.1

    # quad_vertices = create_quad_vertices(start, end, quad_width)