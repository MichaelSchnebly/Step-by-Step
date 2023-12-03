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
    def __init__(self, nn_model):
        self.PAUSE = False
        self.ACC_XYZ = False
        self.ACC_MAG = False
        self.METRONOME = False
        self.LABELLING = False

        self.nn_model = nn_model
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
                print("Pausing...")
                self.nn_model.stop_training()
                self.nn_model.stop_inference()
            else:
                print("Starting...")
                self.nn_model.start_training()
                self.nn_model.start_inference()
            
        if key == glfw.KEY_1 and action == glfw.PRESS:
            print("1: ACC_XYZ")
            self.ACC_XYZ = not self.ACC_XYZ
        if key == glfw.KEY_2 and action == glfw.PRESS:
            print("2: ACC_MAG")
            self.ACC_MAG = not self.ACC_MAG
        if key == glfw.KEY_3 and action == glfw.PRESS:
            print("3: METRONOME")
            self.METRONOME = not self.METRONOME
        if key == glfw.KEY_4 and action == glfw.PRESS:
            print("4: LABELLING")
            self.LABELLING = not self.LABELLING

        if key == glfw.KEY_5 and action == glfw.PRESS:
            self.NN_INFERENCE = not self.NN_INFERENCE
            if self.NN_INFERENCE:
                self.nn_model.start_inference()
            else:
                self.nn_model.stop_inference()
            print("5: NN_INFERENCE " + str(self.NN_INFERENCE))

        if key == glfw.KEY_6 and action == glfw.PRESS:
            self.NN_TRAINING = not self.NN_TRAINING
            if self.NN_TRAINING:
                self.nn_model.start_training()
            else:
                self.nn_model.stop_training()
            print("6: NN_TRAINING " + str(self.NN_TRAINING))


        if key == glfw.KEY_7 and action == glfw.PRESS:
            print("7: Exporting model...")
            self.EXPORT = not self.EXPORT
        if key == glfw.KEY_R and action == glfw.PRESS:
            print("R: Resetting...")
            self.reset()

    def reset(self):
        self.PAUSE = False
        self.ACC_XYZ = False
        self.ACC_MAG = False
        self.METRONOME = False
        self.LABELLING = False
        self.NN_INFERENCE = False
        self.NN_TRAINING = False
        self.EXPORT = False

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
        
        nn_plot.shift()

        metronome.update()
        event_plot.update([metronome.beats, gesture_data.labels[:,1]])

        if FPS:
            glfw.set_window_title(window, TITLE + "   ---   " + f"FPS: {FPS:.2f}")

    return new_frames


def update_data_display(renderers):
    for renderer in renderers:
            renderer.render()

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



    # nn_training_thread = threading.Thread(target=nn_model.training, daemon=True)
    # nn_inference_thread = threading.Thread(target=nn_model.inference, daemon=True)
        
    

    nn_plot = NNPlot(N_FRAMES)
    nn_data = NeuralNetData(N_FRAMES, N_INPUT_FRAMES, N_MEMORY_FRAMES, gesture_data.peak_idx)
    nn_model = NeuralNetModel(nn_data, nn_plot)

    event_plot = EventPlot(N_FRAMES)

    renderers = [EventRenderer(event_plot.lines), IMURenderer(imu_plot.lines), NNRenderer(nn_plot.lines)]

    HOTKEYS = Hotkeys(nn_model)
    glfw.set_key_callback(window, HOTKEYS.update)

    while not glfw.window_should_close(window):
        if not HOTKEYS.PAUSE:
            glfw.poll_events()
            glClear(GL_COLOR_BUFFER_BIT)
            # update_ui(impl)
            update_data(imu_stream, imu_data, imu_plot, window, metronome, event_plot, gesture_data, nn_data, nn_plot)
            update_data_display(renderers)
            glfw.swap_buffers(window)
        else:
            glfw.wait_events()
    
    imu_stream.close()
    nn_model.stop_training()
    nn_model.stop_inference()
    glfw.terminate()

if __name__ == "__main__":
    main()