#version 410 core
layout(lines_adjacency) in;
layout(triangle_strip, max_vertices = 10) out;

uniform float lineWidth;

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