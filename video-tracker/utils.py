import cv2
import numpy as np
import matplotlib.pyplot as plt
import os



# Functions
def stable_show(img, t = 5000):
    cv2.startWindowThread()
    cv2.namedWindow("preview")
    cv2.imshow('preview', img)
    cv2.waitKey(t)
    cv2.destroyAllWindows()

def stable_show_vid(cap):
    while True:
        sucess, img_i = cap.read()
        cv2.imshow("Video", img_i)
        # Break out by pressing 'q' when window is selected
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    # When everything done, release the capture
    # cap.release()
    cv2.destroyAllWindows() 

