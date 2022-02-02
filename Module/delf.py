# Import Libraries
from absl import logging
from PIL import Image, ImageOps
from scipy.spatial import cKDTree
from skimage.measure import ransac
from skimage.transform import AffineTransform
from six import BytesIO
from six.moves.urllib.request import urlopen

import tensorflow as tf
import tensorflow_hub as hub
import cv2 as cv
import numpy as np 
import pandas as pd
import cv2 as cv 
import os

delf = hub.load('https://tfhub.dev/google/delf/1').signatures['default']

def run_delf(image):
  np_image = np.array(image)
  float_image = tf.image.convert_image_dtype(np_image, tf.float32)

  return delf(
      image=float_image,
      score_threshold=tf.constant(100.0),
      image_scales=tf.constant([0.25, 0.3536, 0.5, 0.7071, 1.0, 1.4142, 2.0]),
      max_feature_num=tf.constant(1000))

def feature_extraction(image, new_width = 256, new_height = 256):
    image = cv.resize(image, (new_width, new_height))
    result = run_delf(image)
    return result['locations'], result['descriptors']


def match_images(result1, result2 ):
  distance_threshold = 0.8

  # Read features.
  num_features_1 = result1['locations'].shape[0]
  num_features_2 = result2['locations'].shape[0]
  
  # Find nearest-neighbor matches using a KD tree.
  d1_tree = cKDTree(result1['descriptors'])
  _, indices = d1_tree.query(
      result2['descriptors'],
      distance_upper_bound=distance_threshold)

  # Select feature locations for putative matches.
  locations_2_to_use = np.array([
      result2['locations'][i,]
      for i in range(num_features_2)
      if indices[i] != num_features_1
  ])
  locations_1_to_use = np.array([
      result1['locations'][indices[i],]
      for i in range(num_features_2)
      if indices[i] != num_features_1
  ])

  # Perform geometric verification using RANSAC.
  try:
    _, inliers = ransac((locations_1_to_use, locations_2_to_use),
                        AffineTransform, min_samples=3, residual_threshold=20, max_trials=100)
    inliers = sum(inliers)
  except: 
    inliers = 0

  return inliers