import numpy as np
from OpenGL.GL import *
from OpenGL.arrays import vbo
import glfw


class LineRenderer2D:
    def __init__(self, num_points):
        self.num_points = num_points
        self.vbo = vbo.VBO(np.zeros((num_points, 2), dtype='f'))
        glLineWidth(5.0)

    def update_data(self, data):
        self.vbo.set_array(data)

    def render(self):
        self.vbo.bind()
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(2, GL_FLOAT, 0, self.vbo)
        glDrawArrays(GL_LINE_STRIP, 0, self.num_points)
        glDisableClientState(GL_VERTEX_ARRAY)
        self.vbo.unbind()


class LineRenderer3D:
    def __init__(self, num_points, vertex_shader_path="shaders/vertex_shader.glsl", fragment_shader_path="shaders/fragment_shader.glsl"):
        self.num_points = num_points
        self.shader = create_shader_program(vertex_shader_path, fragment_shader_path)
        self.vbo = vbo.VBO(np.zeros((num_points, 3), dtype='f'))

    def update_data(self, data):
        self.vbo.set_array(data)

    def render(self):
        glUseProgram(self.shader)
        self.vbo.bind()
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, self.vbo)
        glDrawArrays(GL_POINTS, 0, self.num_points)
        glDisableVertexAttribArray(0)
        self.vbo.unbind()
        glUseProgram(0)


class OpenGLApp:
    def __init__(self, window):
        self.window = window
        self.line_renderers = []

    def init_gl(self):
        """ Initialize OpenGL state """
        glClearColor(0.0, 0.0, 0.0, 1.0)  # Set clear color
        glEnable(GL_PROGRAM_POINT_SIZE)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def add_line_renderer(self, renderer):
        """ Add a line renderer to the app """
        self.line_renderers.append(renderer)

    def display(self):
        """ Display callback for GLFW """
        glClear(GL_COLOR_BUFFER_BIT)
        for i in range(0, 3):
            glPushMatrix()
            glTranslatef(-0.666, 1 - (i + 0.5) * 0.666, 0)
            glScalef(0.333, 0.333, 1.0)
            self.line_renderers[i].render()
            glPopMatrix()

        for i in range(3, 6):
            glPushMatrix()
            glTranslatef(0.666, 1 - (i - 3 + 0.5) * 0.666, 0)
            glScalef(0.333, 0.333, 1.0)
            self.line_renderers[i].render()
            glPopMatrix()

        self.line_renderers[6].render()
        glfw.swap_buffers(self.window)

    def update_line_data(self, line_index, data):
        """ Update the data of a specific line renderer """
        if line_index < len(self.line_renderers):
            self.line_renderers[line_index].update_data(data)


def load_shader(shader_file, shader_type):
    with open(shader_file, 'r') as file:
        shader_src = file.read()
    shader_ref = glCreateShader(shader_type)
    glShaderSource(shader_ref, shader_src)
    glCompileShader(shader_ref)

    # Check for shader compilation errors
    compile_success = glGetShaderiv(shader_ref, GL_COMPILE_STATUS)
    if not compile_success:
        info_log = glGetShaderInfoLog(shader_ref)
        print(f"Shader compilation error: {info_log}")
        return None

    return shader_ref


def create_shader_program(vertex_file_path, fragment_file_path):
    vertex_shader = load_shader(vertex_file_path, GL_VERTEX_SHADER)
    fragment_shader = load_shader(fragment_file_path, GL_FRAGMENT_SHADER)
    shader = glCreateProgram()
    glAttachShader(shader, vertex_shader)
    glAttachShader(shader, fragment_shader)
    glLinkProgram(shader)
    return shader