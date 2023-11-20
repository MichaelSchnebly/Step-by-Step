# import numpy as np
# from OpenGL.GL import *
# from OpenGL.GLUT import *

# # Global state
# angle = 0.0

# def init_gl():
#     """ Initialize OpenGL state """
#     glClearColor(0.0, 0.0, 0.0, 1.0)  # Set clear color
#     glEnable(GL_DEPTH_TEST)            # Enable depth testing for 3D

# def draw_triangle():
#     """ Draw a simple triangle """
#     glBegin(GL_TRIANGLES)
#     glColor3f(1, 0, 0); glVertex3f(-0.5, -0.5, 0)
#     glColor3f(0, 1, 0); glVertex3f( 0.5, -0.5, 0)
#     glColor3f(0, 0, 1); glVertex3f( 0.0,  0.5, 0)
#     glEnd()

# def display():
#     """ Display callback for GLUT """
#     global angle

#     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#     glLoadIdentity()
#     glRotatef(angle, 0, 1, 0)  # Rotate around y-axis

#     draw_triangle()

#     glutSwapBuffers()

#     angle += 0.5  # Update angle for the next frame

# def timer(value):
#     """ Timer callback for GLUT """
#     glutPostRedisplay()   # Post a redraw event
#     glutTimerFunc(16, timer, 0)  # Aim for ~60 FPS

# def main():
#     glutInit()
#     glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
#     glutInitWindowSize(800, 600)
#     glutCreateWindow(b"High-Performance PyOpenGL Animation")

#     init_gl()

#     glutDisplayFunc(display)
#     glutTimerFunc(16, timer, 0)  # Start the timer for the first time

#     glutMainLoop()

# if __name__ == "__main__":
#     main()

import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo

# Number of points in the sine wave
NUM_POINTS = 100

# Initialize VBO with dummy data
sine_wave_vbo = vbo.VBO(np.zeros((NUM_POINTS, 2), dtype='f'))

def init_gl():
    """ Initialize OpenGL state """
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Set clear color

def update_sine_wave(phase):
    """ Update the sine wave points for the VBO """
    x = np.linspace(-1, 1, NUM_POINTS)
    y = np.sin(2 * np.pi * x + phase)
    data = np.column_stack((x, y))
    sine_wave_vbo.set_array(data.astype('f'))

def display():
    """ Display callback for GLUT """
    glClear(GL_COLOR_BUFFER_BIT)

    sine_wave_vbo.bind()
    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointer(2, GL_FLOAT, 0, sine_wave_vbo)
    glDrawArrays(GL_LINE_STRIP, 0, NUM_POINTS)
    glDisableClientState(GL_VERTEX_ARRAY)
    sine_wave_vbo.unbind()

    glutSwapBuffers()

def timer(value):
    """ Timer callback for GLUT """
    update_sine_wave(value / 20.0)  # Update phase based on time
    glutPostRedisplay()
    glutTimerFunc(16, timer, value + 1)  # Aim for ~60 FPS

def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Oscillating Sine Wave with VBO")

    init_gl()

    glutDisplayFunc(display)
    glutTimerFunc(16, timer, 0)  # Start the timer for the first time

    glutMainLoop()

if __name__ == "__main__":
    main()