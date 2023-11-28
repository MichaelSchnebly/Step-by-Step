import glfw
import OpenGL.GL as gl
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import glm

# Vertex Shader Source Code
vertex_shader_source = """
#version 410 core
layout(location = 0) in vec2 vertexPosition;

void main() {
    gl_Position = vec4(vertexPosition, 0.0, 1.0);
}
"""

# Geometry Shader Source Code
geometry_shader_source = """
#version 410 core
layout(lines) in;
layout(triangle_strip, max_vertices = 4) out;

uniform float lineWidth; // Width of the line

void main() {
    vec2 perp = normalize(vec2(-gl_in[1].gl_Position.y + gl_in[0].gl_Position.y, 
                               gl_in[1].gl_Position.x - gl_in[0].gl_Position.x)) * lineWidth / 2.0;


    gl_Position = gl_in[0].gl_Position + vec4(perp, 0.0, 0.0);
    EmitVertex();

    gl_Position = gl_in[0].gl_Position - vec4(perp, 0.0, 0.0);
    EmitVertex();

    gl_Position = gl_in[1].gl_Position + vec4(perp, 0.0, 0.0);
    EmitVertex();

    gl_Position = gl_in[1].gl_Position - vec4(perp, 0.0, 0.0);
    EmitVertex();

    EndPrimitive();
}
"""

# Fragment Shader Source Code
fragment_shader_source = """
#version 410 core
out vec4 fragColor;

void main() {
    fragColor = vec4(1.0, 1.0, 1.0, 1.0); // Set line color here
}
"""

def initialize_glfw():
    if not glfw.init():
        raise Exception("GLFW can't be initialized")

    # Set window hints for GLFW
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

    # Create a window
    window = glfw.create_window(800, 600, "OpenGL Window", None, None)
    if not window:
        glfw.terminate()
        raise Exception("GLFW window can't be created")

    glfw.make_context_current(window)

    return window

# Initialize GLFW and create a window
window = initialize_glfw()

# Vertex data for lines
vertices = np.array([
    # Line 1 coordinates
    -0.5, -0.5, 
     0.5, -0.5,

    # Line 2 coordinates
    -0.5,  0.5, 
     0.5,  0.5,
], dtype=np.float32)

# Generate VAO and VBO
vao = gl.glGenVertexArrays(1)
vbo = gl.glGenBuffers(1)

# Bind the VAO
gl.glBindVertexArray(vao)

# Bind the VBO and buffer the data
gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
gl.glBufferData(gl.GL_ARRAY_BUFFER, vertices.nbytes, vertices, gl.GL_STATIC_DRAW)

# Configure vertex attribute
gl.glVertexAttribPointer(0, 2, gl.GL_FLOAT, gl.GL_FALSE, 0, None)
gl.glEnableVertexAttribArray(0)

# Compile shaders and create a program
vertex_shader = compileShader(vertex_shader_source, gl.GL_VERTEX_SHADER)
geometry_shader = compileShader(geometry_shader_source, gl.GL_GEOMETRY_SHADER)
fragment_shader = compileShader(fragment_shader_source, gl.GL_FRAGMENT_SHADER)
shader_program = compileProgram(vertex_shader, geometry_shader, fragment_shader)

# Unbind VAO and VBO
gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
gl.glBindVertexArray(0)

# Get uniform locations
line_width_location = gl.glGetUniformLocation(shader_program, "lineWidth")
projection_matrix_location = gl.glGetUniformLocation(shader_program, "projectionMatrix")

# Set the line width
line_width = 0.05  # Example line width
gl.glUseProgram(shader_program)
gl.glUniform1f(line_width_location, line_width)

# Create a projection matrix
# For simplicity, let's create an orthographic projection matrix
projection_matrix = glm.ortho(-1, 1, -1, 1, -1, 1)
projection_matrix_np = np.array(projection_matrix).astype(np.float32)

# Set the projection matrix
gl.glUniformMatrix4fv(projection_matrix_location, 1, gl.GL_FALSE, projection_matrix_np)


# Main loop
while not glfw.window_should_close(window):
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

    gl.glUseProgram(shader_program)

    # Bind VAO and draw
    gl.glBindVertexArray(vao)
    gl.glDrawArrays(gl.GL_LINES, 0, len(vertices) // 2)

    glfw.swap_buffers(window)
    glfw.poll_events()

# Clean up
gl.glDeleteVertexArrays(1, [vao])
gl.glDeleteBuffers(1, [vbo])
gl.glDeleteProgram(shader_program)
glfw.terminate()