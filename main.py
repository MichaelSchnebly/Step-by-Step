import time
import numpy as np
import glfw

from modules.serial_communication import SerialReader
from modules.data_processing import LineData2D, LineData3D
from modules.opengl_rendering import LineRenderer2D, LineRenderer3D, OpenGLApp

# Constants and Global Variables
TITLE = "Realtime IMU Data"
NUM_POINTS = 200
FPS = 0

def init_window():
    """Initializes and returns a GLFW window."""
    window = glfw.create_window(800, 600, TITLE, None, None)
    if not window:
        glfw.terminate()
        raise Exception("GLFW window can't be created")
    glfw.make_context_current(window)
    return window

def main():
    if not glfw.init():
        raise Exception("GLFW can't be initialized")
    
    window = init_window()
    opengl_app = OpenGLApp(window)
    opengl_app.init_gl()

    serial_reader = SerialReader('/dev/cu.usbserial-028574DD', 1000000)
    # serial_reader = SerialReader('/dev/cu.usbserial-0283D2D2', 1000000)

    line_datas = [LineData2D(NUM_POINTS) for _ in range(6)] + [LineData3D(NUM_POINTS)]
    line_renderers = [LineRenderer2D(NUM_POINTS) for _ in range(6)] + [LineRenderer3D(NUM_POINTS)]
    
    for renderer in line_renderers:
        opengl_app.add_line_renderer(renderer)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        data = None
        while not serial_reader.data_queue.empty():
            data, FPS = serial_reader.get_data()
            line_datas[6].update(data[2])
            # data[0] = line_datas[6].rotate(data[0])
            line_datas[0].update(data[0, 0])
            line_datas[1].update(data[0, 1])
            line_datas[2].update(data[0, 2])
            line_datas[3].update(data[1, 0])
            line_datas[4].update(data[1, 1])
            line_datas[5].update(data[1, 2])
            
            if FPS:
                glfw.set_window_title(window, TITLE + "   ---   " + f"FPS: {FPS:.2f}")

        if data is not None:
            for i, line_data in enumerate(line_datas):
                opengl_app.update_line_data(i, line_data.get_render_data())
            opengl_app.display()

    # Clean up
    serial_reader.close()  # Close serial port
    glfw.terminate()  # Terminate GLFW

if __name__ == "__main__":
    main()