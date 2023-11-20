import numpy as np
from OpenGL.GL import *
from OpenGL.arrays import vbo
import glfw

class LineRenderer:
    def __init__(self, num_points):
        self.num_points = num_points
        self.vbo = vbo.VBO(np.zeros((num_points, 2), dtype='f'))
        glLineWidth(5.0)  # Set line width here or in a render method

    def update_data(self, data):
        self.vbo.set_array(data)

    def render(self):
        self.vbo.bind()
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(2, GL_FLOAT, 0, self.vbo)
        glDrawArrays(GL_LINE_STRIP, 0, self.num_points)
        glDisableClientState(GL_VERTEX_ARRAY)
        self.vbo.unbind()

class OpenGLApp:
    def __init__(self, window):
        self.window = window
        self.line_renderers = []

    def init_gl(self):
        """ Initialize OpenGL state """
        glClearColor(0.0, 0.0, 0.0, 1.0)  # Set clear color

    def add_line_renderer(self, renderer):
        """ Add a line renderer to the app """
        self.line_renderers.append(renderer)

    def display(self):
        """ Display callback for GLFW """
        glClear(GL_COLOR_BUFFER_BIT)
        for renderer in self.line_renderers:
            renderer.render()  # Render each line
        glfw.swap_buffers(self.window)

    def update_line_data(self, line_index, data):
        """ Update the data of a specific line renderer """
        if line_index < len(self.line_renderers):
            self.line_renderers[line_index].update_data(data)