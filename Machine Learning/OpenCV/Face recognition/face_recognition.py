import cv2 as cv
import numpy as np

haarcascade = cv.CascadeClassifier('haarcascade.xml')

people = ['Beyonce', 'Rihanna', 'Cooper'] #lables of the images


features = np.load('features.npy', allow_pickle=True)
labels = np.load('labels.npy', allow_pickle= True)

face_recognizer = cv.face.LBPHFaceRecognizer_create()
face_recognizer.read('face_trained.yml') #this reads the trained models
cap = cv.VideoCapture(0) #upload image of your choice

if not cap.isOpened():
    raise IOError("Cannot open webcam")

while True:
    ret, frame = cap.read()
    frame = cv.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv.INTER_AREA)
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)  # This turns images to grayscale
    haar_cascade = cv.CascadeClassifier('haarcascade.xml')
    face_rect = haar_cascade.detectMultiScale(gray, scaleFactor=1.2,
                                              minNeighbors=3)  # places a rectangle over the face detected

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    rect = haarcascade.detectMultiScale(gray, 1.1, minNeighbors=4)
    for (x, y, w, h) in rect:
        faces = gray[y:y + h, x:x + h]
        label, confidence = face_recognizer.predict(faces)
        print(
            f'Label = {people[label]}of confidence{confidence}')  # This prints out the label and the accuracy to which the model predicted the data presented
        cv.putText(gray, str(people[label]), (20, 20), cv.FONT_HERSHEY_COMPLEX, 1.0, (0, 255, 0),
                   thickness=2)  # allows printing of label onto the picture.
        cv.rectangle(gray, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)

        cv.imshow('Detected face', gray)

        #cv.imshow('Input', frame)
        c = cv.waitKey(1)
        if c == 27:
            break
#detecting the face in the image

cap.release()
cv.destroyAllWindows()
cv.waitKey(0)