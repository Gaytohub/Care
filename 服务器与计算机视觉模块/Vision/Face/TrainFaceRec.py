# import the necessary packages

from Util.FaceUtil import FaceUtil
from imutils import paths
# global variable
dataset_path = 'C:/Users/Administrator/Desktop/Cares/images/'
output_encoding_file_path = 'C:/Users/Administrator/Desktop/Cares/models/face_recognition_hog.pickle'
type = 1

# grab the paths to the input images in our dataset
print("[INFO] quantifying faces...")
image_paths = list(paths.list_images(dataset_path))
temp = str(image_paths).split('/')[-1]
temp = temp.split("\\")[0]
print(temp)
if len(image_paths) == 0:
    print('[ERROR] no images to train.')
else:
    faceutil = FaceUtil()
    print("[INFO] training face embeddings____")
    faceutil.save_embeddings(image_paths, output_encoding_file_path)
