from keras.layers import Dense, GlobalAveragePooling2D, BatchNormalization, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from keras.preprocessing import image
from keras.models import Model, Sequential
from keras import optimizers
import numpy as np

import configurations
import constants
import utils

IMAGE_DIMS = (100, 100)
IMAGE_NUM_CHANNELS = 3

def load_6_class_classifier():
    """
        Load the 6 class classifer model to infer the type of the chess piece
    """

    required_input_shape = (*IMAGE_DIMS, IMAGE_NUM_CHANNELS)

    model = Sequential()
    model.add(Conv2D(32, (3, 3), padding='valid', input_shape=required_input_shape))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    
    model.add(Conv2D(64, (3, 3)))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    
    model.add(Conv2D(128, (3, 3)))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    
    model.add(Dropout(0.5))

    model.add(Flatten())
    
    model.add(Dense(2048))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(Dropout(0.5))

    
    model.add(Dense(256))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(Dropout(0.6))
    
    model.add(Dense(6))
    model.add(Activation('softmax'))
    model.summary()

    # load the model weights
    model.load_weights(configurations.six_class_color_cnn_model_location)
                        
    adam = optimizers.Adam(lr=0.00001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
    model.compile(loss='sparse_categorical_crossentropy', optimizer=adam, metrics=['accuracy'])
    
    return model


def process_images_for_prediction(chess_piece_images):
    """Process the image as required by the color CNN model"""
    processed_chess_piece_images = []
    for chess_piece_image in chess_piece_images:
        processed_chess_piece_image = utils.resize_given_image(chess_piece_image, IMAGE_DIMS)
        processed_chess_piece_images.append(processed_chess_piece_image)

    processed_chess_piece_images = np.array(processed_chess_piece_images)
    processed_chess_piece_images = processed_chess_piece_images.astype('float32')
    processed_chess_piece_images /= 255

    return processed_chess_piece_images