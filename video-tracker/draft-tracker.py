
# https://www.youtube.com/watch?v=1FJWXOO1SRI


# TO DO:
#   - Change color per class
#   - Stop tracking if objects leave the frame? Change tracking algorithm most likely.
#   - Add new detections every frame to detect objects entering the frame
#   - Filter to only track objects detected in 4 frames
#   - Homography
#   - Find crossing trajectories.

# Settings
from utils import *
from sort import *

from detection import *

EXPORT = False


video_file_name = '2-sample-simp'
vidoe_file_extention = "mp4"

FOLDER = 'C:/Users/wb519128/Dropbox/Work/WB/CV/'
DATA = FOLDER + 'Ethiopia/data/prototype/'
NET = FOLDER + 'yolo/yolo-coco/'

# Load video
cap = cv2.VideoCapture(DATA + video_file_name + '.' + vidoe_file_extention)

#------------------------------------------------------------------------------
# Create frame detector instance

detector = detector(NET)

#------------------------------------------------------------------------------
# Initial detections

# Select first frame to start tracking 
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
_, img_0 = cap.read()
# stable_show(img_0)

if EXPORT:
    # Export initial frame for reference
    cv2.imwrite(DATA + video_file_name + 'img_0.jpg' , img_0)



# Detect objects in the first frame
bboxes_0, centriods, confidence, classes = detector.detect(img_0)


#------------------------------------------------------------------------------
# Set trackers

# Create MultiTracker instance
multiTracker = cv2.MultiTracker_create()

# Initialize MultiTracker with the detections in the first frame.
for bbox in bboxes_0:
    # print(tuple(bbox))
    multiTracker.add(newTracker = cv2.TrackerCSRT_create(), image = img_0, boundingBox = tuple(bbox))

#------------------------------------------------------------------------------
# Functions

def create_centroids(bbox):
    """ Turns am array of bounding boxes into one of centroids
    
     - bbox must be a numpy.array (n, 4), being n the number of bounding boxes in the array
     - It returns a (n,1,2) array. The first dimention is the number of centroids, the second
     is the 1 because it only contains 1 centriod per tracked object; and the 3rd are the X and
     Y coordinates of the centroid
    """
    
    # Get dimentions and location of bounding box
    x, y, w, h = bbox[:,0:1], bbox[:,1:2], bbox[:,2:3], bbox[:,3:4]
    
    # Calculare centroid
    center_x = x + w/2
    center_y = y + h/2
    
    # Returns a (n,1,2) array of centroids
    return np.dstack([center_x, center_y]).astype(int)

# Set bbox video anotation function
def drawBox(img, bbox):
    # Change bbox tuple to variables. X and Y of the initial position!
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,255), 3, 1)

# Set bbox video anotation function
def drawCentroid(img, centroid, class_id = 0):
    # Set class color
    if class_id == 0:
        color = (255,0,255)
    elif class_id == 2:
        color = (0,255,0)
    else:
        color = (0,0,0)
        
    # Get centroid coordinates
    center_x = centroid[0]
    center_y = centroid[1]
    
    # Draw on image
    cv2.circle(img, (center_x, center_y), 1, color, 2)

# # draw tracked objects
# for i, newbox in enumerate(bboxes):
#     drawBox(img_0, newbox)


#------------------------------------------------------------------------------
# Process video frame by frame

# Frame 0 centriods
ct_0 = create_centroids(bboxes_0)

# Initialize arrays to be updated
ct_tracked = ct_0

# Video loop
while True:
    
    # timer for frames per section
    timer = cv2.getTickCount()
    
    # Read each frame
    success, img_i = cap.read()
    
    # Add fps to display
    fps = cv2.getTickFrequency()/(cv2.getTickCount()-timer)
    cv2.putText(img_i,
                str(int(fps)),
                (50,50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255),2)
    
    # Update tracker frame by frame
    tracking_bol, bboxes_i = multiTracker.update(img_i)
    
    # Add tracked centroids to array
    ct_i = create_centroids(bboxes_i)
    ct_tracked = np.concatenate([ct_tracked,ct_i], axis = 1)
    
    # draw tracked objects bbox
    for i, new_ct in enumerate(ct_i):
        drawCentroid(img_i, 
                     new_ct[0],# new_ct has an extra dimention for the concatenation to work
                     class_id= classes[i]) 
    
    # Show video
    cv2.imshow("Video", img_i)
    # Break out by pressing 'q' when window is selected
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Make sure there are no open graphics devices
cv2.destroyAllWindows()



# Plot trajectories
draw_trajectories(img_0, ct_tracked)
stable_show(img_0)