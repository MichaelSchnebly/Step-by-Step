#version 120

attribute vec3 position;
varying float z;

void main() {
    float size;

    gl_Position = vec4(position.x, position.y, position.z, 1.0);

    z = position.z;
    z = z + 1;
    z = z / 2;

    size = z * z * 20;

    gl_PointSize = size;
}