#version 120
varying float z;
void main() {
    gl_FragColor = vec4(z, z, z, 1);  // Alpha based on depth
}
