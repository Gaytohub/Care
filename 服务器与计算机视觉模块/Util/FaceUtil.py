#encoding=utf-8


import face_recognition
import cv2
import pickle
import os


class FaceUtil:
    # 超参数
    detection_method = 'hog'  # either 'hog' on 'cnn*. default is hog.
    tolerance = 0.3

    def __init__(self, encoding_file_path=None):
        if encoding_file_path:
            self.load_embeddings(encoding_file_path)

    # load embeddings
    def load_embeddings(self, encoding_file_path):
        # load the known faces and embeddings
        print("[INFO] loading face encodings____")
        self.data = pickle.loads(open(encoding_file_path, "rb").read())

    def get_face_location(self, image):
        face_location_list = []
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        face_locations = face_recognition.face_locations(gray, number_of_times_to_upsample=1,
                                                         model=self.detection_method)

        for (top, right, bottom, left) in face_locations:
            face_location_list.append((left, top, right, bottom))

        return face_location_list

    def get_face_location_name_and_type(self, image):
        # convert the input frame from BGR to RGB
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # detect the (x, y)-coordinates of the bounding boxes
        # cornesponding to each face in the input frame, then
        # compute the facial embeddings for each face
        boxes = face_recognition.face_locations(
            rgb, model=self.detection_method)
        encodings = face_recognition.face_encodings(rgb, boxes)
         # initialize the list of names for each face detected
        names = []

        types = []

        # loop over the facial embeddings
        for encoding in encodings:
        # attempt to match each face in the input image to
        # our known encodings
            matches = face_recognition.compare_faces(
                self.data["encodings"], encoding,
                tolerance = self.tolerance)
            name = "Unknown"
            type = 4
            # check to see if we have found a match
            if True in matches:
                # find the indexes of all matched faces then
                # initialize a dictionary to count the total number
                # of times each face was matched
                matched_idxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}
                counts2 = {}
                # loop oven the matched indexes and maintain a count
                # for each recognized face face
                for i in matched_idxs:
                    name = self.data["names"][i]
                    type = self.data["types"][i]
                    counts[name] = counts.get(name, 0) + 1
                    counts2[type] = counts2.get(type, 0) + 1
                # determine the recognized face with the largest
                # number of votes (note: in the event of an unlikely
                # tie Python will select first entry in the
                # dictionary)
                name = max(counts, key=counts.get)
                type = max(counts2, key=counts2.get)

                # update the list of names
            names.append(name)
            types.append(type)
        face_location_list = []
        for ((top, right, bottom, left)) in boxes:
            face_location_list.append((left, top, right, bottom))

        return face_location_list, names, types

    def save_embeddings(self, image_paths, output_encoding_file_path):    ## type 表示录入人的身份。 老人，义工，工作人员三种。
        warning = ''
        types = 0
        # initialize the list of known encodings and known names
        known_encodings = []
        known_names = []
        known_type = []
        # loop oven the image paths
        for (i, image_path) in enumerate(image_paths):
        # extract the person name from the image path
            temp = str(image_path).split('/')[-1]
            temp = temp.split("\\")[0]
            print(temp)
            if (temp == 'zzj'):
                types = 2
                print("hhhhh")
            else:
                types = 1
                print("hape")
            print("[INFO] processing image {}/{}"
                .format(i + 1, len(image_paths)))
            name = temp
            print("wo cao " + name)

            # load the input image and convert it from
            # R6B (OpenCV ordering) to dlib ordering (RGB)
            image = cv2.imread(image_path)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # detect the (x, y)-coordinates of the bounding boxes
            # cornesponding to each face in the input image
            boxes = face_recognition.face_locations(
                    rgb, model=self.detection_method)

            # compute the facial embedding for the face
            encodings = face_recognition.face_encodings(rgb, boxes)

            if len(encodings) != 1:
                os.remove(image_path)
                warning += '[WARNING] detected %d faces in %s. This file is deleted.'%		  			(len(encodings), image_path)
                continue

            # loop over the encodings
            for encoding in encodings:
            # add each encoding + name to our set of known names
            # and encodings
                known_encodings.append(encoding)
                known_names.append(name)
                print(types)
                known_type.append(types)
        # dump the facial encodings + names to disk
        print("[INFO] serializing encodings...")
        data = {"encodings": known_encodings, "names": known_names, "types" : known_type}
        f = open(output_encoding_file_path, "wb")
        f.write(pickle.dumps(data))
        f.close()

        if warning:
            print(warning)

if __name__ == "__main__":
    faceutil = FaceUtil()
    image = cv2.imread('a.JPG')
    facelocation = faceutil.get_face_location(image)
    print(facelocation)
