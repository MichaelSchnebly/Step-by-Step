import glfw
from OpenGL.GL import *
import numpy as np

# Vertex Shader
vertex_shader = """
#version 120
attribute vec3 position;
varying float z;
void main() {
    float size;

    gl_Position = vec4(position, 1.0);

    z = position.z;
    z = z + 1;
    z = z / 2;

    size = z * 100;

    gl_PointSize = size;
}
"""

# Fragment Shader
fragment_shader = """
#version 120
varying float z;
void main() {
    float depth = z;  // Normalize z to [0, 1]
    gl_FragColor = vec4(1.0, 1.0, 1.0, depth);  // Alpha based on depth
}
"""
# Initialize glfw
if not glfw.init():
    raise Exception("GLFW can not be initialized!")

# Create a window
window = glfw.create_window(800, 600, "OpenGL Window", None, None)
if not window:
    glfw.terminate()
    raise Exception("GLFW window can not be created!")

glfw.make_context_current(window)

# Set up shaders
shader = glCreateProgram()
vertex = glCreateShader(GL_VERTEX_SHADER)
fragment = glCreateShader(GL_FRAGMENT_SHADER)
glShaderSource(vertex, vertex_shader)
glShaderSource(fragment, fragment_shader)
glCompileShader(vertex)
glCompileShader(fragment)
glAttachShader(shader, vertex)
glAttachShader(shader, fragment)
glLinkProgram(shader)

# Check for shader compile errors
if glGetShaderiv(vertex, GL_COMPILE_STATUS) != GL_TRUE:
    raise RuntimeError(glGetShaderInfoLog(vertex))
if glGetShaderiv(fragment, GL_COMPILE_STATUS) != GL_TRUE:
    raise RuntimeError(glGetShaderInfoLog(fragment))


# Example usage
p1 = np.array([0, 0, 0])  # First 3D point
p2 = np.array([0.5, -0.3, 0.9])  # Second 3D point
n = 100 # Number of points to generate
points = np.linspace(p1, p2, n, dtype=np.float32)

vbo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, points.nbytes, points, GL_STATIC_DRAW)

# Set up vertex attribute pointers
glUseProgram(shader)
position = glGetAttribLocation(shader, "position")
glEnableVertexAttribArray(position)
glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 0, None)


glEnable(GL_PROGRAM_POINT_SIZE)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


# Set up the camera
# glMatrixMode(GL_MODELVIEW)
# glLoadIdentity()
# glTranslatef(0.0, 0.0, 1.0)  # Move the scene to simulate the camera movement

# Main window loop
while not glfw.window_should_close(window):
    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glDrawArrays(GL_POINTS, 0, n)

    glfw.swap_buffers(window)

# Finalize and clean up
glfw.terminate()