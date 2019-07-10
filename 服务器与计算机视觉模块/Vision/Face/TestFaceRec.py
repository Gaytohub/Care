# import the necessary packages
from Util.FaceUtil import FaceUtil
import cv2
import time
import argparse
import imutils
#传入参数
from Vision.Smile.SmileDetect import test

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--filename", required = False, default ='',help="")
args = vars(ap.parse_args())
#全局变量
facial_recognition_model_path = 'C:/Users/Administrator/Desktop/Cares/models/face_recognition_hog.pickle'
input_video = args['filename']
#初始化摄像头
if not input_video:
    vs = cv2.VideoCapture(0)
    time.sleep(2)
else:
    vs = cv2.VideoCapture(input_video)
#初始化人脸识别模&
faceutil = FaceUtil(facial_recognition_model_path)

#不斷循环
while True:
    # grab the current frame
    (grabbed, frame) = vs.read()

    # if we are viewing a video and did not grab a frame, then we
    # have reached the end of the video
    if input_video and not grabbed:
        break
    if not input_video:
        frame = cv2.flip(frame, 1)

    # resize the frame, convert it to grayscale, and then clone the
    # original frame so we can draw on it later in the program
    frame = imutils.resize(frame, width = 600)

    face_location_list, names, types = faceutil.get_face_location_name_and_type(
        frame)


    print(types)

    # loop over the face bounding boxes
    for ((left, top, right, bottom), name, type) in zip(
                                face_location_list,
                                names, types) :
        #   display label and bounding box rectangle on the output frame
        cv2.putText(frame, name, (left, top - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.rectangle(frame, (left, top), (right, bottom),
            (0, 0, 255), 2)

        if (type == 1):
            res = test(cv2.resize(frame[top:bottom, left:right], (48, 48)))
            if (res == "happy"):
                print("wo hen hape")
                # user = Event_info(0, time.strftime('%Y-%m-%d', time.localtime(time.time())), name)
                # user.add()
                # save_jpg(image, "happy")

    cv2.imshow("Face Recongnition", frame)

    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break

vs.release()
cv2.destroyAllWindows()
