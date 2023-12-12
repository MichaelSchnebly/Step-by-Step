import glfw
from OpenGL.GL import *

from src.imu import IMUData
from src.stream import IMUStream
from src.plot import IMUPlot, EventPlot, NNPlot
from src.render import IMURenderer, EventRenderer, NNRenderer
from src.metronome import Metronome
from src.gesture import GestureData
from src.neuralnet import NeuralNetData, NeuralNetModel
from src.hotkeys import Hotkeys

import numpy as np

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
    glClearColor(0.0, 0.0, 0.0, 2.0)
    glEnable(GL_MULTISAMPLE)
    # glEnable(GL_PROGRAM_POINT_SIZE)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_LINE_SMOOTH)


def update_data(imu_stream, imu_data, imu_plot, window, metronome, event_plot, gesture_data, nn_data, nn_plot):
    while not imu_stream.data_queue.empty():

        frame, FPS = imu_stream.get_frame()
        imu_data.update(frame[0]) #acceleration.x, acceleration.y, acceleration.z
        imu_plot.update(frame[0]) #acceleration.x, acceleration.y, acceleration.z
        gesture_data.update(np.linalg.norm(frame[0])) #acceleration.mag

        metronome.update()
        
        event_plot.update([metronome.beats, gesture_data.labels[:,1]])

        i = gesture_data.peak_idx
        nn_data.update(imu_data.data[i:i+N_INPUT_FRAMES], 
                       gesture_data.labels[i+1:i+1+N_MEMORY_FRAMES,1],
                       gesture_data.labels[i,:])
        nn_plot.shift()

        if gesture_data.labels[gesture_data.peak_idx,1] == 1:
            metronome.low_beat.play()


        if FPS:
            glfw.set_window_title(window, TITLE + "   ---   " + f"FPS: {FPS:.2f}")



def main():
    if not glfw.init():
        raise Exception("GLFW can't be initialized")
    
    window = init_window()
    init_gl()

    imu_plot = IMUPlot(N_FRAMES)
    imu_data = IMUData(N_FRAMES)
    imu_stream = IMUStream('/dev/cu.usbserial-0283D2D2', 1000000, record=False, read_file=False) #'/dev/cu.usbserial-028574DD'

    metronome = Metronome(N_FRAMES, 60)

    gesture_data = GestureData(N_FRAMES)

    nn_plot = NNPlot(N_FRAMES)
    nn_data = NeuralNetData(N_FRAMES, N_INPUT_FRAMES, N_MEMORY_FRAMES, gesture_data.peak_idx)
    nn_model = NeuralNetModel(nn_data, nn_plot)

    event_plot = EventPlot(N_FRAMES)

    event_renderer = EventRenderer(event_plot.lines)
    imu_renderer = IMURenderer(imu_plot.lines)
    nn_renderer = NNRenderer(nn_plot.lines, nn_data.batch_size + nn_data.labeling_delay + 10)

    

    HOTKEYS = Hotkeys(imu_stream, imu_plot, metronome, gesture_data, nn_model, nn_plot)
    glfw.set_key_callback(window, HOTKEYS.update)

    while not glfw.window_should_close(window):
        if not HOTKEYS.PAUSE:
            glfw.poll_events()
            glClear(GL_COLOR_BUFFER_BIT)

            update_data(imu_stream, imu_data, imu_plot, window, metronome, event_plot, gesture_data, nn_data, nn_plot)
            event_renderer.render()
            imu_renderer.render()
            nn_renderer.render()

            glfw.swap_buffers(window)
        else:
            glfw.wait_events()
    
    
    nn_model.stop_training()
    nn_model.stop_inference()
    imu_stream.stop()
    glfw.terminate()

if __name__ == "__main__":
    main()