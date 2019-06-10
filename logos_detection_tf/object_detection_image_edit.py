# This is modification of the code of Evan Juras at 
# https://github.com/EdjeElectronics/TensorFlow-Object-Detection-API-Tutorial-Train-Multiple-Objects-Windows-10/blob/master/Object_detection_image.py
# Where he sites using the following: 
# Google's example at
# https://github.com/tensorflow/models/blob/master/research/object_detection/object_detection_tutorial.ipynb
# Dat Tran's example at
# https://github.com/datitran/object_detector_app/blob/master/object_detection_app.py

# Edited to contain all the code within a single detection class for images 

import os
import cv2
import numpy as np
import tensorflow as tf
import sys

from utils import label_map_util
from utils import visualization_utils as vis_util

# TODO: Clean up the docstrings for various functions and the init for the ObjectDetectionImage class

# Variables related to the trained model; can be moved to command line arguments 
# Currently these are relative to the project structure 
sys.path.append("..")
# Name of the directory containing the object detection module we're using
MODEL_NAME = 'inference_graph'
# Path to frozen detection graph .pb file, which contains the trained model
CWD_PATH = os.getcwd()
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')
# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH,'training','labelmap.pbtxt')
# Number of classes 
NUM_CLASSES = 4


class ObjectDetectionImage():
    def __init__(self, path_to_model, path_to_labels, num_classes):
        self.label_map = label_map_util.load_labelmap(path_to_labels)
        self.categories = label_map_util.convert_label_map_to_categories(self.label_map, 
                            max_num_classes=num_classes, use_display_name=True)
        self.category_index = label_map_util.create_category_index(self.categories)
        self.load_model(path_to_model)

    def load_model(self, path_to_model):
        '''
        path_to_model: path to the frozen inference graph 
        load the model into memory 
        '''
        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(path_to_model, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
            self.sess = tf.Session(graph=self.detection_graph)
        #return self.detection_graph, self.sess # this return line may or may not be needed - try it out! 

    # Input tensor is the image
    def get_image_tensor(self):
        image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
        return image_tensor

    # Output tensors are the detection boxes, scores, and classes
    # Each box represents a part of the image where a particular object was detected
    def get_detection_boxes(self):
        detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
        return detection_boxes

    # Each score represents level of confidence for each of the objects.
    # The score is shown on the result image, together with the class label.
    def get_detection_scores(self):
        detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
        return detection_scores

    def get_detection_classes(self):
        detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
        return detection_classes

    # Number of objects detected
    def get_num_detections(self):
        num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')
        return num_detections

    def get_image(self, image_path):
        image = cv2.imread(image_path)
        return image
    
    # Perform the actual detection by running the model with the image as input
    # to do this need to expand image dimensions to have shape: [1, None, None, 3]
    # i.e. a single-column array, where each item in the column has the pixel RGB value
    # TODO: make a version of this that works with a list of images 
    def do_object_detection(self, image_path):
        (boxes, scores, classes, num) = self.sess.run(
            [self.get_detection_boxes(), self.get_detection_scores(), 
            self.get_detection_classes(), self.get_num_detections()],
            feed_dict={self.get_image_tensor(): np.expand_dims(self.get_image(image_path), axis=0)})
        return (boxes, scores, classes, num)

    def visualise_detection(self, image_path):
        image = self.get_image(image_path)
        (boxes, scores, classes, num) = self.do_object_detection(image_path)
        # Draw the results of the detection (aka 'visulaize the results')

        vis_util.visualize_boxes_and_labels_on_image_array(
            image,
            np.squeeze(boxes),
            np.squeeze(classes).astype(np.int32),
            np.squeeze(scores),
            self.category_index,
            use_normalized_coordinates=True,
            line_thickness=8,
            min_score_thresh=0.60)

        # All the results have been drawn on image. Now display the image.
        cv2.imshow('Object detector', image)

        # Press any key to close the image
        cv2.waitKey(0)

        # Clean up
        cv2.destroyAllWindows()


if __name__ == '__main__':
    object_detection = ObjectDetectionImage(PATH_TO_CKPT, PATH_TO_LABELS, NUM_CLASSES)
    # loop over the whole set of test images, visualising the predictions one by one 
    # note that you need to press any key on the image in order to close it and 
    # move on to the next image 
    for image in os.listdir('tests'):
        if image.endswith('.jpg'):
            image_path = os.path.join(CWD_PATH, 'tests', image)
            object_detection.visualise_detection(image_path)

    # alternatively run on a single image as below 
    #image_name = 'tests/train_2.jpg'
    #image_path = os.path.join(CWD_PATH, image_name)
    #object_detection.visualise_detection(image_path)