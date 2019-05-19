# USAGE
# python test_network.py --model santa_not_santa.model --image images/examples/santa_01.png

# import the necessary packages
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import argparse
import imutils
import cv2
import time
import numpy
from PIL import Image
import cv2
import mss


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", required=True,
	help="path to trained model model")
#ap.add_argument("-i", "--image", required=True,
#	help="path to input image")
args = vars(ap.parse_args())

with mss.mss() as sct:
    model = load_model(args["model"])
    monitor = {"top":40, "left":0, "width": 800, "height": 640}
    while "Screen capturing":
        last_time = time.time()
        # load the image
        frame = numpy.array(sct.grab(monitor))
        #image = cv2.imread(img)
        orig = frame.copy()
        # pre-process the image for classification
        image = cv2.resize(frame, (28, 28))
        image = image.astype("float") / 255.0
        image = img_to_array(frame)
        image = np.expand_dims(frame, axis=0)
        # load the trained convolutional neural network
        print("[INFO] loading network...")
    
        # classify the input image
        (notSanta, santa) = model.predict(image)[0]
        # build the label
        label = "win" if santa > notSanta else "lose"
        proba = santa if santa > notSanta else notSanta
        label = "{}: {:.2f}%".format(label, proba * 100)        
        # draw the label on the image
        output = imutils.resize(orig, width=400)
        cv2.putText(output, label, (10, 25),  cv2.FONT_HERSHEY_SIMPLEX,
	        0.7, (0, 255, 0), 2)
        print("fps: {}".format(1/(time.time()-last_time)))
        # show the output image
        cv2.imshow("Output", output)
        cv2.waitKey(0)
     

