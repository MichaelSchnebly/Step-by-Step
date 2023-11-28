#version 410

in vec3 position;
out vec4 color;

void main() {
    float z;
    float size;

    gl_Position = vec4(position.x, position.y, position.z, 1.0);

    z = position.z;
    z = z + 1;
    z = z / 2;

    size = z * z * 20;

    gl_PointSize = size;
    color = vec4(z,z,z,1);
}