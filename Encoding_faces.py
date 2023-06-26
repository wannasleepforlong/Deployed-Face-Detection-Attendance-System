import cv2
import face_recognition
import pickle
import numpy as np
import os
import csv
import datetime

# Importing student images
folderPath = r'C:\Users\HP\Desktop\Programming\Python\Face Detection Attendance\Faces'
pathList = os.listdir(folderPath)
print(pathList)
imgList = []
studentIds = []
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0])

def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

print("Encoding Started ...")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, studentIds]
print("Encoding Complete")

file = open("Encoding.p", 'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("File Saved")

