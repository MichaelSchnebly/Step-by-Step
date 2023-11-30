#version 410 core
layout(points) in;
layout(line_strip, max_vertices = 2) out;
uniform mat4 transform;

void main()
{
    gl_Position = transform * vec4(gl_in[0].gl_Position.x, 0.0, 0.0, 1.0);
    EmitVertex();
    gl_Position = transform * vec4(gl_in[0].gl_Position.x, 1.0, 0.0, 1.0);
    EmitVertex();
    EndPrimitive();
}