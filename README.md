# Step-by-Step: Training IMU-based Gestures with Live Feedback
This is a software tool that allows users to train gesture recognition models with live audiovisual feedback. Step-by-Step uses a simple neural network to learn to recognize and distinguish multiple gestures in IMU timeseries data. Users can train the model by performing gestures and receiving live feedback on the model’s performance. Step-by-Step is designed to be accessible to users with no machine learning experience, while providing a powerful codebase for advanced users.

![Real-time Training](docs/figures/realtime_training.jpg)
*Figure: Live Learning Feedback: The user performs a gesture and receives live feedback on the model’s performance. Bottom Panel: 10 seconds of training data. Acceleration components (x, y, z) are shown in color; magnitude is shown in grey. Each magnitude peak is marked by a thin vertical line, indicating it has been labelled as a gesture in the training data. Top Panel: 10 seconds of inference data. At t = 0 seconds the neural network is completely untrained. Naive to what is and is not a gesture, it predicts gesture and non-gesture with equal probability (0.5). As the model trains on non-gesture date, it begins to predict non-gesture with higher probability. At t = 5 seconds, the model has converged on a solution that reliably distinguishes non-gesture. At t = 10 seconds, the model has converged on a solution that reliably distinguishes gestures. Given more training data and time to learn, the model’s performance would continue to improve with gessture and non-gesture probabilities approaching 1 and 0, respectively. See supplementary video for live demo in the github repo.*

## System Overview

The system consists of hardware and software components. The hardware measures body movement and streams the data to a computer. The software processes the data, trains a neural network, and provides live feedback to the user.

### Hardware

The hardware used for measuring body movement is the Bosch BNO-055, a 9-axis IMU that includes an accelerometer, gyroscope, and magnetometer. The IMU streams data via I2C to a microcontroller (Espressif ESP8266) which passes that data on to a laptop (Macbook Pro 2017) via USB for further processing.

### Software

The software is written in Python and structured into three main components: data processing, neural network, and user interface. The data processing component handles data collection, labelling, and storage. The neural network component handles model structure, training, and inference. The user interface component handles user interaction and feedback.

## Data Processing

The IMU data is collected as a timeseries of frames. Each frame is a 3D vector representing linear acceleration in each of the three axes: x, y, and z. The data is collected at a rate of 100 Hz and can be streamed directly from an IMU, recorded to a file, or loaded from a file.

## Neural Network

The neural network is a shallow, two-branched model. One branch represents a recent history of sensor values while the other represents a recent history of model outputs. Combining the information from these two sources, the model is trained to maximize the probability of the correct gesture and minimize the probabilities of all other gestures.

## User Interface and Control

All rendering is done using OpenGL. With keyboard inputs, the user can control various aspects of the application. The user can start and stop data collection, data labelling, model training, and model inference. For more detail on control, please see the "Hotkeys.py" file.

## Results

After just a few examples of a gesture, the model converges on a solution that reliably distinguishes gesture from non-gesture. Performance improves as more examples are provided. A representative example of the model learning to recognize a single gesture in just 10 seconds is shown in the paper and at the top of this page.

For more details, please refer to the paper in the `docs` directory.