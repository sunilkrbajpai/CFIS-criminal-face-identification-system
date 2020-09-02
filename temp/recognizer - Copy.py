import numpy as np
import sqlite3
import cv2


cascadePath = "haarcascade_frontalface_default.xml"
faceDetect = cv2.CascadeClassifier(cascadePath)
cam = cv2.VideoCapture(0)
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("recognizer\\training_data.yml")
Id=0
def getProfile(id):
    conn=sqlite3.connect("criminal.db")
    cmd="Select * from people where ID="+str(id)
    cursor=conn.execute(cmd)
    profile=None
    for row in cursor:
        profile=row
        break
    
    conn.close()
    return profile

font = cv2.FONT_HERSHEY_SIMPLEX
while True:
    ret, im =cam.read()
    gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    faces=faceDetect.detectMultiScale(gray, 1.2,5)
    for(x,y,w,h) in faces:
        cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
        Id, conf = recognizer.predict(gray[y:y+h,x:x+w])
        profile=getProfile(Id)
        if(profile!=None):
            ###################################################
            cv2.putText(im,"Name: "+str(profile[1]), (x,y+h),font,1,(255,0,255),3)
            cv2.putText(im,"Gender: "+str(profile[2]), (x,y+h+30),font,1,(0,255,0),3)
            cv2.putText(im,"Crime: "+str(profile[9]), (x,y+h+60),font,1,(0,0,255),3)


        cv2.imshow('CFIS',im)
    if (cv2.waitKey(1)==ord('q')):
        break
cam.release()
cv2.destroyAllWindows()
