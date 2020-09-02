#copy a folder images containing images of person names in small letters
import face_recognition as fr
import cv2
import numpy as np
import os

def load_images_from_folder(folder):
    images=[]
    for filename in os.listdir(folder):
        images.append(filename)
    return images
video_capture=cv2.VideoCapture(0)
images=load_images_from_folder("images")
#print(images)

images_name=[]
for img in images:
    images_name.append(fr.load_image_file(os.path.join("images",img)))
encodings=[]
for img in images_name:
    encodings.append(fr.face_encodings(img)[0])
#Create array of known face encoding and their names
known_face_encodings=[]
for encode in encodings:
    known_face_encodings.append(encode)
known_face_names=[]
for name in images:
    known_face_names.append(os.path.splitext(name)[0])
#initialize some variables*******************************************************************************************************************************************
face_locations=[]
face_encodings=[]
face_names=[]
process_this_frame=True
while True:
    #Grab a single frame of video
    ret,frame=video_capture.read()
    #Resize the frame of video to 1/4 size for fast process
    small_frame=cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
    #convert the image to BGR color(openCV) to RGB color(face_recognition)
    rgb_small_frame=small_frame[:,:,::-1]
    #Only process every other frame of video to save time
    if process_this_frame:
        #find all the faces and face encodings in the current frame of video
        face_locations=fr.face_locations(rgb_small_frame)
        face_encodings=fr.face_encodings(rgb_small_frame,face_locations)
        face_names=[]
        for face_encoding in face_encodings:
            #See if the face is a match for known face(s)
            matches=fr.compare_faces(known_face_encodings,face_encoding)
            name="Unknown"
            face_distances=fr.face_distance(known_face_encodings,face_encoding)
            best_match_index=np.argmin(face_distances)
            if matches[best_match_index]:
                name=known_face_names[best_match_index]
            face_names.append(name)
    process_this_frame=not process_this_frame
    #display the result
    for(top,right,bottom,left),name in zip(face_locations,face_names):
        top*=4
        right*=4
        bottom*=4
        left*=4
        cv2.rectangle(frame,(left,top),(right,bottom),(0,0,225),2)
        cv2.rectangle(frame,(left,bottom-35),(right,bottom),(0,0,225),cv2.FILLED)
        font=cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame,name,(left+6,bottom-6),font,1.0,(225,225,225),1)
    cv2.imshow('Video',frame)
    if cv2.waitKey(1) & 0XFF==ord('q'):
        break
video_capture.release()
cv2.destroyAllWindows()










            

            
            






            
            





    
    
    
    

