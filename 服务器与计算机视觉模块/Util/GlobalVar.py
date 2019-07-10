import argparse
from Util.FaceUtil import FaceUtil

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--filename", required = False, default ='',help="")
args = vars(ap.parse_args())
#全局变量
facial_recognition_model_path = 'C:/Users/Administrator/Desktop/Cares/models/face_recognition_hog.pickle'
input_video = args['filename']
is_invaded = 0
is_interact = 0
is_fall = 0
is_forbidden = 0

faceutil = FaceUtil(facial_recognition_model_path)

# def faceRegniZation(image):
#     data = numpy.array(image)
#
#     face_location_list, names, types = faceutil.get_face_location_name_and_type(
#         data)
#
#     is_invaded = is_Invaded(types, is_invaded, data)
#     print(is_invaded)
