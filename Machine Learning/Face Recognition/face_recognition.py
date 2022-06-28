import cv2 as cv
import numpy as np

haarcascade = cv.CascadeClassifier('haarcascade.xml')

people = ['Beyonce', 'Rihanna', 'Cooper'] #lables of the images
#features = np.load('features.npy')
#labels = np.load('labels.npy')

face_recognizer = cv.face.LBPHFaceRecognizer_create()
face_recognizer.read('face_trained.yml') #this saves the trained models
img = cv.imread('jp1.jpg')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('unknown', gray)

#detecting the face in the image
rect = haarcascade.detectMultiScale(gray, 1.1, minNeighbors=4)
for (x,y,w,h) in rect:
    faces = gray[y:y+h, x:x+h]
    label, confidence = face_recognizer.predict(faces)
    print(f'Label = {people[label]}of confidence{confidence}')
    cv.putText(img, str (people[label]), (20,20), cv.FONT_HERSHEY_COMPLEX, 1.0, (0,255,0), thickness=2)
    cv.rectangle(img, (x,y), (x+w,y+h), (0,255,0), thickness = 2)

cv.imshow('Detected face', img)
cv.waitKey(0)
