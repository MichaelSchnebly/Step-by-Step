import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np

# Vertex Shader
vertex_src = """
#version 120
attribute vec3 a_position;
varying float z;
void main() {
    z = a_position.z;
    gl_Position = vec4(a_position, 1.0);
}
"""

# Fragment Shader
fragment_src = """
#version 120
varying float z;
void main() {
    float intensity = 1.0 - z; // Dimmer as Z increases
    gl_FragColor = vec4(intensity, intensity, intensity, 1.0);
}
"""

# Initialize GLFW
if not glfw.init():
    raise Exception("GLFW can not be initialized!")

# Set window's OpenGL version to 2.1
glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)

# Creating the window
window = glfw.create_window(800, 600, "PyOpenGL Triangle", None, None)

# Check if window was created
if not window:
    glfw.terminate()
    raise Exception("GLFW window can not be created!")

# Set window's position and make the context current
glfw.set_window_pos(window, 400, 200)
glfw.make_context_current(window)

# Triangle vertices
vertices = [-0.5, -0.5, 1.0, 0.5, -0.5, 0.0, 0.0,  0.5, 0.0]
vertices = np.array(vertices, dtype=np.float32)

# Vertex Buffer Object
VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

# Compile the shaders
shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                        compileShader(fragment_src, GL_FRAGMENT_SHADER))

# Get the position of the 'a_position' attribute
pos = glGetAttribLocation(shader, 'a_position')

# The main application loop
while not glfw.window_should_close(window):
    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT)

    glUseProgram(shader)

    # Bind the VBO and set the vertex attribute
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glVertexAttribPointer(pos, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(pos)

    glDrawArrays(GL_TRIANGLES, 0, 3)
    glDisableVertexAttribArray(pos)

    glfw.swap_buffers(window)

# Terminate GLFW
glfw.terminate()