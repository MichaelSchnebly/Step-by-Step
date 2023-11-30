import tensorflow.python.keras.optimizer_v1
from keras.layers import *
from keras.models import *
from keras.losses import *
from keras.optimizers import *
# from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import numpy as np
# import coremltools as ct

class NeuralNetData:
    def __init__(self, n_samples, n_input_frames, n_memory_frames, n_features=3, n_labels=2):
        self.n_samples = n_samples
        self.n_input_frames = n_input_frames
        self.n_memory_frames = n_memory_frames
        self.n_features = n_features
        self.n_labels = n_labels
        
        self.input_data = np.zeros((n_samples, n_input_frames, n_features), dtype=np.float32)
        self.input_memory = np.zeros((n_samples, n_memory_frames, n_features), dtype=np.float32)
        self.output_labels = np.zeros((n_samples, n_labels), dtype=np.float32)
    
    def update(self, input_data_window, input_memory_window, output_labels):
        self.input_data[1:, :, :] = self.input_data[:-1, :, :]
        self.input_data[0, :, :] = input_data_window

        self.input_memory[1:, :, :] = self.input_memory[:-1, :, :]
        self.input_memory[0, :, :] = input_memory_window

        self.output_labels[1:, :] = self.output_labels[:-1, :]
        self.output_labels[0, :] = output_labels



class NeuralNet:
    def build(self, INPUT, INPUT_MEMORY, OUTPUT_LABELS):
        Conv_Input = Input(shape=(INPUT.shape[1], INPUT.shape[2]), name='input')
        Conv_Branch = Conv1D(8, INPUT.shape[1], activation="relu")(Conv_Input) #N_FILTERS = 8
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

        return MODEL


    def train(self, MODEL, INPUT_DATA, INPUT_MEMORY, OUTPUT_LABELS, CLASS_WEIGHTS, EPOCHS):

        history = MODEL.fit([INPUT_DATA, INPUT_MEMORY],
                            OUTPUT_LABELS,
                            batch_size=32,
                            class_weight=CLASS_WEIGHTS,
                            epochs=EPOCHS)

        loss = history.history['loss']
        plt.plot(range(len(loss)), loss)
        # plt.ylim([0, 0.35])
        plt.show()

        return MODEL


# def assess(MODEL, INPUT_DATA, INPUT_MEMORY, OUTPUT_LABELS):
#     predicted_output = MODEL.predict([INPUT_DATA, INPUT_MEMORY])
#     actual_output = OUTPUT_LABELS

#     for i in range(OUTPUT_LABELS.shape[1]):
#         print()
#         print('Confusion Matrix: ' + str(i))
#         print(confusion_matrix(actual_output[:, i], np.around(predicted_output[:, i])))
#         plt.scatter(predicted_output[:, i], actual_output[:, i], alpha=.005)
#         plt.show()
#         print()

    # print()
    # print('Confusion Matrix: 0')
    # print(confusion_matrix(actual_output[:, 0], np.around(predicted_output[:, 0])))
    # plt.scatter(predicted_output[:, 0], actual_output[:, 0], alpha=.005)
    # plt.show()
    # print()


# def save(MODEL, session, parts):
#     directory = '/Users/admin/data/laef/recordings/'
#     path = directory + session + '/NN/NN_Firefly'
#     path += "".join(["_" + p for p in parts])

#     MODEL.save(path)

#     MODEL_COREML = ct.convert(MODEL)
#     MODEL_COREML.save(path + '.mlmodel')
#     print("Model Saved!")
