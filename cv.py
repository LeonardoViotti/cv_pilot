
# conda activate cv

import numpy as np
import cvlib as cv
import cv2
import os
import matplotlib.pyplot as plt


# Set directory
os.chdir('C:/Users/wb519128/Desktop')

# Load data
im = cv2.imread('cars_4.png')

plt.imshow(im)
plt.show()



bbox, label, conf = cv.detect_common_objects(im)
output_image = draw_bbox(im, bbox, label, conf)
plt.imshow(output_image)
plt.show()
print('Number of cars in the image is '+ str(label.count('car')))`