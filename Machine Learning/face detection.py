import cv2 as cv

img = cv.imread('faces.jpg') # use image of choice
cv.imshow('face', img)

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) #This turns images to grayscale
cv.imshow('gray', gray)

blur = cv.GaussianBlur(gray, (3,3), cv.BORDER_DEFAULT) # This blurs the image

canny = cv.Canny(blur, 125, 140)
haar_cascade = cv.CascadeClassifier('haarcascade.xml')
face_rect = haar_cascade.detectMultiScale(gray, scaleFactor= 1.2, minNeighbors=3) #places a rectangle over the face detected

print(f'Number of faces*{len(face_rect)}')

for(x,y,w,h) in face_rect:
    cv.rectangle(gray, (x,y), (x+w, y+h), (0,255,0), thickness=1)

cv.imshow('Detected faces', gray)

cv.waitKey(0)