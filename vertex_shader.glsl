#version 120
attribute vec3 aPos; // Use 'attribute' instead of 'layout'

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main() {
    gl_Position = projection * view * model * vec4(aPos, 1.0);
}