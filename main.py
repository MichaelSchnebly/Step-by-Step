import time
import numpy as np
import glfw
from OpenGL import GL
import imgui
from imgui.integrations.glfw import GlfwRenderer

from modules.data_stream import Stream
from modules.data_processing import PolylineData
from modules.opengl_rendering import PolylineRenderer, OpenGLApp

# Constants and Global Variables
TITLE = "Realtime IMU Data"
NUM_POINTS = 500
FPS = 0

def init_window():
    """Initializes and returns a GLFW window."""
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)

    monitor = glfw.get_primary_monitor()
    mode = glfw.get_video_mode(monitor)
    window = glfw.create_window(mode.size.width, mode.size.height, TITLE, None, None)

    if not window:
        glfw.terminate()
        raise Exception("GLFW window can't be created")
    glfw.make_context_current(window)

    #OpenGL Version Check
    opengl_version = GL.glGetString(GL.GL_VERSION)
    print(f"OpenGL version: {opengl_version.decode('utf-8')}")

    #OpenGL Line Width Check
    line_width_range = check_line_width_support()
    return window

def check_line_width_support():
    range = GL.glGetFloatv(GL.GL_LINE_WIDTH_RANGE)
    print(f"Supported line width range: {range[0]} to {range[1]}")
    return range

def main():
    if not glfw.init():
        raise Exception("GLFW can't be initialized")
    
    window = init_window()
    opengl_app = OpenGLApp(window)
    opengl_app.init_gl()

    # stream = Stream('/dev/cu.usbserial-0283D2D2', 1000000, record=False, read_file=False)
    stream = Stream('/dev/cu.usbserial-028574DD', 1000000, record=False, read_file=False)

    polylines = [PolylineData(NUM_POINTS, 0.002, np.array([0, 1, 1, 1]), [1, 1/3, 1], [0, 2/3, 0]),
                 PolylineData(NUM_POINTS, 0.002, np.array([1, 0, 1, 1]), [1, 1/3, 1], [0, 0, 0]),
                 PolylineData(NUM_POINTS, 0.002, np.array([1, 0.7, 0, 1]), [1, 1/3, 1], [0, -2/3, 0])]
    
    line_renderers = [PolylineRenderer(polylines)]

    opengl_app.add_renderer(line_renderers[0])

    while not glfw.window_should_close(window):
        glfw.poll_events()

        data = None
        while not stream.data_queue.empty():
            data, FPS = stream.get_data()
            polylines[0].update(data[0, 0])
            polylines[1].update(data[0, 1])
            polylines[2].update(data[0, 2])
            
            if FPS:
                glfw.set_window_title(window, TITLE + "   ---   " + f"FPS: {FPS:.2f}")

        # if data is not None:
        opengl_app.display()

    # Clean up
    stream.close()  # Close serial port
    glfw.terminate()  # Terminate GLFW

if __name__ == "__main__":
    main()