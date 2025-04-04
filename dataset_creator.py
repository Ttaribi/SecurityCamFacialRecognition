import sqlite3
#our sql db which will hold out data such as names with faces, facial enc as vectors

import numpy as np
#helps represent our image data as arrays, also handles datasets for facial encodings

import cv2
#CV2 is used for our facial rec. Capturing webcam vid, detecting face w/ Haar cascades, etc

import time

# ✅ Step 1: Make sure the STUDENTS table exists
conn = sqlite3.connect("sqlite.db")
conn.execute('''
    CREATE TABLE IF NOT EXISTS STUDENTS (
        Id INTEGER PRIMARY KEY,
        Name TEXT,
        age INTEGER
    );
''')
conn.commit()
conn.close()

faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml') #This will help us detect the faces
cam=cv2.VideoCapture(0) #0 indicates using the web camera
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


def insertOrUpdate(Id, Name, age): #This will send data to sqldb
    conn=sqlite3.connect("sqlite.db") #Connecting db
    cmd = "SELECT * FROM STUDENTS WHERE Id=" + str(Id) #This will give us all the user's detail when the id is entered
    cursor = conn.execute(cmd) #Cursor will execute our statement
    isRecordExist = 0. #assume no record exist in out table
    for row in cursor:
        isRecordExist = 1 #This checks each line if a record exist in our student table.
    if isRecordExist == 1: #If the record is in table, we update the name
        conn.execute("UPDATE STUDENTS SET NAME=? WHERE Id=?", (Name, Id))
        conn.execute("UPDATE STUDENTS SET age=? WHERE Id=?", (age, Id))
    else: #If no record, we insert a student
        conn.execute("INSERT INTO STUDENTS (Id,Name,age) values(?,?,?)", (Id,Name,age))

    conn.commit()
    conn.close()
#Out user defined values for our table
Id=input("Enter User Id: ")
Name=input("Enter User Name: ")
age=input("Enter Age: ")

insertOrUpdate(Id,Name,age)

#This will detect our face in web camera
sampleNum=0 #Amount of our datasets

#Code logic for allowing detector to capture as it goes
# while(True):
#     ret, img = cam.read() #This line opens camera
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #We the faces we see in the web cam into Gray Scale for accuracy (BGRGRAY)
#     faces = faceDetect.detectMultiScale(gray, 1.3, 5)
#     for(x,y,w,h) in faces:
#         sampleNum += 1 #If face is detected, we increment the sample number
#         cv2.imwrite("dataset/user."+str(Id)+"."+str(sampleNum) + ".jpg", gray[y:y+h,x:x+w]) #if face is detected, we save the face in out dataset file. (The color also)
#         cv2.rectangle(img,(x, y),(x + w, y + h),(0,255,0) ,2) #Once we detecte a face, we put a rectangle on it
#         cv2.waitKey(100) #We will show faces detected for 100 secs
#     cv2.imshow("Face", img) #show face detected in cam
#     cv2.waitKey(1) #delay time
#     if sampleNum > 20: #If our dataset is more than 20, we break
#         break


#Logic for taking planned pictures for model

totalSamples = 20                 #total number of images to capture
capture_interval = 2             #seconds between photos
last_capture_time = time.time()  #initialize the timerr

while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray, 1.2, 6)

    countdown = capture_interval - (time.time() - last_capture_time)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        #show countdown on the screen
        if countdown > 0:
            cv2.putText(img, f"Capturing in {int(countdown) + 1}...", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

        #capture photo after th countdown
        if countdown <= 0:
            sampleNum += 1
            last_capture_time = time.time()  #resets timer
            face_img = gray[y:y + h, x:x + w]
            filename = f"dataset/user.{Id}.{sampleNum}.jpg"
            cv2.imwrite(filename, face_img)
            print(f"✅ Saved {filename}")
            time.sleep(0.5)  #pause after capture to avoid duplicates

    cv2.imshow("Face", img)
    if cv2.waitKey(1) == ord('q') or sampleNum >= totalSamples:
        break
cam.release()
cv2.destroyAllWindows() #This quits program





