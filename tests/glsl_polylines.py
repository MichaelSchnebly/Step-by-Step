import glfw

import numpy as np
import OpenGL.GL as GL
from OpenGL.GL import shaders
from OpenGL.arrays import vbo

class Polyline:
    def __init__(self, vertices, color, transformation):
        self.vertices = vertices
        self.color = color
        self.transformation = transformation
        self.vbo = vbo.VBO(self.vertices)

def main():
    # Initialize GLFW
    if not glfw.init():
        return

    # Window setup
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    window = glfw.create_window(640, 480, "OpenGL Window", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    # Compile shaders
    vertex_shader = shaders.compileShader("""
    #version 410 core
    layout(location = 0) in vec3 position;
    uniform mat4 transform;
    void main() {
        gl_Position = transform * vec4(position, 1.0);
    }
    """, GL.GL_VERTEX_SHADER)

    # geometry_shader = shaders.compileShader("""
    # #version 410 core
    # layout(lines) in;
    # layout(triangle_strip, max_vertices = 4) out;

    # // uniform mat4 projectionMatrix;
    # // uniform float lineWidth;

    # void main() {
    #     float lineWidth = 0.5;                                   

    #     vec4 p0 = gl_in[0].gl_Position;
    #     vec4 p1 = gl_in[1].gl_Position;

    #     vec2 direction = normalize(p1.xy - p0.xy);
    #     vec2 normal = vec2(-direction.y, direction.x);
    #     vec2 offset = (lineWidth / 2.0) * normal;

    #     gl_Position = p0 + vec4(offset, 0.0, 0.0);
    #     EmitVertex();
    #     gl_Position = p0 - vec4(offset, 0.0, 0.0);
    #     EmitVertex();
    #     gl_Position = p1 + vec4(offset, 0.0, 0.0);
    #     EmitVertex();
    #     gl_Position = p1 - vec4(offset, 0.0, 0.0);
    #     EmitVertex();

    #     EndPrimitive();
    # }
    # """, GL.GL_GEOMETRY_SHADER)

    # geometry_shader = shaders.compileShader("""
    # #version 410 core
    # layout(lines_adjacency) in;
    # layout(triangle_strip, max_vertices = 10) out;

    # //uniform float lineWidth;

    # void main() {
    #     float lineWidth = 0.05;
    #     vec4 prev = gl_in[0].gl_Position; // Previous vertex
    #     vec4 start = gl_in[1].gl_Position; // Start vertex of current segment
    #     vec4 end = gl_in[2].gl_Position; // End vertex of current segment
    #     vec4 next = gl_in[3].gl_Position; // Next vertex after current segment

    #     vec2 prevDir = normalize(start.xy - prev.xy);
    #     vec2 curDir = normalize(end.xy - start.xy);
    #     vec2 nextDir = normalize(next.xy - end.xy);

    #     vec2 normalStart = vec2(-curDir.y, curDir.x);
    #     vec2 normalEnd = vec2(-nextDir.y, nextDir.x);

    #     vec2 offsetStart = (lineWidth / 2.0) * normalStart;
    #     vec2 offsetEnd = (lineWidth / 2.0) * normalEnd;

    #     // Bevel join at the start
    #     vec2 bevelStartDir = normalize(normalStart + prevDir);
    #     vec2 bevelStartOffset = (lineWidth / 2.0) * bevelStartDir;

    #     // Bevel join at the end
    #     vec2 bevelEndDir = normalize(normalEnd + curDir);
    #     vec2 bevelEndOffset = (lineWidth / 2.0) * bevelEndDir;

    #     // Emit vertices for the bevel join at the start
    #     gl_Position = vec4(start.xy + bevelStartOffset, 0.0, 1.0);
    #     EmitVertex();
    #     gl_Position = vec4(start.xy - bevelStartOffset, 0.0, 1.0);
    #     EmitVertex();

    #     // Emit vertices for the current line segment
    #     gl_Position = vec4(start.xy + offsetStart, 0.0, 1.0);
    #     EmitVertex();
    #     gl_Position = vec4(start.xy - offsetStart, 0.0, 1.0);
    #     EmitVertex();
    #     gl_Position = vec4(end.xy + offsetEnd, 0.0, 1.0);
    #     EmitVertex();
    #     gl_Position = vec4(end.xy - offsetEnd, 0.0, 1.0);
    #     EmitVertex();

    #     // Emit vertices for the bevel join at the end
    #     gl_Position = vec4(end.xy + bevelEndOffset, 0.0, 1.0);
    #     EmitVertex();
    #     gl_Position = vec4(end.xy - bevelEndOffset, 0.0, 1.0);
    #     EmitVertex();

    #     EndPrimitive();
    # }
    # """, GL.GL_GEOMETRY_SHADER)

    geometry_shader = shaders.compileShader("""
    #version 410 core
    layout(lines_adjacency) in;
    layout(triangle_strip, max_vertices = 10) out;

    // uniform float lineWidth;
    float lineWidth = 0.005;

    vec2 miterJoin(vec2 p0, vec2 p1, vec2 p2, float lineWidth, out float miterLength) {
        
                                            
        // Direction of the two segments
        vec2 dir1 = normalize(p1 - p0);
        vec2 dir2 = normalize(p2 - p1);

        // Normal of the two segments
        vec2 normal1 = vec2(-dir1.y, dir1.x);
        vec2 normal2 = vec2(-dir2.y, dir2.x);

        // Miter vector
        vec2 miter = normalize(normal1 + normal2);

        // Calculate miter length
        miterLength = lineWidth / dot(miter, normal1);

        return miter * miterLength;
    }

    void main() {
        vec2 prevVertex = gl_in[0].gl_Position.xy; // Previous vertex
        vec2 currentStart = gl_in[1].gl_Position.xy; // Start vertex of current segment
        vec2 currentEnd = gl_in[2].gl_Position.xy; // End vertex of current segment
        vec2 nextVertex = gl_in[3].gl_Position.xy; // Next vertex

        float miterLength1, miterLength2;
        vec2 miter1 = miterJoin(prevVertex, currentStart, currentEnd, lineWidth, miterLength1);
        vec2 miter2 = miterJoin(currentStart, currentEnd, nextVertex, lineWidth, miterLength2);

        // Emit vertices for the miter join at the start
        gl_Position = vec4(currentStart + miter1, 0.0, 1.0);
        EmitVertex();
        gl_Position = vec4(currentStart - miter1, 0.0, 1.0);
        EmitVertex();

        // Emit vertices for the current line segment
        gl_Position = vec4(currentEnd + miter2, 0.0, 1.0);
        EmitVertex();
        gl_Position = vec4(currentEnd - miter2, 0.0, 1.0);
        EmitVertex();

        EndPrimitive();
    }
    """, GL.GL_GEOMETRY_SHADER)

    fragment_shader = shaders.compileShader("""
    #version 410 core
    uniform vec4 lineColor;
    out vec4 fragColor;
    void main() {
        fragColor = lineColor;
    }
    """, GL.GL_FRAGMENT_SHADER)

    vao = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(1)

    # Bind the VBO and buffer the data
    # GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
    # glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    # Configure vertex attribute
    # GL.glVertexAttribPointer(0, 2, GL.GL_FLOAT, GL.GL_FALSE, 0, None)
    # GL.glEnableVertexAttribArray(0)
    shader = shaders.compileProgram(vertex_shader, geometry_shader, fragment_shader)

    # Create multiple polylines
    vertices = np.zeros((100, 3), dtype=np.float32)
    vertices[:, 0] = np.linspace(-1, 1, 100, True)
    vertices[:, 1] = np.random.uniform(-0.5, 0.5, 100)
    vertices[:, 2] = 0.0

    polylines = [
        Polyline(vertices, 
                 np.array([1.0, 0.0, 0.0, 1.0], dtype=np.float32), 
                 np.eye(4, dtype=np.float32)),
        # Add more Polylines with different properties
    ]

    while not glfw.window_should_close(window):
        # Render logic
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glUseProgram(shader)

        transform_loc = GL.glGetUniformLocation(shader, "transform")
        color_loc = GL.glGetUniformLocation(shader, "lineColor")

        for polyline in polylines:
            # Update polyline data
            # ... [Add logic to update polyline.vertices]

            polyline.vbo.set_array(polyline.vertices)

            # Bind VBO
            polyline.vbo.bind()

            # # Enable vertex array
            GL.glEnableVertexAttribArray(0)
            GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 0, None)

            # Set color and transformation
            GL.glUniformMatrix4fv(transform_loc, 1, GL.GL_FALSE, polyline.transformation)
            GL.glUniform4fv(color_loc, 1, polyline.color)

            # Draw polyline
            GL.glDrawArrays(GL.GL_LINE_STRIP_ADJACENCY, 0, len(polyline.vertices))

            # Unbind VBO
            polyline.vbo.unbind()

        # Swap buffers
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()