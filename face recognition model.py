import cv2 as cv
import os
import numpy as np

people = ['Beyonce', 'Rihanna', 'Cooper'] #lables of the images
data = r'/home/barbra/Downloads/Train' # path to access the image folders
features =[]
labels = []
haarcascade = cv.CascadeClassifier('haarcascade.xml')
def create_train():
    for person in people:
        path = os.path.join(data, person)
        label = people.index(person)

        for img in os.listdir(path): #grabs the image path
            img_path = os.path.join(path, img)
            img_array = cv.imread(img_path)
            gray = cv.cvtColor(img_array, cv.COLOR_BGR2GRAY)

            rect = haarcascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

            for(x,y,w,h) in rect:
                faces = gray[y:y+h, x:x+w]
                features.append(faces)
                labels.append(label)
                # for each photo presented, the face when recognized is stored as a feature and the label is given to it as to what the machine model may perceive it is.
                # There is need pf converiting data into numbers for ease in translation

create_train()

#this comfirms number of features and labels in the data used
print(f'Length of features = {len(features)}')
print(f'Length of labels = {len(labels)}')

#training the model:
features = np.array(features, dtype='object')
labels = np.array(labels)

face_recognizer = cv.face.LBPHFaceRecognizer_create()
face_recognizer.train(features, labels)

face_recognizer.save('face_trained.yml') #this saves the trained models

np.save('features.npy', features)
np.save('labels.npy', labels)





