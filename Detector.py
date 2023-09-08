import cv2
import numpy as np
import time

np.random.seed(20)
class Detector:
    def __init__(self, videoPath, configPath, modelPath, classesPath):
        self.videoPath = videoPath
        self.configPath = configPath
        self.modelPath = modelPath
        self.classesPath = classesPath

        ################ Model Setup ######################

        self.net = cv2.dnn_DetectionModel(self.modelPath, self.configPath)
        self.net.setInputSize(320, 320) #model was trained at size 320x320
        self.net.setInputScale(1.0/127.5)
        self.net.setInputMean(127.5)
        self.net.setInputSwapRB(True)

        self.readClasses()

    ############### READ CLASS LABEL LIST ##################
    def readClasses(self):
        with open(self.classesPath, 'r') as f:
            self.classesList = f.read().splitlines()
        
        self.classesList.insert(0, '__Background__') #added a new class at index 0

        #choosing random colour for different classes
        self.colorList = np.random.uniform(low=0, high=255, size=(len(self.classesList), 3)) 

        #print(self.classesList)

    
    def onVideo(self):
        cap = cv2.VideoCapture(self.videoPath)

        if (cap.isOpened()==False):
            print("Error opening file...")
            return
        
        (sucess, image) = cap.read() #here the video is read in form of images and each frame is named as image


        while sucess:
            classLabelIDs, confidences, bboxs = self.net.detect(image, confThreshold = 0.4)

            bboxs = list(bboxs)
            confidences = list(np.array(confidences).reshape(1, -1)[0])
            confidences = list(map(float, confidences))

            bboxIdx = cv2.dnn.NMSBoxes(bboxs, confidences, score_threshold = 0.5, nms_threshold=0.2)

            if len(bboxIdx) != 0: #non overlapping bounding boxes
                for i in range(0, len(bboxIdx)):

                    bbox = bboxs[np.squeeze(bboxIdx[i])]
                    classConfidence = confidences[np.squeeze(bboxIdx[i])]
                    classLabelID = np.squeeze(classLabelIDs[np.squeeze(bboxIdx[i])])
                    classLabel = self.classesList[classLabelID]
                    classColor = [int(c) for c in self.colorList[classLabelID]]

                    displayText = "{}:{:.2f}".format(classLabel, classConfidence)

                    x,y,w,h = bbox

                    cv2.rectangle(image, (x, y), (x+w, y+h), color=classColor, thickness=1)
                    cv2.putText(image, displayText, (x, y-10), cv2.FONT_HERSHEY_PLAIN, 1, classColor, 1)

                    #########################################

                    

            cv2.imshow("Result", image)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

            (sucess, image) = cap.read()

        cv2.destroyAllWindows()