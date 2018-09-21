from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os

default_encoding_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "encodings.pickle")

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--dataset", required=True, help="path to input directory of faces + images")
ap.add_argument("-e", "--encodings", default=default_encoding_path,
                help="path to serialized db of facial encodings")
ap.add_argument("-d", "--detection-method", type=str, default="hog",
                help="face detection model to use: either `hog` or `cnn`")
args = vars(ap.parse_args())

if not os.path.exists(default_encoding_path):
    print("[WELCOME] Encoding provided dataset images...")
else:
    print("[WARNING] Encoding file already exists here:")
    print(default_encoding_path)
    response = input("Would you like to overwrite this encoding file? (y/n): ")
    if response is 'n':
        print("[EXITING] Please re-run and enter a new name for the encoding file!")
        exit()
    else:
        print("[INFO] face_trainer will continue and overwrite the previous encoding file!")

print("[INFO] quantifying faces...")
imagePaths = list(paths.list_images(args["dataset"]))
knownEncodings = []  # initialize the list of known encodings and known names
knownNames = []

# loop over the image paths
for (i, imagePath) in enumerate(imagePaths):
    # extract the person name from the image path
    print("[INFO] processing image {}/{}".format(i + 1, len(imagePaths)))
    name = imagePath.split(os.path.sep)[-2]
    image = cv2.imread(imagePath)
    # cv2.imshow("face", image)
    # cv2.waitKey(0)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb, model=args["detection_method"])
    encodings = face_recognition.face_encodings(rgb, boxes)
    for encoding in encodings: # for loop to cover the case of multiple faces in the picture
        knownEncodings.append(encoding)
        knownNames.append(name)
    

print("[INFO] serializing encodings...")  # writing the facial encodings and names to the disk
data = {"encodings": knownEncodings, "names": knownNames}
f = open(args["encodings"], "wb")
f.write(pickle.dumps(data))
f.close()
print("[COMPLETE]")
