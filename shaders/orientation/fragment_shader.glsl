#version 410 core

in vec4 color;      // Input color
out vec4 fragColor; // Output color

void main() {
    fragColor = color; // Assign the input color to the output
}