import numpy as np
import glfw
from OpenGL.GL import *
import imgui
from imgui.integrations.glfw import GlfwRenderer

from modules.imu import IMUData
from modules.stream import IMUStream
from modules.plot import IMUPlot, EventPlot, NNPlot
from modules.render import IMURenderer, EventRenderer, NNRenderer
from modules.metronome import Metronome
from modules.gesture import GestureData
from modules.neuralnet import NeuralNetData, NeuralNetModel

import threading

# Constants and Global Variables
TITLE = "Realtime IMU Data"
N_FRAMES = 1024
N_INPUT_FRAMES = 20
N_MEMORY_FRAMES = 15
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


def update_data(imu_stream, imu_data, imu_plot, window, metronome, event_plot, gesture_data, nn_data, nn_plot):
    new_frames = 0
    while not imu_stream.data_queue.empty():
        new_frames += 1
        frame, FPS = imu_stream.get_frame()

        imu_data.update(frame[0]) #acceleration.x, acceleration.y, acceleration.z
        imu_plot.update(frame[0]) #acceleration.x, acceleration.y, acceleration.z

        gesture_data.update(np.linalg.norm(frame[0])) #acceleration.mag

        i = gesture_data.peak_idx
        nn_data.update(imu_data.data[i:i+N_INPUT_FRAMES], 
                       gesture_data.labels[i+1:i+1+N_MEMORY_FRAMES,1],
                       gesture_data.labels[i,:])
        
        # print(nn_data.output_results)
        nn_plot.update([nn_data.output_results])
        


        # output = nn_model.model.predict([nn_data.input_data[:1], nn_data.input_memory[:1]], 1)
        # nn_data.update_results(output[0][1])
        # print(output[0])

        # j = i
        # if gesture_data.labels[j,1] == 1:
        #     print(imu_data.data[i:i+N_INPUT_FRAMES])
        #     print(gesture_data.labels[i:i+N_MEMORY_FRAMES,1])
        #     print(gesture_data.labels[i,:])
        #     exit()

        # print(np.argwhere(gesture_data.labels[:,1] == True))

        metronome.update()
        event_plot.update([metronome.beats, gesture_data.labels[:,1]])

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
    # impl = init_ui(window)
    
    imu_stream = IMUStream('/dev/cu.usbserial-0283D2D2', 1000000, record=False, read_file=False)
    # imu_stream = IMUStream('/dev/cu.usbserial-028574DD', 1000000, record=False, read_file=False)
    imu_data = IMUData(N_FRAMES)
    imu_plot = IMUPlot(N_FRAMES)

    gesture_data = GestureData(N_FRAMES)

    nn_data = NeuralNetData(N_FRAMES, N_INPUT_FRAMES, N_MEMORY_FRAMES)
    nn_model = NeuralNetModel(nn_data)
    nn_training_thread = threading.Thread(target=nn_model.train, daemon=True)
    nn_inference_thread = threading.Thread(target=nn_model.predict, daemon=True)
        
    metronome = Metronome(N_FRAMES, 60)
    event_plot = EventPlot(N_FRAMES)

    nn_plot = NNPlot(N_FRAMES)

    renderers = [IMURenderer(imu_plot.lines), EventRenderer(event_plot.lines), NNRenderer(nn_plot.lines)]

    nn_training_thread.start()
    nn_inference_thread.start()

    while not glfw.window_should_close(window):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT)
        # update_ui(impl)
        update_data(imu_stream, imu_data, imu_plot, window, metronome, event_plot, gesture_data, nn_data, nn_plot)
        update_data_display(renderers)
        glfw.swap_buffers(window)

    imu_stream.close()
    glfw.terminate()

if __name__ == "__main__":
    main()