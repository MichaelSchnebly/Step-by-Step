import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import glm

# Vertex Shader
vertex_src = """
#version 120
uniform mat4 view;
uniform mat4 projection;
attribute vec3 a_position;
varying float z;
void main() {
    z = a_position.z;
    gl_Position = projection * view * vec4(a_position, 1.0);
}
"""

# Fragment Shader
fragment_src = """
#version 120
varying float z;
void main() {
    float intensity = 1.0 + z; // Dimmer as Z decreases
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

# Perspective projection matrix
aspect_ratio = 800 / 600  # Assuming your window size is 800x600
projection = glm.perspective(glm.radians(45), aspect_ratio, 0.1, 10.0)

# Camera matrix
camera_pos = glm.vec3(0, 0, 3)  # Camera is 3 units back on the Z-axis
camera_target = glm.vec3(0, 0, 0)  # Camera is looking at the origin
camera_up = glm.vec3(0, 1, 0)  # 'Up' is in the positive Y direction
view = glm.lookAt(camera_pos, camera_target, camera_up)

# Triangle vertices
# Quad vertices (two triangles)
vertices = [
    -0.5, -0.5, -1.0,  # Bottom left of the first triangle
     0.5, -0.5, 0.0,  # Bottom right of the first triangle / Bottom left of the second
     0.5,  0.5, 0.0,  # Top right of the first triangle / Top right of the second
    -0.5, -0.5, -1.0,  # Bottom left of the first triangle / Top left of the second
     0.5,  0.5, 0.0,  # Top right of the first triangle / Top right of the second
    -0.5,  0.5, 0.0   # Top left of the second triangle
]
vertices = np.array(vertices, dtype=np.float32)

# Vertex Buffer Object
VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

# Compile the shaders
shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                        compileShader(fragment_src, GL_FRAGMENT_SHADER))

# Set the shader program
glUseProgram(shader)

# Get the position of the 'a_position' attribute
pos = glGetAttribLocation(shader, 'a_position')

# Get the location of the 'projection' uniform and set it
projection_loc = glGetUniformLocation(shader, "projection")
glUniformMatrix4fv(projection_loc, 1, GL_FALSE, glm.value_ptr(projection))

# Set the view matrix
view_loc = glGetUniformLocation(shader, "view")
glUniformMatrix4fv(view_loc, 1, GL_FALSE, glm.value_ptr(view))


# The main application loop
while not glfw.window_should_close(window):
    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT)

    glUseProgram(shader)

    # Bind the VBO and set the vertex attribute
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glVertexAttribPointer(pos, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(pos)

    glDrawArrays(GL_TRIANGLES, 0, 6)
    glDisableVertexAttribArray(pos)

    glfw.swap_buffers(window)

# Terminate GLFW
glfw.terminate()