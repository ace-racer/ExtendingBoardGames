import cv2
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
import numpy as np
import os
import random
from collections import Counter, defaultdict
from itertools import product, combinations
import math
import cv2
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score

random.seed(100)

import keras
from keras.layers import Input, Conv2D, Lambda, average, Dense, Flatten,MaxPooling2D, BatchNormalization, Dropout, Activation, Subtract, subtract, GlobalAveragePooling2D
from keras.models import Model, Sequential
from keras.regularizers import l2
from keras import backend as K
from keras.optimizers import SGD,Adam
from keras.losses import binary_crossentropy
from keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard
import numpy.random as rng
from keras.applications.xception import Xception
from sklearn.metrics import confusion_matrix


IMAGE_SIZE = (100, 100)
TOTAL_TRAIN_IMAGES = 10000
TOTAL_TEST_IMAGES = 300

class PrintConfusionMatrix(keras.callbacks.Callback):

    def on_epoch_end(self, epoch, logs={}):
        if epoch % 5 == 0:
            # get the predictions providing the X for the validation data
            y_pred = self.model.predict(self.validation_data[0])
            y_test_pred = [np.argmax(x) for x in y_pred]
            print(confusion_matrix(self.validation_data[1], y_test_pred))
            print("F1 score: {0}".format(f1_score(self.validation_data[1], y_test_pred, average='weighted')))
        return

def f1(y_true, y_pred):
    def recall(y_true, y_pred):
        """Recall metric.

        Only computes a batch-wise average of recall.

        Computes the recall, a metric for multi-label classification of
        how many relevant items are selected.
        """
        total_true_pos = 0
        for type in range(0, 6):
            true_pos = K.sum((y_true == type) & (y_pred == y_true))
            total_true_pos += true_pos
        #true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        #possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
        #recall = true_positives / (possible_positives + K.epsilon())
        return total_true_pos

    def precision(y_true, y_pred):
        """Precision metric.

        Only computes a batch-wise average of precision.

        Computes the precision, a metric for multi-label classification of
        how many selected items are relevant.
        """
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
        precision = true_positives / (predicted_positives + K.epsilon())
        return precision
    precision = precision(y_true, y_pred)
    recall = recall(y_true, y_pred)
    #print("Precision {0} Recall {1}".format(precision, recall))
    #return 2*((precision*recall)/(precision+recall+K.epsilon()))
    return recall


from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
train_datagen = ImageDataGenerator(
        rotation_range=40,
        rescale=1./255,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        fill_mode='nearest')

# this is the augmentation configuration we will use for testing:
# only rescaling
test_datagen = ImageDataGenerator(rescale=1./255)


# batch size
batch_size = 32

# this is a generator that will read pictures found in
# subfolers of 'data/train', and indefinitely generate
# batches of augmented image data
train_generator = train_datagen.flow_from_directory(
        'C:\\Users\\issuser\\Desktop\\ExtendingBoardGamesOnline\\data\\\six_class_data\\v1\\train',  # this is the target directory
        target_size=IMAGE_SIZE,
        batch_size=batch_size,
        class_mode='sparse')

# this is a similar generator, for validation data
validation_generator = test_datagen.flow_from_directory(
        'C:\\Users\\issuser\\Desktop\\ExtendingBoardGamesOnline\\data\\\six_class_data\\v1\\test',
        target_size=IMAGE_SIZE,
        batch_size=batch_size,
        class_mode='sparse')


# number of training epochs
epochs1 = 500
epochs2 = 500

required_input_shape = (*IMAGE_SIZE, 3)

model_folder_name = "models"
tensorboard_logs_folder_location = "logs"

# checkpoint
if not os.path.exists(model_folder_name):
    os.makedirs(model_folder_name)

# tensorboard logs
if not os.path.exists(tensorboard_logs_folder_location):
    os.makedirs(tensorboard_logs_folder_location)

