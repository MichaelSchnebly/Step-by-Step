#version 410 core

layout(lines_adjacency) in;
layout(triangle_strip, max_vertices = 4) out;

uniform float lineWidth;

out vec3 coord;

void main() {
    vec4 start = gl_in[1].gl_Position;
    vec4 end = gl_in[2].gl_Position;
    float halfWidth = lineWidth / 2.0;

    vec4 direction = normalize(end - start);
    vec4 normal = vec4(-direction.y, direction.x, 0.0, 0.0);
    vec4 offset = halfWidth * normalize(normal);
    vec4 extension = halfWidth * direction;

    // Extend the endpoints along the line direction
    vec4 extendedStart = start - extension;
    vec4 extendedEnd = end + extension;

    float lineLength = length(end - start);
    float x = halfWidth/lineLength;

    coord = vec3(0, 0-x, x);
    gl_Position = extendedStart + offset;
    EmitVertex();
    
    coord = vec3(0, 1+x, x);
    gl_Position = extendedStart - offset;
    EmitVertex();
    
    coord = vec3(1, 0-x, x);
    gl_Position = extendedEnd + offset;
    EmitVertex();
    
    coord = vec3(1, 1+x, x);
    gl_Position = extendedEnd - offset;
    EmitVertex();

    EndPrimitive();
}