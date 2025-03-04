import cv2
import numpy as np
import os.path
import time
import multiprocessing
from multiprocessing.pool import ThreadPool

from ai.color_detection import colorProcess
from ai.human_detection import humanProcess
from ai.face_recog import faceProcess
from com_save import saveData

def humanProcessFunc(frame, net, outputLayers, human_queue):
    humans = humanProcess(frame, net, outputLayers)
    human_queue.put(humans)

def faceProcessFunc(frame, face_path, face_queue):
    faces = faceProcess(frame, face_path)
    face_queue.put(faces)

def colorProcessFunc(frame, color_queue):
    color = colorProcess(frame)
    color_queue.put(color)

def frameProcess(frame, net, outputLayers, face_path, human_queue, color_queue, counter):
    if counter <= 25 and False:
        faces = faceProcess(frame, face_path)
        if len(faces) > 0:
            saveData(faces, "face")
            print("face found.")
    else:
        human_process = multiprocessing.Process(target=humanProcessFunc, args=(frame, net, outputLayers, human_queue))
        human_process.start()

        color_process = multiprocessing.Process(target=colorProcessFunc, args=(frame, color_queue))
        color_process.start()

        humans = human_queue.get()
        if len(humans) > 0:
            saveData(humans, "human")
            for human in humans:
                cv2.rectangle(frame, (human[0], human[1]), (human[0] + human[2], human[1] + human[3]), (255, 0, 0), 2)
            print("human found.")
        human_process.join()

        colors = color_queue.get()
        if len(colors) > 0:
            saveData(colors, "color")
            for color in colors:
                cv2.rectangle(frame, (color[0], color[1]), (color[0] + color[2], color[1] + color[3]), (0, 255, 0), 2)
            print("color found.")
        color_process.join()
