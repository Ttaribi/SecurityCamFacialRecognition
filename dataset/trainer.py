import os
import cv2
import numpy as np
from PIL import Image

#This file will train our model with the pictures from dataset_creator.py


recognizer = cv2.face.LBPHFaceRecognizer_create()
path = "/Users/mitchelltaribi/Desktop/FacialRecognition/dataset"



def get_images_with_id(path):
    images_paths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]  # set images path to os
    faces = []
    ids = []

    for single_image_path in images_paths:
        faceImg = Image.open(single_image_path).convert('L')  #image converted into gray color  L = luminance
        faceNp = np.array(faceImg, np.uint8)
        id = int(os.path.split(single_image_path)[-1].split(".")[1])
        print(id)

        faces.append(faceNp)
        ids.append(id)

        cv2.imshow("Training", faceNp)
        cv2.waitKey(10)

    return np.array(ids), faces

ids,faces=get_images_with_id(path)
recognizer.train(faces,ids)
if not os.path.exists("recognizer"):
    os.makedirs("recognizer")

recognizer.save("../recognizer/trainingdata.yml")


cv2.destroyAllWindows()
