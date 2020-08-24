
#--------------------------------------------------------------------
# Settings

# conda activate cv

import tensorflow as tf
import tensornets as nets
import cv2
import cvlib as cv
import numpy as np
import matplotlib.pyplot as plt

import time
import os

# Set directory
os.chdir('C:/Users/wb519128/Desktop')

#--------------------------------------------------------------------
# Video

inputs = tf.placeholder(tf.float32, [None, 416, 416, 3]) 
model = nets.YOLOv3COCO(inputs, nets.Darknet19)

#to display other detected objects,change the classes and list of classes to their respective #
# COCO indices available in their website. Here 0th index is for #people and 1 for bicycle and so on. 
# If you want to detect all the #classes, add the indices to this list
classes = {'0':'person','1':'bicycle','2':'car','3':'bike','5':'bus','7':'truck'}
list_of_classes=[0,1,2,3,5,7]


with tf.Session() as sess:
    sess.run(model.pretrained())
    
    cap = cv2.VideoCapture("road_h2_s1_b.avi")
    #change the path to your directory or to '0' for webcam
    while(cap.isOpened()):
        ret, frame = cap.read()
        img=cv2.resize(frame,(416,416))
        imge=np.array(img).reshape(-1,416,416,3)
        start_time=time.time()
        preds = sess.run(model.preds, {inputs: model.preprocess(imge)})

#--------------------------------------------------------------------
# Image
im = cv2.imread('cars_4.png')

plt.imshow(im)
plt.show()



bbox, label, conf = cv.detect_common_objects(im)
output_image = draw_bbox(im, bbox, label, conf)
plt.imshow(output_image)
plt.show()
print('Number of cars in the image is '+ str(label.count('car')))