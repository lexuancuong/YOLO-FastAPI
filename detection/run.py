import io
import os
from PIL import Image
import cv2
import numpy as np
from base64 import b64decode, b64encode
from .utils import *
from .darknet import Darknet
import cv2 
import matplotlib.pyplot as plt
import uuid 

try:
    #load model for coco format
    cfg_file = './detection/cfg/yolov3.cfg'
    weight_file = './detection/weights/yolov3.weights'
    namesfile = './detection/data/coco.names'
    m = Darknet(cfg_file)
    m.load_weights(weight_file)
    class_names = load_class_names(namesfile)
    #Load model for vn food
    cfg_file_vn = './detection/cfg/yolov3-5c-5000-max-steps.cfg'
    weight_file_vn = './detection/weights/yolov3-5c-5000-max-steps_last.weights'
    namesfile_vn = './detection/data/obj.names'
    m_vn = Darknet(cfg_file_vn)
    m_vn.load_weights(weight_file_vn)
    class_names_vn = load_class_names(namesfile_vn)
except:
    print('Path is Error!!!')

def inferenceYoLo(original_image):
    resized_image = cv2.resize(original_image, (m.width, m.height),interpolation=cv2.INTER_AREA)
    nms_thresh = 0.4
    iou_thresh = 0.6
    boxes = detect_objects(m, resized_image, iou_thresh, nms_thresh)
    url = plot_boxes(original_image, boxes, class_names, plot_labels = True)
    objects = print_objects(boxes, class_names)
    plt.imshow(original_image)
    name = os.path.join('./static/images',str(uuid.uuid1()) + '.png')
    im = plt.savefig(name)
    return name

def inferenceVNFood(original_image):
    resized_image= cv2.resize(original_image, (m_vn.width, m_vn.height),interpolation=cv2.INTER_AREA)
    nms_thresh = 0.4
    iou_thresh = 0.6
    boxes = detect_objects(m_vn, resized_image, iou_thresh, nms_thresh)
    url = plot_boxes(original_image, boxes, class_names_vn, plot_labels = True)
    objects = print_objects(boxes, class_names_vn)
    plt.imshow(original_image)
    name = os.path.join('./static/images', str(uuid.uuid1()) + '.png')
    im = plt.savefig(name)
    return name

