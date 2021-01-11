
#------------------------------------------------------------------------------
# Crop sample video
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
# Settings
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

DATA = 'C:/Users/wb519128/Dropbox/Work/WB/CV/Ethiopia/data/'

#------------------------------------------------------------------------------
# Load video

# Load vidoe capture object
cap = cv2.VideoCapture(DATA + 'full.mp4')


# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(DATA + 'output1.avi',fourcc = fourcc, fps = 29.9, frameSize = (720,480))


# Set number of frames to be saved
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
n_frames = 200

# Loop over frames and display vidoe
for fno in range(0, n_frames):
    # print(fno)
    cap.set(cv2.CAP_PROP_POS_FRAMES, fno)
    _, img_i = cap.read()
    
    # Save frames
    out.write(img_i)
    
    # Show video
    cv2.imshow("Video", img_i)
    # Break out by pressing 'q' when window is selected
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture and close window
cap.release()
cv2.destroyAllWindows()