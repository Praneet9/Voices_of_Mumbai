import os
import cv2
import numpy as np
from .preprocessing import parse_annotation
from .utils import draw_boxes
from .frontend import YOLO
import json
import tensorflow as tf

os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]="0"

global detection_graph, detection_sess

config_path  = 'potholes/config.json'
weights_path = 'potholes/weights/trained_wts.h5'

with open(config_path) as config_buffer:    
    config = json.load(config_buffer)

detection_graph = tf.Graph()
detection_sess = tf.Session(graph = detection_graph)

with detection_graph.as_default():
    with detection_sess.as_default():
        ###############################
        #   Make the model 
        ###############################

        yolo = YOLO(backend = config['model']['backend'],
                    input_size = config['model']['input_size'], 
                    labels = config['model']['labels'], 
                    max_box_per_image = config['model']['max_box_per_image'],
                    anchors = config['model']['anchors'])

        ###############################
        #   Load trained weights
        ###############################    
        print("Loaded")
        yolo.load_weights(weights_path)

def predict_potholes(image_path):

    ###############################
    #   Predict bounding boxes 
    ###############################

    image = cv2.imread(image_path)
    # print(image)

    with detection_graph.as_default():
        with detection_sess.as_default():
            boxes = yolo.predict(image)
    # print(boxes)
    image, pothole_coords = draw_boxes(image, boxes, config['model']['labels'])

    no_boxes = len(boxes)

    return image, no_boxes, pothole_coords

