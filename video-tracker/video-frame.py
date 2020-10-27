from utils import *

DATA = 'C:/Users/wb519128/Dropbox/Work/WB/CV/Ethiopia/data/'

#------------------------------------------------------------------------------
# Load video

# Load vidoe capture object
cap = cv2.VideoCapture(DATA + 'full.mp4')

# stable_show_vid(cap)

# Select an arbitrary frame
cap.set(cv2.CAP_PROP_POS_FRAMES, 50)
_, img_i = cap.read()

# Show frame
stable_show(img_i)

# Save frame
cv2.imwrite(DATA + 'sample-frame.jpg', img_i) 
