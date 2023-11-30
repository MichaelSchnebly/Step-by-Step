import numpy as np
import glfw
from OpenGL.GL import *
import imgui
from imgui.integrations.glfw import GlfwRenderer

from modules.imu import IMUData
from modules.stream import IMUStream
from modules.plot import IMUPlot, MetronomePlot
from modules.data_rendering import PolylineRenderer
from modules.metronome import Metronome

# Constants and Global Variables
TITLE = "Realtime IMU Data"
N_FRAMES = 500
FPS = 0

def init_window():
    """Initializes and returns a GLFW window."""
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)

    # monitor = glfw.get_primary_monitor()
    # mode = glfw.get_video_mode(monitor)
    # window = glfw.create_window(mode.size.width, mode.size.height, TITLE, None, None)
    window = glfw.create_window(1080, 1080, TITLE, None, None)

    if not window:
        glfw.terminate()
        raise Exception("GLFW window can't be created")
    
    glfw.make_context_current(window)
    return window

def init_gl():
    """Initializes OpenGL state."""
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_PROGRAM_POINT_SIZE)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


def init_ui(window):
    """Initializes and returns an ImGUI renderer."""
    imgui.create_context()
    impl = GlfwRenderer(window)
    return impl


def update_ui(impl):
    """Updates the ImGUI renderer."""
    impl.process_inputs()
    imgui.new_frame()
    if imgui.begin("Your Window"):
        imgui.text("Hello, world!")
        if imgui.button("Click me!"):
            print("Button clicked")

    imgui.end()
    imgui.render()
    impl.render(imgui.get_draw_data())


def update_data(stream, data, plot, window, metronome):
    new_frames = 0
    while not stream.data_queue.empty():
        new_frames += 1
        frame, FPS = stream.get_frame()
        data.update(frame[0])
        plot.update(frame[0])
        metronome.update()
        if FPS:
            glfw.set_window_title(window, TITLE + "   ---   " + f"FPS: {FPS:.2f}")

    return new_frames


def update_data_display(renderers):
    for renderer in renderers:
            renderer.render()

def main():
    if not glfw.init():
        raise Exception("GLFW can't be initialized")
    
    window = init_window()
    impl = init_ui(window)
    
    # stream = Stream('/dev/cu.usbserial-0283D2D2', 1000000, record=False, read_file=False)
    stream = IMUStream('/dev/cu.usbserial-028574DD', 1000000, record=False, read_file=False)
    data = IMUData(N_FRAMES)
    plot = IMUPlot(N_FRAMES)
    metronome = Metronome(N_FRAMES, 60)

    renderers = [PolylineRenderer(plot.polylines)]


    while not glfw.window_should_close(window):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT)
        # update_ui(impl)
        update_data(stream, data, plot, window, metronome)
        update_data_display(renderers)
        glfw.swap_buffers(window)

    stream.close()
    glfw.terminate()

if __name__ == "__main__":
    main()