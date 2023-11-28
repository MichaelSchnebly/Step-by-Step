import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.arrays import vbo
import glfw
import glm


class Polyline:
    def __init__(self, vertices, color, transformation):
        self.vertices = vertices
        self.color = color
        self.transformation = transformation
        self.vbo = vbo.VBO(self.vertices)

    
class 


class LineRenderer2D:
    def __init__(self, num_points):
        self.num_points = num_points
        
        # Generate VAO and VBO
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)

        # Bind the VAO
        glBindVertexArray(self.vao)

        # Bind the VBO and buffer the data
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        # glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        # Configure vertex attribute
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)

        # Compile shaders and create a program
        vertex_shader = load_shader("shaders/2D/vertex.glsl", GL_VERTEX_SHADER)
        geometry_shader = load_shader("shaders/2D/geometry.glsl", GL_GEOMETRY_SHADER)
        fragment_shader = load_shader("shaders/2D/fragment.glsl", GL_FRAGMENT_SHADER)
        self.shader = compileProgram(vertex_shader, geometry_shader, fragment_shader)

        # Unbind VAO and VBO
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

        # Get uniform locations
        line_width_location = glGetUniformLocation(self.shader, "lineWidth")

        # Set the line width
        line_width = 0.05  # Example line width
        glUseProgram(self.shader)
        glUniform1f(line_width_location, line_width)
        glUseProgram(0)

    def update_data(self, vertices):
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def render(self):
        glUseProgram(self.shader)
        glBindVertexArray(self.vao)
        glDrawArrays(GL_LINE_STRIP, 0, self.num_points)
        glBindVertexArray(0)
        glUseProgram(0)



class OpenGLApp:
    def __init__(self, window):
        self.window = window
        self.polylines = []

    def init_gl(self):
        """ Initialize OpenGL state """
        glClearColor(0.0, 0.0, 0.0, 1.0)  # Set clear color
        glEnable(GL_PROGRAM_POINT_SIZE)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def add_line_renderer(self, renderer):
        """ Add a line renderer to the app """
        self.polylines.append(renderer)

    def display(self):
        """ Display callback for GLFW """
        glClear(GL_COLOR_BUFFER_BIT)
        for i in range(0, 3):
            # glPushMatrix()
            # glTranslatef(-0.666, 1 - (i + 0.5) * 0.666, 0)
            # glScalef(0.333, 0.333, 1.0)
            self.polylines[i].render()
            # glPopMatrix()

        for i in range(3, 6):
            # glPushMatrix()
            # glTranslatef(0.666, 1 - (i - 3 + 0.5) * 0.666, 0)
            # glScalef(0.333, 0.333, 1.0)
            self.line_renderers[i].render()
            # glPopMatrix()

        # self.line_renderers[6].render()

        # self.line_renderers[0].render()
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


def print_vbo_data(vbo, num_points, num_components):
    """
    Print the data from a VBO.

    :param vbo: VBO object to read from.
    :param num_points: Number of points in the VBO.
    :param num_components: Number of components per point (e.g., 2 for 2D, 3 for 3D).
    """
    vbo.bind()
    
    # Calculate the size of the data in bytes
    data_size = num_points * num_components * np.dtype('float32').itemsize

    # Retrieve the data from the VBO
    data = glGetBufferSubData(GL_ARRAY_BUFFER, 0, data_size)

    # Convert to a NumPy array for easy viewing
    data_array = np.frombuffer(data, dtype='f')
    data_array = data_array.reshape(num_points, num_components)

    vbo.unbind()

    print(np.around(data_array[0], 2))