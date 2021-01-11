# TO DO:
#   Ta muito lenta essa porra. Acho que é essa merda desse loop. 
#       - Usar tensors?
#       - Apply?
#       - Dar uma limpada nas coisas que não precisão acontecer em cada frame

import cv2
import numpy as np
import os


class detector:
    """
    This class contains a object detector for static images or video frames
    """
    def __init__(self, model_path, model_name = "yolov3"):
        """
        Params:
        model_name - A srt containing the filenames of .weights and .cfg files
        model_path - a file path to directory containing [model_name].weights and [model_name].cfg files
        """
        # Load pre-trained model 
        weights = os.path.join(model_path, model_name + '.weights')
        config = os.path.join(model_path , model_name + '.cfg')
        self.net = cv2.dnn.readNet(model = weights, config = config)
        
        # Select output layers to get dections
        layer_names = self.net.getLayerNames()
        self.outputLayers = [layer_names[i[0]- 1] for i in self.net.getUnconnectedOutLayers()]
        
        # For now hardcoded list of classes o based on the ones in coco.names (SAME ORDER!)
        self.classes  = ['person',
                        'bicycle',
                        'car',
                        'motorbike',
                        'bus',
                        'train',
                        'truck',
                        'traffic light',
                        'stop sign']
        
        # Set random colors for each class. This is mostly for visualization
        # self.class_colors = np.random.uniform(0,255, size = (len(self.classes), 3))
    #------------------------------------------------------------------------------
    # Pass image into net and output detections
    def detect(self, img, threshold = .4):
        """
        Params:
        img - an image of type numpy.ndarray
        threshold - a float in [0,1) to set the minimum confidence for a detection not to be discarted 
        """
        
        # Image dimentions
        height, width, channels = img.shape
        
        # Turn image into blob. Basically sliptting image into 3 channels,
        # red, blue and green
        blob = cv2.dnn.blobFromImage(img, 
                                    scalefactor = 0.00392, 
                                    size = (416,416),
                                    mean = (0,0,0),
                                    swapRB = True,
                                    crop = False)
        self.net.setInput(blob)
        outs = self.net.forward(self.outputLayers)
        # Process information outputed by net
        class_ids = []
        confidences = []
        centroids = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                # Select only detections above certain confidence
                if confidence > threshold:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    # Detection box
                    x = int(center_x - w /2)
                    y = int(center_y - h /2)
                    # cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
                    # Add detections to lists
                    boxes.append([x,y,w,h])
                    centroids.append([center_x, center_y])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
        # Remove duplicated detections
        indexes = cv2.dnn.NMSBoxes(bboxes = boxes, 
                                   scores = confidences, 
                                   score_threshold = 0.5, 
                                   nms_threshold = 0.4)
        
        # Filterin bolean
        bol = np.in1d(np.array(range(len(boxes))), indexes)
        
        boxes_filtered = np.array(boxes)[bol]
        confidences_filtered = np.array(confidences)[bol]
        class_ids_filtered = np.array(class_ids)[bol]
        centroids_filtered = np.array(centroids)[bol]
                        
        return(boxes_filtered, 
               centroids_filtered,
               confidences_filtered, 
               class_ids_filtered)

