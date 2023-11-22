import glfw
import time
from serial_communication import SerialReader
from data_processing import LineData
from opengl_rendering import LineRenderer, OpenGLApp

TITLE = "Realtime IMU Data"
NUM_POINTS = 200
# NUM_LINES = 6
fps = 0


def main():
    if not glfw.init():
        raise Exception("GLFW can't be initialized")

    window = glfw.create_window(800, 600, TITLE, None, None)
    if not window:
        glfw.terminate()
        raise Exception("GLFW window can't be created")

    glfw.make_context_current(window)

    # Initialize OpenGL app
    opengl_app = OpenGLApp(window)
    opengl_app.init_gl()

    # Initialize serial reader and line data
    # serial_reader = SerialReader('/dev/cu.usbserial-028574DD', 1000000)
    serial_reader = SerialReader('/dev/cu.usbserial-0283D2D2', 1000000)

    line_datas = [LineData(NUM_POINTS) for _ in range(6)]
    line_renderers = [LineRenderer(NUM_POINTS) for _ in range(6)]
    
    line_datas.append(LineData(2, dynamic_x=True))
    line_renderers.append(LineRenderer(2))
    

    for renderer in line_renderers:
        opengl_app.add_line_renderer(renderer)


    # Main loop
    while not glfw.window_should_close(window):
        glfw.poll_events()

        while not serial_reader.data_queue.empty():
            data, fps = serial_reader.get_data()
            # line_data.update(data.ox)
            line_datas[0].update_y(data.ax)
            line_datas[1].update_y(data.ay)
            line_datas[2].update_y(data.az)
            line_datas[3].update_y(data.gx)
            line_datas[4].update_y(data.gy)
            line_datas[5].update_y(data.gz)
            line_datas[6].update_xy(data.oy, data.ox)
            if fps:
                glfw.set_window_title(window, TITLE + "   ---   " + f"FPS: {fps:.2f}")

        if data:
            # line_renderer.update_data(line_data.get_render_data())
            for i, line_data in enumerate(line_datas):
                opengl_app.update_line_data(i, line_data.get_render_data())
            opengl_app.display()

    # Clean up
    serial_reader.close()  # Close serial port
    glfw.terminate()  # Terminate GLFW

if __name__ == "__main__":
    main()