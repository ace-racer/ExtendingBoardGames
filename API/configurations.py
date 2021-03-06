three_class_cnn_model_location = "models/3_class_cnn.hdf5"
six_class_cnn_model_location = "models/6_class_cnn.hdf5"
six_class_xception_model_location = "models/6_class_xception.hdf5"
six_class_color_cnn_model_location = "models/6_class_color_cnn.hdf5"

#Redis Configurations
redis_host = "localhost"
redis_port = 6379

#Mongo DB Configurations
MONGO_DB_HOST="localhost"
MONGO_DB_PORT=27017

#Generated Images location
IMAGES_LOCATION = "outputs/"

# Application Flags
APP_FLAGS = {
    "SEND_DELTA_ONLY" : False,
    "USE_MONGO": False,
    "USE_REDIS": False
}

#Chess board resized image dimension
REQUIRED_CHESS_BOARD_DIMENSION = (835, 817)

# size of the chess block
CHESS_BLOCK_IMAGE_SIZE = (70, 70)

# name of the 6 class classifier model to use
SIX_CLASS_MODEL_TO_USE = "xception"