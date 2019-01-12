inceptionV3configs = { "epochs": [100, 100], "batch_size": [64, 64], "lr": [0.00001, 0.0001], "model_weights_file_name": ["chess_pieces_inceptionv3_p1.hdf5", "chess_pieces_inceptionv3_p2.hdf5"], "model_weights_file_to_use": 1   }
customCNNconfigs = { "epochs": [150], "batch_size": [32], "lr": [0.0001], "model_weights_file_name": ["custom_cnn.hdf5"], "model_weights_file_to_use": 0   }
alexNetconfigs = { "epochs": [150], "batch_size": [8], "lr": [0.0001], "model_weights_file_name": ["alexnet.hdf5"], "model_weights_file_to_use": 0   }