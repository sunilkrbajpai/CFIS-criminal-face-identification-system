import cv2,os
import numpy as np
from PIL import Image

recognizer = cv2.face.LBPHFaceRecognizer_create()
path="dataSet"

def getImgID(path):
    #get the path of all the files in the folder
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
    #create empth face list
    faces=[]
    #create empty ID list
    Ids=[]
    #now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        #loading the image and converting it to gray scale
        faceImage=Image.open(imagePath).convert('L')
        #Now we are converting the PIL image into numpy array
        faceNp=np.array(faceImage,'uint8')
        #getting the Id from the image
        Id=int(os.path.split(imagePath)[-1].split(".")[1])
        faces.append(faceNp)
        Ids.append(Id)
        #cv2.imshow("training",faceNp)
        #cv2.waitKey(10)
        # extract the face from the training image sample
        #faces=detector.detectMultiScale(imageNp)
         #If a face is there then append that in the list as well as Id of it
    return Ids,faces

    
Ids,faces = getImgID(path)
#print(Ids,faces)
recognizer.train(faces, np.array(Ids))
recognizer.write('recognizer\\training_data.yml')
cv2.destroyAllWindows()
