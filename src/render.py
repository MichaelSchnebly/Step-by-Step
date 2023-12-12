from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram


class EventRenderer:
    '''A class to render Event Lines. Converts x-axis points into vertical lines.
    '''

    def __init__(self, lines):
        self.lines = lines

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        vertex_shader = load_shader("assets/shaders/2D/point-to-line/vertex.glsl", GL_VERTEX_SHADER)
        geometry_shader = load_shader("assets/shaders/2D/point-to-line/geometry.glsl", GL_GEOMETRY_SHADER)
        fragment_shader = load_shader("assets/shaders/2D/point-to-line/fragment.glsl", GL_FRAGMENT_SHADER)
        self.shader = compileProgram(vertex_shader, geometry_shader, fragment_shader)

        glUseProgram(self.shader)

        self.transform_loc = glGetUniformLocation(self.shader, "transform")
        # self.width_loc = glGetUniformLocation(self.shader, "lineWidth")
        self.color_loc = glGetUniformLocation(self.shader, "lineColor")

        glUseProgram(0)
        glBindVertexArray(0)

        self.running = True

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def render(self):
        if self.running:
            for line in self.lines:
                if line.running:
                    glUseProgram(self.shader)
                    glBindVertexArray(self.vao)

                    line.vbo.bind()
                    glEnableVertexAttribArray(0)
                    glVertexAttribPointer(0, 1, GL_FLOAT, GL_FALSE, 0, None)

                    glUniformMatrix4fv(self.transform_loc, 1, GL_FALSE, line.transform)
                    # glUniform1f(self.width_loc, line.width)
                    glUniform4fv(self.color_loc, 1, line.color)

                    glDrawArrays(GL_POINTS, 0, line.vertices.shape[0])

                    line.vbo.unbind()

class IMURenderer:
    def __init__(self, lines):
        self.lines = lines

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        vertex_shader = load_shader("assets/shaders/2D/polyline/vertex.glsl", GL_VERTEX_SHADER)
        geometry_shader = load_shader("assets/shaders/2D/polyline/geometry.glsl", GL_GEOMETRY_SHADER)
        fragment_shader = load_shader("assets/shaders/2D/polyline/fragment.glsl", GL_FRAGMENT_SHADER)
        self.shader = compileProgram(vertex_shader, geometry_shader, fragment_shader)

        glUseProgram(self.shader)

        self.transform_loc = glGetUniformLocation(self.shader, "transform")
        self.width_loc = glGetUniformLocation(self.shader, "lineWidth")
        self.color_loc = glGetUniformLocation(self.shader, "lineColor")

        glUseProgram(0)
        glBindVertexArray(0)

        self.running = True

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def render(self):
        if self.running:
            for line in self.lines:
                if line.running:
                    glUseProgram(self.shader)
                    glBindVertexArray(self.vao)

                    line.vbo.bind()
                    glEnableVertexAttribArray(0)
                    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

                    glUniformMatrix4fv(self.transform_loc, 1, GL_FALSE, line.transform)
                    glUniform1f(self.width_loc, line.width)
                    glUniform4fv(self.color_loc, 1, line.color)

                    glDrawArrays(GL_LINE_STRIP_ADJACENCY, 0, line.vertices.shape[0])

                    line.vbo.unbind()

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


class NNRenderer:
    def __init__(self, lines, delay):
        self.lines = lines
        self.delay = delay

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        vertex_shader = load_shader("assets/shaders/2D/polyline/vertex.glsl", GL_VERTEX_SHADER)
        geometry_shader = load_shader("assets/shaders/2D/polyline/geometry.glsl", GL_GEOMETRY_SHADER)
        fragment_shader = load_shader("assets/shaders/2D/polyline/fragment.glsl", GL_FRAGMENT_SHADER)
        self.shader = compileProgram(vertex_shader, geometry_shader, fragment_shader)

        glUseProgram(self.shader)

        self.transform_loc = glGetUniformLocation(self.shader, "transform")
        self.width_loc = glGetUniformLocation(self.shader, "lineWidth")
        self.color_loc = glGetUniformLocation(self.shader, "lineColor")

        glUseProgram(0)
        glBindVertexArray(0)

        self.running = True

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def render(self):
        if self.running:
            for line in self.lines:
                if line.running:
                    glUseProgram(self.shader)
                    glBindVertexArray(self.vao)

                    line.vbo.bind()
                    glEnableVertexAttribArray(0)
                    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

                    glUniformMatrix4fv(self.transform_loc, 1, GL_FALSE, line.transform)
                    glUniform1f(self.width_loc, line.width)
                    glUniform4fv(self.color_loc, 1, line.color)

                    glDrawArrays(GL_LINE_STRIP_ADJACENCY, self.delay, line.vertices.shape[0] - self.delay)

                    line.vbo.unbind()