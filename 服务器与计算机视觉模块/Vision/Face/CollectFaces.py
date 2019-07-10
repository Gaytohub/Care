# -*- coding: utf-8 -*-
import sys

# import argparse
from Util.FaceUtil import FaceUtil
from Util import AudioPlayer
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
import os
import shutil
import time
# import face_recognition

# MODEL_DIR = os.path.realpath(__file__).rsplit('\\', 2)[0]
# audioplayer.play_audio(os.path.join('../audios', 'multi_faces_detected.mp3'))


def collect(id):
    audio_dir = 'C:/Users/Administrator/Desktop/Cares/Audios'
    error = 0
    start_time = None
    limit_time = 2

    # ap = argparse.ArgumentParser()
    # ap.add_argument('-ic', '--id', required=True, help='')
    # ap.add_argument('-id', '--imagedir', required=True, help='')
    # args = vars(ap.parse_args())

    # args = {'imagedir' : 'images/', 'id' : 'xuefeiue'}

    action_list = ['blink', 'open_mouth', 'smile', 'raise_head', 'bow_head', 'look_left', 'look_right']
    action_map = {'blink': '请眨眼', 'open_mouth': '请张嘴', 'smile': '请笑一笑', 'raise_head': '请抬头',
                  'bow_head': '请低头', 'look_left': '请向左前方看', 'look_right': '请向右前方看'}
    imagedir = 'images/'
    #id是名字
    cam = cv2.VideoCapture(0)
    #cam.set(3, 640)
    #cam.set(4, 480)

    faceutil = FaceUtil()

    counter = 0
    while True:
        counter += 1
        ret, image = cam.read()
        if counter <= 10:
            continue

        image = cv2.flip(image, 1)

        if error == 1:
            end_time = time.time()
            difference = end_time - start_time
            print(difference)
            if difference >= limit_time:
                error = 0

        face_location_list = faceutil.get_face_location(image)
        # print((face_location_list))
        print(face_location_list)
        for (left, top, right, bottom) in face_location_list:
            cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)

        cv2.imshow('Collecting Faces', image)

        k = cv2.waitKey(100) & 0xff
        if k == 27:
             break

        face_count = len(face_location_list)
        if error == 0 and face_count == 0:
            print('[WARNING] 没有检测到人脸')
            AudioPlayer.play_audio(os.path.join(audio_dir, 'no_face_detected.mp3'))

        elif error == 0 and face_count == 1:
            print('[INFO] 可以开始采集图像了')
            # print(os.path.join(audio_dir, 'start_image_capturing.mp3'))
            AudioPlayer.play_audio(os.path.join(audio_dir, 'start_image_capturing.mp3'))
            break
        elif error == 0 and face_count > 1:
            print('[WARNING] 检测到多张人脸')
            AudioPlayer.play_audio(os.path.join(audio_dir, 'multi_faces_detected.mp3'))
            error = 1
            start_time = time.time()
        else:
            pass


    if os.path.exists(os.path.join(imagedir, id)):
        shutil.rmtree(os.path.join(imagedir, id), True)
    os.makedirs(os.path.join(imagedir, id))

    for action in action_list:
        AudioPlayer.play_audio(os.path.join(audio_dir, action+'.mp3'))
        action_name = action_map[action]

        counter = 1
        for i in range(15):
            print('%s-%d' %(action_name, i))
            ret, img_OpenCV = cam.read()
            img_OpenCV = cv2.flip(img_OpenCV, 1)
            origin_img = img_OpenCV.copy()

            face_location_list = faceutil.get_face_location(img_OpenCV)
            for (left, top, right, bottom) in face_location_list:
                cv2.rectangle(img_OpenCV, (left, top), (right, bottom), (0, 0, 255), 2)

            img_PIL = Image.fromarray(cv2.cvtColor(img_OpenCV, cv2.COLOR_BGR2RGB))

            draw = ImageDraw.Draw(img_PIL)
            #Linux
            draw.text((int(image.shape[1]/2), 30), action_name,
                font=ImageFont.truetype('mingliub.ttc', 40),
                fill=(255, 0, 0))
            #windows
            #draw.text((int(image.shape[1] / 2), 30), action_name)
                      #font=ImageFont.truetype('calibril.ttc', 40),
                      # fill=(255, 0, 0))
            img_OpenCV = cv2.cvtColor(np.asarray(img_PIL), cv2.COLOR_RGB2BGR)

            cv2.imshow('Collectiong Face', img_OpenCV)

            image_name = os.path.join(imagedir, id, action+'_'+str(counter)+'.jpg')
            cv2.imwrite(image_name, origin_img)

            k = cv2.waitKey(100) & 0xff
            if k == 27:
                break
            counter += 1

    print('采集完毕')
    AudioPlayer.play_audio(os.path.join(audio_dir, 'end_capturing.mp3'))

    cam.release()
    cv2.destroyAllWindows()
    # def set_modeldir(dir):
    #     global MODEL_DIR
    #     MODEL_DIR = dir

if __name__ == '__main__':
    collect("yzw")