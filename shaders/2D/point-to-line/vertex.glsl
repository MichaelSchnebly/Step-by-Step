#version 410 core
layout(location = 0) in float xPos; // x position as a float
void main()
{
    gl_Position = vec4(xPos, 0.0, 0.0, 1.0); // Use the xPos directly
}