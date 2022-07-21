import cv2 as cv

cap = cv.VideoCapture(2)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

while True:
    ret, frame = cap.read()
    frame = cv.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv.INTER_AREA)
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)  # This turns images to grayscale
    haar_cascade = cv.CascadeClassifier('haarcascade.xml')
    face_rect = haar_cascade.detectMultiScale(gray, scaleFactor=1.2,
                                              minNeighbors=3)  # places a rectangle over the face detected

    print(f'Number of faces*{len(face_rect)}')
    for (x, y, w, h) in face_rect:
        cv.rectangle(gray, (x, y), (x + w, y + h), (0, 255, 0), thickness=1)

    cv.imshow('Detected faces', gray)


    c = cv.waitKey(1)
    if c == 27:
     break


cap.release()
cv.destroyAllWindows()
cv.waitKey(0)