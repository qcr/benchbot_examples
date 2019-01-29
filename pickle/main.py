import pickle
import cv2
import sys
from numpy import array

data = pickle.load( open( sys.argv[1], "rb" ) )

for key in data:
    img = data[key]
    cv2.imshow(key, img)

cv2.waitKey()
