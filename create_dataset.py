# creates a dataset via the mac's built in web cam utilizing a cnn to detect faces
# takes name of person as an argument

import cv2
import face_recognition
import argparse
import os

# argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--detection-method", type=str, default="hog",
                help="face detection model to use: either `hog` (light) or `cnn` (heavy)")
ap.add_argument("-n", "--name", type=str, help="label for the face in the dataset images")
args = vars(ap.parse_args())

dataset_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), args['name'])
if not os.path.exists(dataset_path):
    os.makedirs(dataset_path)
else:
    print("[WARNING] Directory for the name argument provided already exists!")
    print("[EXITING] Please choose a new name and re-run the script")
    exit()

cap = cv2.VideoCapture(0)

print("[WELCOME] Welcome to the face dataset creator!")
print("[INFO] Attempting to recognize face...")
faces_recognized = 0
while (True):
    ret, frame = cap.read()
    if not ret:
        print("[WARNING] Error retrieving frame from web-cam")
        exit()
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    box = face_recognition.face_locations(rgb_frame, model=args[
        'detection_method'])  # recognize face in frame and grab coordinates
    if len(box) <= 1:
        if box:  # prevents printing of a null variable
            top, right, bottom, left = box[0] # add support for
            faces_recognized += 1
            print("[%i] Face recognized..." % faces_recognized)
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            # cropped_face = frame[top:bottom, left:right]
            # cv2.imshow('face detected', cropped_face) # Display the face being detected
            image_path = os.path.join(dataset_path, args['name'] + "-" + str(faces_recognized) + ".jpg")
            cv2.imwrite(image_path, frame)  # save images with faces to disk
    else:
        print("[WARNING] Multiple faces detected!")
        # os.rmdir(dataset_path)
        # print("[INFO] Deleted dataset")
        # print("[EXITING]")
        # break

    cv2.imshow('face dataset creator', frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
