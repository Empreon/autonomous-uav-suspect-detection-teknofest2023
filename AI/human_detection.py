import cv2
import numpy as np

def nmsBoxes(boxes, scores, score_threshold=0.2, nms_threshold=0.5, max_boxes=10):
    # Non-Maximum Suppression (NMS)
    indices = cv2.dnn.NMSBoxes(boxes, scores, score_threshold, nms_threshold)
    indices = indices.flatten()[:max_boxes] if len(indices) > 0 else []
    return indices

def humanProcess(img, net, outputLayers, score_threshold=0.2, nms_threshold=0.5, max_boxes=10):
    blob = cv2.dnn.blobFromImage(img, scalefactor=1/255, size=(320,320), mean=(0,0,0), swapRB=True, crop=False)
    net.setInput(blob)
    layerOutputs = net.forward(outputLayers)

    confidences = []
    boxes = []

    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > score_threshold and classId == 0:
                center_x = int(detection[0] * img.shape[1])
                center_y = int(detection[1] * img.shape[0])
                width = int(detection[2] * img.shape[1])
                height = int(detection[3] * img.shape[0])
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])

    indices = nmsBoxes(boxes, confidences, score_threshold, nms_threshold, max_boxes)

    objects = []
    for i in indices:
        box = boxes[i]
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        confidence = confidences[i]
        objects.append([x, y, w, h, confidence])

    return objects
