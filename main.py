import glfw
import time
from serial_communication import SerialReader
from data_processing import LineData
from opengl_rendering import LineRenderer, OpenGLApp

# Constants
NUM_POINTS = 200


def main():
    if not glfw.init():
        raise Exception("GLFW can't be initialized")

    window = glfw.create_window(800, 600, "Realtime IMU Data", None, None)
    if not window:
        glfw.terminate()
        raise Exception("GLFW window can't be created")

    glfw.make_context_current(window)

    # Initialize OpenGL app
    opengl_app = OpenGLApp(window)
    opengl_app.init_gl()

    # Initialize serial reader and line data
    serial_reader = SerialReader('/dev/cu.usbserial-028574DD', 1000000)
    line_data = LineData(NUM_POINTS)
    line_renderer = LineRenderer(NUM_POINTS)

    opengl_app.add_line_renderer(line_renderer)

    # Main loop
    while not glfw.window_should_close(window):
        glfw.poll_events()

        while not serial_reader.data_queue.empty():
            data = serial_reader.get_data()
            line_data.update(data.ox)

        if data:
            line_renderer.update_data(line_data.get_render_data())
            opengl_app.display()

    # Clean up
    serial_reader.close()  # Close serial port
    glfw.terminate()  # Terminate GLFW

if __name__ == "__main__":
    main()