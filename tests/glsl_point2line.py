import glfw
from OpenGL.GL import *
import numpy as np

# Vertex Shader - Modified to accept a single float for x position
vertex_shader = """
#version 410 core
layout(location = 0) in float xPos; // x position as a float
void main()
{
    gl_Position = vec4(xPos, 0.0, 0.0, 1.0); // Use the xPos directly
}
"""

# Fragment Shader - Remains the same
fragment_shader = """
#version 410 core
out vec4 FragColor;
void main()
{
    FragColor = vec4(1.0, 1.0, 1.0, 1.0);
}
"""

# Geometry Shader - Remains the same
geometry_shader = """
#version 410 core
layout(points) in;
layout(line_strip, max_vertices = 2) out;
void main()
{
    gl_Position = vec4(gl_in[0].gl_Position.x, -1.0, 0.0, 1.0);
    EmitVertex();
    gl_Position = vec4(gl_in[0].gl_Position.x, 1.0, 0.0, 1.0);
    EmitVertex();
    EndPrimitive();
}
"""

def main():
    # Initialize GLFW
    if not glfw.init():
        return

    # Create a windowed mode window and its OpenGL context
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    window = glfw.create_window(640, 480, "OpenGL Vertical Line", None, None)
    if not window:
        glfw.terminate()
        return

    # Make the window's context current
    glfw.make_context_current(window)

    # Compile shaders and create a shader program
    shader_program = glCreateProgram()

    for shader_source, shader_type in [(vertex_shader, GL_VERTEX_SHADER), (fragment_shader, GL_FRAGMENT_SHADER), (geometry_shader, GL_GEOMETRY_SHADER)]:
        shader = glCreateShader(shader_type)
        glShaderSource(shader, shader_source)
        glCompileShader(shader)
        if not glGetShaderiv(shader, GL_COMPILE_STATUS):
            error = glGetShaderInfoLog(shader).decode()
            print(f'Shader compile error: {error}')
            return
        glAttachShader(shader_program, shader)

    glLinkProgram(shader_program)

    # Check for linking errors
    if not glGetProgramiv(shader_program, GL_LINK_STATUS):
        print(f'Error linking program: {glGetProgramInfoLog(shader_program)}')
        return

    glUseProgram(shader_program)

    # Set up vertex data - now a single float for x position
    x_position = np.array([0.5], dtype=np.float32)  # Change this value to move the line on the x-axis
    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)

    glBindVertexArray(VAO)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, x_position.nbytes, x_position, GL_STATIC_DRAW)

    # Note: glVertexAttribPointer now has a size of 1, since we're passing a single float
    glVertexAttribPointer(0, 1, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(0)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Render here
        glClear(GL_COLOR_BUFFER_BIT)

        glBindVertexArray(VAO)
        glDrawArrays(GL_POINTS, 0, 1)

        # Swap front and back buffers
        glfw.swap_buffers(window)

        # Poll for and process events
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()