# Face Detection and Face Recognition
### Requirements
* Python 3
* OpenCv
* Haarcascade model file.
* numpy


- Install OpenCV though [OpenCV](https://sourceforge.net/projects/opencvlibrary/). add it to the library of your code editor of choice.
- Install Python3 though [Python3](https://www.python.org/downloads/)
- pip install numpy
- For the Haarcascade file, from [haarcascade for face](https://github.com/opencv/opencv/blob/4.x/data/haarcascades/haarcascade_frontalface_default.xml) Copy the file when raw and create a new file in your folder and save as "haarcascade.xml" and paste the contents into the file. Save.
However I have made the one currently in use in the repository.

## Face Detection
The face detection code enables one to detect the faces and number of faces in a an image by placing a retangle over the face. This is done through OpenCV. It best works with gray  scale images.

### How to use Face detection
- Use image of choice and place its path in img for reading. To ease work, you can save the image in the same folder as your code and refer to it directly. Save your images as jpg.
- Changing the 'minNeighbors' value may affect the quality of your detection.

## Face recognition
This project detects an face in a photo and assigns it to it respective label as trained in the model. One needs to train the model first before using it to predict images. There is the trained model and the face recognition code itself.

### How to use Face Recognition
1. Train model with data of choice. 
- Create a folder of the data(peoples faces, self created or downloaded) of you choice and label them according to its contents(features). The labels are the names to your folders. ( in this example i used pictures of celebrities for training)
- Add path to your training folder.
- The model, features and labels are saved through code as yml files  and numpy (np) files respectively to be used in predicting.

2. Use model to predict features.
 - Here the model, labels and features are loaded into the file.
 - Use image of choice related to the images used for training to test the model.

Have Fun learning!