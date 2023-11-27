import glfw
from OpenGL.GL import *

# Initialize GLFW and create a window (needed to initialize OpenGL context)
if not glfw.init():
    raise Exception("GLFW can't be initialized")

window = glfw.create_window(800, 600, "OpenGL Window", None, None)
if not window:
    glfw.terminate()
    raise Exception("GLFW window can't be created")

glfw.make_context_current(window)

# Query OpenGL version
version = glGetString(GL_VERSION)
print("OpenGL version:", version.decode())

glfw.terminate()