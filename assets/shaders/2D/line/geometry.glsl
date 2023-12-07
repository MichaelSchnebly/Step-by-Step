#version 410 core
layout(lines) in;
layout(triangle_strip, max_vertices = 4) out;

uniform float lineWidth; // Width of the line

void main() {
    vec3 perp = normalize(cross(vec3(gl_in[1].gl_Position) - vec3(gl_in[0].gl_Position), vec3(0.0, 0.0, 1.0))) * lineWidth / 2.0;
    vec4 perpVec4 = vec4(perp, 0.0);

    gl_Position = gl_in[0].gl_Position + perpVec4;
    EmitVertex();

    gl_Position = gl_in[0].gl_Position - perpVec4;
    EmitVertex();

    gl_Position = gl_in[1].gl_Position + perpVec4;
    EmitVertex();

    gl_Position = gl_in[1].gl_Position - perpVec4;
    EmitVertex();

    EndPrimitive();
}