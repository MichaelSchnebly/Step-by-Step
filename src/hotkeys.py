import glfw

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
                print("3: Starting Labeling...")
                self.gesture_data.start_labeling()
            else:
                print("3: Stopping Labeling...")
                self.gesture_data.stop_labeling()

        if key == glfw.KEY_4 and action == glfw.PRESS:
            self.NN_INFERENCE = not self.NN_INFERENCE
            if self.NN_INFERENCE:
                self.nn_model.start_inference()
                self.nn_plot.lines[0].start()
            else:
                self.nn_model.stop_inference()
                self.nn_plot.lines[0].stop()
            print("4: NN_INFERENCE " + str(self.NN_INFERENCE))

        if key == glfw.KEY_5 and action == glfw.PRESS:
            self.NN_TRAINING = not self.NN_TRAINING
            if self.NN_TRAINING:
                self.nn_model.start_training()
            else:
                self.nn_model.stop_training()
            print("5: NN_TRAINING " + str(self.NN_TRAINING))



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
