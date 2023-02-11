import os
import pickle
from tensorflow.keras.models import load_model

# Sequential Model PATH
CONV2D_CLASSIFIER = 'models/conv2d_classifier.h5'

# Transfer Learning Model PATH
VGG_CLASSIFIER = 'models/transfer_learning_models/vgg19_classifier.h5'
MOBNETV2_CLASSIFIER = 'models/transfer_learning_models/mobv2_classifier.h5'
RESNET50_CLASSIFIER = 'models/transfer_learning_models/resnet50_classifier.h5'
INCEPTIONV3_CLASSIFIER = 'models/transfer_learning_models/inceptionv3_classifier.h5'

# Hybrid Learning Model PATH

VGG19_FEATURES = 'models/hybrid_models/vgg19_features.h5'
# MODEL_PATH_CONV_FEATURES = 'models/conv_features.h5'
SVM_VGG = 'models/hybrid_models/svm_vgg19_2.sav'
RF_VGG = 'models/hybrid_models/rf_vgg19.sav'
VGG_CONV_DENSE = 'models/hybrid_models/vgg19_conv_dense.h5'

# Machine Learning Model PATH
SVM = "models/ml_models/svm.sav"
RF = "models/ml_models/rf.sav"
LR = "models/ml_models/log_reg.sav"
KNN = "models/ml_models/knn.sav"
NB = "models/ml_models/nb.sav"

def get_models(transfer_learning=True, machine_learning=True, sequential=True, hybrid=True):
    models = {}
    print("LOADING MODELS.....")
    models["transfer_learning"] = {
        "VGG19": load_model(VGG_CLASSIFIER),
        "ResNet50": load_model(RESNET50_CLASSIFIER),
        "InceptionV3": load_model(INCEPTIONV3_CLASSIFIER),
        "MobileNetV2": load_model(MOBNETV2_CLASSIFIER)
    }

    models["hybrid_models"] = {
        "VGG19_Features": load_model(VGG19_FEATURES),
        "RF": pickle.load(open(RF_VGG, "rb")),
        "SVM": pickle.load(open(SVM_VGG, "rb")),
        "VGG_CONV_DENSE": load_model(VGG_CONV_DENSE)
    }

    models["machine_learning"] = {
        "SVM" : pickle.load(open(SVM, "rb")),
        "RF" : pickle.load(open(RF, "rb")),
        "LR" : pickle.load(open(LR, "rb")),
        "KNN" : pickle.load(open(KNN, "rb")),
        "NB" : pickle.load(open(NB, "rb"))
    }

    models["sequential"] = {
        "CONV2D": load_model(CONV2D_CLASSIFIER)
    }
    return models