def get_xception_model():
    base_model = Xception(include_top=False, weights='imagenet', input_shape=required_input_shape)
    # add a global spatial average pooling layer

    print("Shape")
    x = base_model.output
    print(x.shape)

    x = GlobalAveragePooling2D()(x)

    # let's add a fully-connected layer
    x = Dense(1024, activation='relu')(x)

    # and a softmax layer
    predictions = Dense(6, activation='softmax')(x)

    # this is the model we will train
    model = Model(inputs=base_model.input, outputs=predictions)

    # first: train only the top layers (which were randomly initialized)
    # i.e. freeze all convolutional InceptionV3 layers
    for layer in base_model.layers:
        layer.trainable = False

    return model

def resize_image(image_location):
    image = cv2.imread(image_location)

    if image.shape[0] != IMAGE_SIZE[0] or image.shape[1] != IMAGE_SIZE[1]:
        # print("Resizing the image: {0}".format(image_location))
        resized_image = cv2.resize(image, IMAGE_SIZE, interpolation = cv2.INTER_AREA)
    else:
        resized_image = image

    return resized_image

def get_validation_data(data_path):
    X, y = [], []
    features_with_labels = []
    type_locations = ["b", "n", "k", "p", "q", "r"]
    type_name_to_label = { "p":0, "b":1, "n":2, "r":3, "q": 4, "k":5 }

    for type_name in type_locations:
            piece_type_folder = os.path.join(data_path, type_name)
            for f in (os.listdir(piece_type_folder)):
                if f.endswith(".jpg"):

                    img_file_loc = os.path.join(piece_type_folder, f)
                    resized_image = resize_image(img_file_loc)
                    label = type_name_to_label[type_name]
                    features_with_labels.append({"feature": resized_image, "label": label})

    random.shuffle(features_with_labels)

    X = [x["feature"] for x in features_with_labels]
    y = [x["label"] for x in features_with_labels]

    X = np.array(X)
    X = X.astype('float32')
    X /= 255

    return X, np.array(y)


xception_model = get_xception_model()


filepath = os.path.join(model_folder_name, "xception.hdf5")
checkpoint = ModelCheckpoint(filepath, monitor='val_f1', verbose=1, save_best_only=True, mode='max')

earlystop = EarlyStopping(monitor='val_f1', min_delta=0.0001, patience=50, verbose=1, mode='max')

tensorboard = TensorBoard(log_dir=tensorboard_logs_folder_location, histogram_freq=0, write_graph=True, write_images=True)

print_confusion_matrix = PrintConfusionMatrix()

callbacks_list = [checkpoint, earlystop, tensorboard, print_confusion_matrix]

adam = Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
xception_model.compile(loss='sparse_categorical_crossentropy', optimizer=adam, metrics=['accuracy', f1])

X_val, y_val = get_validation_data('C:\\Users\\issuser\\Desktop\\ExtendingBoardGamesOnline\\data\\\six_class_data\\v1\\test')

xception_model.fit_generator(
        train_generator,
        steps_per_epoch=TOTAL_TRAIN_IMAGES // batch_size,
        epochs=epochs1,
        validation_data=(X_val, y_val),
        callbacks=callbacks_list)

# at this point, the top layers are well trained and we can start fine-tuning
# convolutional layers from inception V3. We will freeze the bottom N layers
# and train the remaining top layers.

# let's visualize layer names and layer indices to see how many layers
# we should freeze:
#for i, layer in enumerate(xception_model.layers):
#   print(i, layer.name)

# we chose to train the top 3 Xception blocks, i.e. we will freeze
# the first 105 layers and unfreeze the rest:
for layer in xception_model.layers[:106]:
   layer.trainable = False
for layer in xception_model.layers[106:]:
   layer.trainable = True

# we need to recompile the model for these modifications to take effect
# we use SGD with a low learning rate
from keras.optimizers import SGD
xception_model.compile(optimizer=SGD(lr=0.0001, momentum=0.9), loss='sparse_categorical_crossentropy', metrics=['accuracy', f1])

# we train our model again (this time fine-tuning the top 2 inception blocks
# alongside the top Dense layers
xception_model.fit_generator(train_generator,
        steps_per_epoch=TOTAL_TRAIN_IMAGES // batch_size,
        epochs=epochs2,
        validation_data=(X_val, y_val),
        callbacks=callbacks_list)
