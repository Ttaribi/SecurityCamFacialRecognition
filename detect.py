import cv2
import numpy as np
import os #For reading and writing file
import sqlite3
from datetime import datetime

recognized_id = None
frame_stability = 0
stable_threshold = 5

recognized_log = []  #keeps track of who was seen
max_log_entries = 5  #show last  5 logs on screen


facedetect=cv2.CascadeClassifier("haarcascade_frontalface_default.xml") #Will hrelp us detect our face
cam=cv2.VideoCapture(0) #Will open our web cam

recognizer=cv2.face.LBPHFaceRecognizer_create()
recognizer.read("recognizer/trainingdata.yml") #From our dataset

def getProfile(id):
    conn = sqlite3.connect("sqlite.db") #Connects to our db
    cursor = conn.execute("SELECT * FROM STUDENTS WHERE id=?", (id,))
    profile = None
    for row in cursor:
        profile = row
    conn.close()
    return profile #If profile was created we'll return it


logged_recently = set()     #to track recent recognitions
clear_after = 100           #how often to clear duplicates in frames (100 frames is about 3 - 4 secs)
frame_counter = 0           #to track how many frames passed

while(True):
    ret,img = cam.read()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #Converts our imgs into grey
    faces = facedetect.detectMultiScale(gray, 1.2, 6)
    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x + w,y + h), (0, 255, 0), 2)
        id, conf = recognizer.predict(gray[y:y + h, x:x + w])

        #sets a confidence threshold lower value = more confident match
        threshold = 70  #tweaking this  does (lower = stricter)

        id, conf = recognizer.predict(gray[y:y + h, x:x + w])
        if conf < threshold:
            if recognized_id == id:
                frame_stability += 1
            else:
                recognized_id = id
                frame_stability = 0

            if frame_stability >= stable_threshold:
                profile = getProfile(id)
                if profile:
                    cv2.putText(img, "Name: " + str(profile[1]), (x, y + h + 25), cv2.FONT_HERSHEY_COMPLEX, .8,
                                (0, 255, 127), 2)
                    cv2.putText(img, "Age: " + str(profile[2]), (x, y + h + 45), cv2.FONT_HERSHEY_COMPLEX, .8,
                                (0, 255, 127), 2)

                    #Llogs recognized person
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    entry = (profile[1], timestamp)

                    if profile[1] not in logged_recently:
                        recognized_log.append(entry)
                        logged_recently.add(profile[1])


        else:
            recognized_id = None
            frame_stability = 0
            cv2.putText(img, "Unknown", (x, y + h + 25), cv2.FONT_HERSHEY_COMPLEX, .8, (0, 0, 255), 2)

            #logs unknown person
            cv2.putText(img, "Unknown", (x, y + h + 25), cv2.FONT_HERSHEY_COMPLEX, .8, (0, 0, 255), 2)
            timestamp = datetime.now().strftime("%H:%M:%S")
            entry = ("Unknown", timestamp)

            if "Unknown" not in logged_recently:
                recognized_log.append(entry)
                logged_recently.add("Unknown")

    #draws the recognition log
    y_offset = 30
    cv2.rectangle(img, (5, 5), (270, 5 + max_log_entries * 30 + 20), (50, 50, 50), -1)  # background panel
    cv2.putText(img, "Recognized Log", (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    for i, (label, time_str) in enumerate(recognized_log):
        color = (255, 255, 255) if label != "Unknown" else (0, 0, 255)
        cv2.putText(img, f"{label} @ {time_str}", (15, 60 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    frame_counter += 1
    if frame_counter >= clear_after:
        logged_recently.clear()
        frame_counter = 0


    cv2.imshow("Face", img)  #show the image after drawing everything


    if (cv2.waitKey(1) == ord('q')):
        break
cam.release()
cv2.destroyAllWindows()



