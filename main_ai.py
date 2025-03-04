import cv2
import numpy as np
import os.path
import time
import multiprocessing
from multiprocessing.pool import ThreadPool

from ai.frame_process import frameProcess
from com_read import readData
from com_protocol import protocolCheck

#Face recognition code is not written here but there is a function for it in AI directory
if __name__=="__main__":
    file_path = "file-path"
    config_path = "models/yolov4-tiny.cfg"
    weights_path = "models/yolov4-tiny.weights"
    log_file = "log.pkl"

    net = cv2.dnn.readNetFromDarknet(os.path.join(file_path, config_path), os.path.join(file_path, weights_path))
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    layers = net.getLayerNames()
    outputLayers = [layers[i-1] for i in net.getUnconnectedOutLayers()]
    
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)
    
    resolution = (320, 320)
    num_frames = 0
    start_time = time.time()

    human_queue = multiprocessing.Queue()
    color_queue = multiprocessing.Queue()
    
    log_path = os.path.join(file_path, log_file)
    
    '''while True:
        if readData(log_path) != None and protocolCheck(readData(log_path)) == 1:
            break'''
    
    while True:
        '''if protocolCheck(readData(log_path)) == 3:
            print(readData(log_path))
            break'''
        
        _, frame = cap.read()
        frame = cv2.resize(frame, resolution)
        
        #frame = cv2.flip(frame, -1)
        
        frameProcess(frame, net, outputLayers, os.path.join(file_path, database_path), human_queue, color_queue, num_frames)
        
        cv2.imshow('frame', frame)
        num_frames += 1
        
        elapsed_time = time.time() - start_time
        fps = num_frames / elapsed_time
        print(fps)

        if cv2.waitKey(30) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    
    
