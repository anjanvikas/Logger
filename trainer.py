import os
import cv2
import numpy as np
from PIL import Image
import pyprind

def getImagesWithId(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    imagePaths.remove(os.path.join(path, '.keep'))
    faces = []
    ids = []
    n = len(imagePaths)
    bar = pyprind.ProgBar(n, track_time = True, title = "Retrieving Dataset")
    for imagePath in imagePaths:
        faceImg = Image.open(imagePath).convert('L')
        faceNp = np.array(faceImg, 'uint8')
        identifier = int(os.path.split(imagePath)[-1].split('.')[1])
        faces.append(faceNp)
        ids.append(identifier)
        cv2.imshow("Training", faceNp)
        cv2.waitKey(10)
        bar.update()
    return ids, faces

def main():
    recognizer = cv2.createLBPHFaceRecognizer()
    path = "dataSet"
    ids, faces = getImagesWithId(path)
    recognizer.train(faces, np.array(ids))
    recognizer.save(os.path.join("recognizer", "trainingData.yml"))
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
