import tensorflow as tf
from tensorflow import keras

import cv2 as cv
import numpy as np
import os

from numpy.linalg import norm
from numpy import dot

def load_model(path):
  model = keras.models.load_model(path + 'model_resnet.h5')
  return model

def retrieval_resnet(feature_query, feature_corpus, top = 10):
    #compute cosine distance
    cosine_dis = {}
    for img in feature_corpus:
        cosine_dis[img] = dot(feature_corpus[img].T, feature_query)/(norm(feature_corpus[img].T)*norm(feature_query))
        
    results = sorted(cosine_dis.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
    return results[:top]

def feature_extraction_resnet(model, img, new_width = 256, new_height = 256):
  img = np.array(cv.resize(img, (new_width, new_height)))
  return np.array(model.predict(img[None,:,:])).T