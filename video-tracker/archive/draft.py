#------------------------------------------------------------------------------
# Draft
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
# Settings
from utils import *

FOLDER = 'C:/Users/wb519128/Dropbox/Work/WB/CV/'
DATA = FOLDER + 'Ethiopia/data/'
NET = FOLDER + 'yolo/yolo-coco/'

#------------------------------------------------------------------------------
# Load image

img = cv2.imread(DATA + 'sample-frame.jpg')
height, width, channels = img.shape

#------------------------------------------------------------------------------
# Load YOLO pre-trained algorithm

weights = NET + 'yolov3.weights'
config = NET + 'yolov3.cfg'

net = cv2.dnn.readNet(model = weights, config = config)

# Set a list of classes of interest based on the ones in coco.names
classes  = ['person',
            'bicycle',
            'car',
            'motorbike',
            'bus',
            'train',
            'truck',
            'traffic light',
            'stop sign']

# random colors for each class
colors = np.random.uniform(0,255, size = (len(classes), 3))
# Select output layers to get dections
layer_names = net.getLayerNames()
outputLayers = [layer_names[i[0]- 1] for i in net.getUnconnectedOutLayers()]

#------------------------------------------------------------------------------
# Process image

# Turn image into blob. Basically sliptting image into 3 channels,
# red, blue and green
blob = cv2.dnn.blobFromImage(img, 
                             scalefactor = 0.00392, 
                             size = (416,416),
                             mean = (0,0,0),
                             swapRB = True,
                             crop = False)

#------------------------------------------------------------------------------
# Pass image into net

net.setInput(blob)
outs = net.forward(outputLayers)

# Process information outputed by net
class_ids = []
confidences = []
boxes = []
for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        # Select only detections above certain confidence
        if confidence > 0.5:
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)
            # Draw centroid circle in the image
            cv2.circle(img, (center_x, center_y), 2, (0, 255, 0), 1)
            # Draw detection box
            x = int(center_x - w /2)
            y = int(center_y - h /2)
            # cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
            # Add detections to lists
            boxes.append([x,y,w,h])
            confidences.append(float(confidence))
            class_ids.append(class_id)

# Score treshold, will not show boxes if not  in trashold
# indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
# print(indexes)

# Add labels
for i in range(len(boxes)):
    # if i in indexes:
    if True:
        x,y,w,h = boxes[i]
        label = str(classes[class_ids[i]])
        color = colors[i]
        cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
        cv2.putText(img, label, (x, y + 30), 
                    cv2.FONT_HERSHEY_PLAIN, 3, (0,0,0), 3)

stable_show(img)


#------------------------------------------------------------------------------
# DRAFT

# Blank array
# canvas = np.zeros((dim))
