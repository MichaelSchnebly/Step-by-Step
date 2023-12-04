from keras.layers import Input, Dense, Conv1D, Flatten, GlobalMaxPooling1D, concatenate
from keras.models import Model
from keras.losses import CategoricalCrossentropy
from keras.optimizers import Adam
from keras.utils import plot_model
# from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import numpy as np
# import coremltools as ct
import time
import threading


class NeuralNetData:
    def __init__(self, n_samples, n_input_frames, n_memory_frames, labeling_delay, n_features=3, n_labels=2):
        self.batch_size = 16
        self.batch_count = 0

        self.n_samples = n_samples
        self.n_input_frames = n_input_frames
        self.n_memory_frames = n_memory_frames
        self.labeling_delay = labeling_delay
        self.n_features = n_features
        self.n_labels = n_labels
        
        self.input_data = np.zeros((n_samples, n_input_frames, n_features), dtype=np.float32)
        self.input_memory = np.zeros((n_samples, n_memory_frames, 1), dtype=np.float32)
        self.output_labels = np.zeros((n_samples, n_labels), dtype=np.float32)
        self.output_results = np.full((n_samples), 0.5, dtype=np.float32)
    
    def update(self, input_data_window, input_memory_window, output_labels):
        self.batch_count += 1
        self.input_data[1:, :, :] = self.input_data[:-1, :, :]
        self.input_data[0, :, :] = input_data_window

        self.input_memory[1:, :, :] = self.input_memory[:-1, :, :]
        self.input_memory[0, :, 0] = input_memory_window

        self.output_labels[1:, :] = self.output_labels[:-1, :]
        self.output_labels[0, :] = output_labels

    def update_results(self, output_result):
        i = self.batch_count + self.labeling_delay
        b = self.batch_size
        # j = 0 if i - b < 0 else i - b
        self.output_results[i+b:] = self.output_results[i:-b]
        self.output_results[i:i+b] = output_result
        # if output_result > 0.5:
        #     print(output_result)



class NeuralNetModel:
    def __init__(self, nn_data, nn_plot):
        self.nn_data = nn_data
        self.nn_plot = nn_plot

        self.run_training = False
        self.run_inference = False

        self.model = self.build()

    
    def start_training(self):
        if not self.run_training:
            self.run_training = True
            self.training_thread = threading.Thread(target=self.training, daemon=True)
            self.training_thread.start()

    def stop_training(self):
        if self.run_training:
            self.run_training = False
            self.training_thread.join()

    def start_inference(self):
        if not self.run_inference:
            self.run_inference = True
            self.inference_thread = threading.Thread(target=self.inference, daemon=True)
            self.inference_thread.start()

    def stop_inference(self):
        if self.run_inference:
            self.run_inference = False
            self.inference_thread.join()

    def training(self):
        while self.run_training:
            INPUT_DATA = self.nn_data.input_data
            INPUT_MEMORY = self.nn_data.input_memory
            OUTPUT_LABELS = self.nn_data.output_labels
            self.model.fit([INPUT_DATA, INPUT_MEMORY],
                                OUTPUT_LABELS,
                                batch_size=32,
                                epochs=1,
                                verbose=0)
            time.sleep(0.001)


    def inference(self):
        self.nn_data.batch_count = 0
        
        while self.run_inference:
            count = self.nn_data.batch_count
            size = self.nn_data.batch_size
            if count >= size:
                pre_diff = count - size
                self.nn_data.batch_count = pre_diff
                INPUT_DATA = self.nn_data.input_data[pre_diff:pre_diff+size]
                INPUT_MEMORY = self.nn_data.input_memory[pre_diff:pre_diff+size]
                output = self.model.predict([INPUT_DATA, INPUT_MEMORY], size, verbose=0)
                # post_diff = self.nn_data.batch_count
                # print("PRE: ", pre_diff, "POST: ", post_diff)
                self.nn_data.update_results(output[:,1])
                self.nn_plot.update([self.nn_data.output_results])
            time.sleep(0.01)


    def build(self):
        INPUT_DATA = self.nn_data.input_data
        INPUT_MEMORY = self.nn_data.input_memory
        OUTPUT_LABELS = self.nn_data.output_labels
        Conv_Input = Input(shape=(INPUT_DATA.shape[1], INPUT_DATA.shape[2]), name='input')
        Conv_Branch = Conv1D(8, INPUT_DATA.shape[1], activation="relu")(Conv_Input) #N_FILTERS = 8
        Conv_Branch = Flatten()(Conv_Branch)
        Conv_Branch = Model(inputs=Conv_Input, outputs=Conv_Branch)

        Memory_Input = Input(shape=(INPUT_MEMORY.shape[1], INPUT_MEMORY.shape[2]), name='memory')
        Memory_Branch = GlobalMaxPooling1D()(Memory_Input)
        Memory_Branch = Model(inputs=Memory_Input, outputs=Memory_Branch)

        MODEL = concatenate([Conv_Branch.output, Memory_Branch.output])
        MODEL = Dense(OUTPUT_LABELS.shape[1], activation="softmax", name='output')(MODEL)
        MODEL = Model(inputs=[Conv_Branch.input, Memory_Branch.input], outputs=MODEL, name='LaefNet')

        OPT = Adam(learning_rate=0.001)
        MODEL.compile(loss=CategoricalCrossentropy(), optimizer=OPT, metrics=["categorical_accuracy"])
        MODEL.summary()

        # plot_model(MODEL, to_file='images/model_diagram.svg', show_shapes=True, dpi = 60)

        return MODEL