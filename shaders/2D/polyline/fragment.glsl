#version 410 core

uniform vec4 lineColor;
in vec3 coord;
out vec4 fragColor;

void main() {
    float distX = abs(0.5-coord.x);
    float distY = abs(0.5-coord.y) - 0.5;
    
    if (distY > 0) {
        distY = distY / coord.z / 2;
        float dist = sqrt(distX * distX + distY * distY);
        if (dist > 0.5) {
            discard;
        }
    }

    fragColor = lineColor;
}