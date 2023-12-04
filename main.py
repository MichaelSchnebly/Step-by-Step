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

# HOTKEY CONDITIONALS
class Hotkeys:
    def __init__(self, imu_stream, imu_plot, metronome, gesture_data, nn_model, nn_plot):
        self.PAUSE = False

        self.imu_stream = imu_stream
        self.IMU_STREAM = False

        self.imu_plot = imu_plot
        self.MAGNITUDE = False

        self.metronome = metronome
        self.METRONOME = False

        self.gesture_data = gesture_data
        self.LABELING = False

        self.nn_model = nn_model
        self.nn_plot = nn_plot
        self.NN_INFERENCE = False
        self.NN_TRAINING = False

        self.EXPORT = False

    def update(self, window, key, scancode, action, mods):
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            print("ESC: Exiting...")
            glfw.set_window_should_close(window, True)
        if key == glfw.KEY_SPACE and action == glfw.PRESS:
            self.PAUSE = not self.PAUSE
            if self.PAUSE:
                print("SPACE: Pausing Application...")
                self.nn_model.stop_training()
                self.nn_model.stop_inference()
                self.imu_stream.stop()
                self.metronome.stop()
            else:
                print("SPACE: Starting Application...")
                if self.METRONOME:
                    self.metronome.start()
                if self.IMU_STREAM:
                    self.imu_stream.start()
                if self.NN_INFERENCE:
                    self.nn_model.start_inference()
                if self.NN_TRAINING:    
                    self.nn_model.start_training()
            
        if key == glfw.KEY_1 and action == glfw.PRESS:
            self.IMU_STREAM = not self.IMU_STREAM
            if self.IMU_STREAM:
                print("1: Starting IMU Stream...")
                self.imu_stream.start()
                self.imu_plot.lines[0].start()
                self.imu_plot.lines[1].start()
                self.imu_plot.lines[2].start()
            else:
                print("1: Stopping IMU Stream...")
                self.imu_stream.stop()
                self.imu_plot.lines[0].stop()
                self.imu_plot.lines[1].stop()
                self.imu_plot.lines[2].stop()

        if key == glfw.KEY_2 and action == glfw.PRESS:
            self.MAGNITUDE = not self.MAGNITUDE
            if self.MAGNITUDE:
                print("2: Starting Magnitude Plot...")
                self.imu_plot.lines[3].start()
            else:
                print("2: Stopping Magnitude Plot...")
                self.imu_plot.lines[3].stop()

        if key == glfw.KEY_M and action == glfw.PRESS:
            self.METRONOME = not self.METRONOME
            if self.METRONOME:
                print("Starting Metronome...")
                self.metronome.start()
            else:
                print("Stopping Metronome...")
                self.metronome.stop()

        if key == glfw.KEY_3 and action == glfw.PRESS:
            self.LABELING = not self.LABELING
            if self.LABELING:
                print("4: Starting Labeling...")
                self.gesture_data.start_labeling()
            else:
                print("4: Stopping Labeling...")
                self.gesture_data.stop_labeling()

        if key == glfw.KEY_4 and action == glfw.PRESS:
            self.NN_INFERENCE = not self.NN_INFERENCE
            if self.NN_INFERENCE:
                self.nn_model.start_inference()
                self.nn_plot.lines[0].start()
            else:
                self.nn_model.stop_inference()
                self.nn_plot.lines[0].stop()
            print("5: NN_INFERENCE " + str(self.NN_INFERENCE))

        if key == glfw.KEY_5 and action == glfw.PRESS:
            self.NN_TRAINING = not self.NN_TRAINING
            if self.NN_TRAINING:
                self.nn_model.start_training()
            else:
                self.nn_model.stop_training()
            print("6: NN_TRAINING " + str(self.NN_TRAINING))

        # if key == glfw.KEY_7 and action == glfw.PRESS:
        #     print("7: Exporting model...")
        #     self.EXPORT = not self.EXPORT

    #     if key == glfw.KEY_R and action == glfw.PRESS:
    #         print("R: Resetting...")
    #         self.reset()

    # def reset(self):
    #     self.PAUSE = False
    #     self.IMU_STREAM = False
    #     self.MAGNITUDE = False
    #     self.METRONOME = False
    #     self.LABELING = False
    #     self.NN_INFERENCE = False
    #     self.NN_TRAINING = False
    #     self.EXPORT = False


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
    glEnable(GL_MULTISAMPLE)
    # glEnable(GL_PROGRAM_POINT_SIZE)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_LINE_SMOOTH)


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


        if FPS:
            glfw.set_window_title(window, TITLE + "   ---   " + f"FPS: {FPS:.2f}")



def on_key(window, key, scancode, action, mods):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

def main():
    if not glfw.init():
        raise Exception("GLFW can't be initialized")
    
    
    window = init_window()
    init_gl()

    imu_plot = IMUPlot(N_FRAMES)
    imu_data = IMUData(N_FRAMES)
    imu_stream = IMUStream('/dev/cu.usbserial-028574DD', 1000000, record=False, read_file=False) #'dev/cu.usbserial-0283D2D2'
    
    

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
            # update_ui(impl)

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