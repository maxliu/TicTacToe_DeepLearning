"""

Unilities for tensorflow model

"""

import numpy as np
import tensorflow as tf
import tflearn

import cPickle

# Define the neural network
def build_model(dimTrainX, dimTrainY):
    # This resets all parameters and variables, leave this here
    tf.reset_default_graph()
    
    # Inputs
    net = tflearn.input_data([None, dimTrainX],dtype=tf.float32)

    # Hidden layer(s)
    net = tflearn.fully_connected(net, 10, activation='ReLU')

    # Output layer and training model
    net = tflearn.fully_connected(net, dimTrainY, activation='softmax')
    net = tflearn.regression(net, optimizer='adam', learning_rate=0.01, loss='categorical_crossentropy')

    model = tflearn.DNN(net)
    return model

def getComputerFunc(model):
    def computerNext(humanList, computerList):
        ori = [-1] * 9
        for i in humanList:
            ori[i] = 1
        for i in computerList:
            ori[i] = 0
        y = model.predict([ori])
        return y[0].argmax()
    return computerNext
              