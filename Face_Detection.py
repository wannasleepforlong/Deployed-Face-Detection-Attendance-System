import cv2
import face_recognition
import pickle
import numpy as np
import os
import csv
import datetime
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="sh221b777",
    password="12345",
    database="attendance"
)

cursor = conn.cursor()
img=r'C:\Users\HP\Desktop\Programming\Python\Face Detection Attendance\gui.png'

window_position = (100, 100)

cv2.namedWindow('Webcam', cv2.WINDOW_NORMAL)

cv2.moveWindow('Webcam', window_position[0], window_position[1])

cap = cv2.VideoCapture(0)

file = open("Encoding.p", "rb")
encodingwithid = pickle.load(file)
file.close()

def write_attendance_to_csv(student_id):
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    attendance_data = [current_date, student_id, "P"]

    with open("attendance.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(attendance_data)
    
def write_attendance_to_database(student_id):
    date = str(datetime.datetime.now().strftime("%Y-%m-%d"))
    attendance = "P"
    name = student_id
    insert_query = "INSERT INTO attendance (EventDate, Name, Attendance) VALUES (%s, %s, %s)"
    new_row = (date, name, attendance)
    cursor.execute(insert_query, new_row)
    conn.commit()
    print("New row added successfully.")


def is_already_detected(student_id):
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    with open("attendance.csv", mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == current_date and row[1] == student_id:
                return True

    return False



threshold = 0.5
while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodingwithid[0], encodeFace)
        facedistance = face_recognition.face_distance(encodingwithid[0], encodeFace)
        matchIndex = np.argmin(facedistance)

        if facedistance[matchIndex] <= threshold:
            if matches[matchIndex]:
                name = encodingwithid[1][matchIndex]
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

                # Check if face is already detected for the day
                if not is_already_detected(name):
                    write_attendance_to_csv(name)
                    write_attendance_to_database(name)
        else:
            name = 'Unknown'
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 2)
            

    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cursor.close()
conn.close()
cap.release()
cv2.destroyAllWindows()
