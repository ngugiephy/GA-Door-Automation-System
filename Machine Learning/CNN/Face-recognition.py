import tensorflow as tf
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
import numpy as np
from mtcnn.mtcnn import MTCNN
import PIL
from sklearn.preprocessing import LabelEncoder
import sklearn
import cv2 as cv
from pathlib import Path

base_directory = Path(__file__).resolve().parent
#This function extracts features of faces of images
def extract_face(filename, image_pixels = None, image_size=(160,160)):
  if filename is not None:
    image = PIL.Image.open(filename)
    detector = MTCNN()
    image = image.convert('RGB')
    pixels = np.asarray(image)
  elif image_pixels is not None:
    pixels = image_pixels
  results = detector.detect_faces(pixels)
  x1, y1, w, h = results[0]['box']
  x1, y1 = abs(x1), abs(y1)
  x2, y2 = (x1+w), (y1+h)
  face = pixels[y1:y2, x1:x2]
  box = (x1, y1, w, h)
  image = PIL.Image.fromarray(face)
  image = image.resize(image_size)
  image_array = np.asarray(image)
  return image_array


#loading in the facenet model:
model = load_model(base_directory / 'facenet_keras.h5', compile= 'True')
print('Loaded model')


def get_embedding(model, face_pixels):
  face_pixels = face_pixels.astype('float32')
  mean, std = face_pixels.mean(), face_pixels.std()
  face_pixels = (face_pixels - mean)/std
  samples = np.expand_dims(face_pixels, axis=0)
  predictions = model.predict(samples)
  return predictions[0]


#classification of faces
embed_data = np.load(base_directory / 'Face embeddings.npz')
trainX, trainy, valX, valy = embed_data['arr_0'], embed_data['arr_1'], embed_data['arr_2'], embed_data['arr_3']

out_encoder = LabelEncoder()
out_encoder.fit(trainy)
trainy = out_encoder.transform(trainy)
valy = out_encoder.transform(valy)

import pickle

filename = base_directory / 'SVM saved.sav'

model2 = pickle.load(open(filename, 'rb'))

def face_recognize(image):
    faces = extract_face(image, image_pixels=image)
    X = np.asarray(faces)
    # Get the Face Embeddings for the extracted face pixels and store as numpy array
    embedding = get_embedding(model, X)
    X = []
    X.append(embedding)
    X = np.asarray(X)
    ## Predict label for the face by using the pretrained models
    prediction = model2.predict(X)
    prob = model2.predict_proba(X)
    accuracy = prob[0,prediction] * 100
    predicted_label = out_encoder.inverse_transform([prediction])
    title = ('%s (%.3f)' % (predicted_label[0], accuracy))
    plt.imshow(faces)
    plt.title(title, color = 'green')
    
    return plt.show()

cap = cv.VideoCapture(0)
while True:
    ret, frame = cap.read()
    frame = cv.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv.INTER_AREA)
    face_recognize(frame)