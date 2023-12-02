from keras.layers import Input, Dense, Conv1D, Flatten, GlobalMaxPooling1D, concatenate
from keras.models import Model
from keras.losses import CategoricalCrossentropy
from keras.optimizers import Adam
# from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import numpy as np
# import coremltools as ct
import time


class NeuralNetData:
    def __init__(self, n_samples, n_input_frames, n_memory_frames, n_features=3, n_labels=2):
        
        self.batch_size = 32
        self.batch_count = 0
        self.count = 0

        self.n_samples = n_samples
        self.n_input_frames = n_input_frames
        self.n_memory_frames = n_memory_frames
        self.n_features = n_features
        self.n_labels = n_labels
        
        self.input_data = np.zeros((n_samples, n_input_frames, n_features), dtype=np.float32)
        self.input_memory = np.zeros((n_samples, n_memory_frames, 1), dtype=np.float32)
        self.output_labels = np.zeros((n_samples, n_labels), dtype=np.float32)
        self.output_results = np.zeros((n_samples), dtype=np.float32)
    
    def update(self, input_data_window, input_memory_window, output_labels):
        self.count += 1
        self.batch_count += 1
        self.input_data[1:, :, :] = self.input_data[:-1, :, :]
        self.input_data[0, :, :] = input_data_window

        self.input_memory[1:, :, :] = self.input_memory[:-1, :, :]
        self.input_memory[0, :, 0] = input_memory_window

        self.output_labels[1:, :] = self.output_labels[:-1, :]
        self.output_labels[0, :] = output_labels

    def update_results(self, output_result):
        i = self.batch_count + 10
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
        self.model = self.build()
        

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

        return MODEL


    def train(self): #CLASS_WEIGHTS
        
        while(True):
            INPUT_DATA = self.nn_data.input_data
            INPUT_MEMORY = self.nn_data.input_memory
            OUTPUT_LABELS = self.nn_data.output_labels
            # if np.sum(OUTPUT_LABELS[:1,1]) >= 1:
            #     print("\n\n")
            #     print(INPUT_DATA[:1])
            #     print(INPUT_MEMORY[:1])
            #     print(OUTPUT_LABELS[:1])
            #     output_result = self.infer(INPUT_DATA[:1], INPUT_MEMORY[:1])
            #     print(output_result)
            #     print("\n\n")
            self.model.fit([INPUT_DATA, INPUT_MEMORY],
                                OUTPUT_LABELS,
                                batch_size=32,
                                # class_weight=CLASS_WEIGHTS,
                                epochs=1,
                                verbose=0)
            
            time.sleep(0.001)
                
                
                
                # self.nn_data.update_results(output_result[0])
            # else:
            #     time.sleep(0.01)
            
    def predict(self):
        while True:
            count = self.nn_data.batch_count
            size = self.nn_data.batch_size
            if count >= size:
                pre_diff = count - size
                self.nn_data.batch_count = pre_diff
                INPUT_DATA = self.nn_data.input_data[pre_diff:pre_diff+size]
                INPUT_MEMORY = self.nn_data.input_memory[pre_diff:pre_diff+size]
                output = self.model.predict([INPUT_DATA, INPUT_MEMORY], size, verbose=0)
                post_diff = self.nn_data.batch_count
                # print("Pre: " + str(pre_diff) + "   Post: " + str(post_diff))
                self.nn_data.update_results(output[:,1])
                self.nn_plot.update([self.nn_data.output_results])
                

            # INPUT_DATA = self.nn_data.input_data[:1]
            # INPUT_MEMORY = self.nn_data.input_memory[:1]
            # OUTPUT_LABELS = self.nn_data.output_labels[:1]
            # if np.sum(OUTPUT_LABELS[:,1]) == 1:
            # output = self.model.predict([INPUT_DATA, INPUT_MEMORY], 32, verbose=0)
            # print(self.nn_data.count)
            # self.nn_data.update_results(output[0][1])
            # else:
            time.sleep(0.01)


    
    # def infer(self, input_data_window, input_memory_window):
    #     return self.model.predict([input_data_window, input_memory_window], 1)


# history = self.model.fit([INPUT_DATA, INPUT_MEMORY],
            #                     OUTPUT_LABELS,
            #                     batch_size=32,
            #                     # class_weight=CLASS_WEIGHTS,
            #                     epochs=1)

# loss = history.history['loss']
# plt.plot(range(len(loss)), loss)
# plt.ylim([0, 0.35])
# plt.show()

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
