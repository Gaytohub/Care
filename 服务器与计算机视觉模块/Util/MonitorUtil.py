import time

import cv2
import os

from Vision.Smile.SmileDetect import test
from model import Event_info
import datetime

fgbg = cv2.createBackgroundSubtractorMOG2()
weight = 0

def is_Invaded(types, is_invaded,image):
    if (4 in types and is_invaded == 0):
        user = Event_info(2, datetime.datetime.now())
        user.add()
        save_jpg(image, "invaded")
        return 1
    elif (4 not in types):
        return 0


def is_FallDown(face_location_list, names, types, image):
    global weight
    for ((left, top, right, bottom), name, type) in zip(
            face_location_list,
            names, types):
        # 微笑检测
        if (type == 1):
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            fgmask = fgbg.apply(gray)
            # Find contours
            contours, hierarchy = cv2.findContours(fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            if contours:
                areas = []
                for contour in contours:
                    ar = cv2.contourArea(contour)
                    areas.append(ar)
                max_area = max(areas or [0])
                max_area_index = areas.index(max_area)
                cnt = contours[max_area_index]
                M = cv2.moments(cnt)
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.drawContours(fgmask, [cnt], 0, (255, 255, 255), 3, maxLevel=0)
                if h < w:
                    weight += 1
                if weight > 10:
                    # print "FALL"
                    # cv2.putText(fgmask, 'FALL', (x, y), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255,255,255), 2)
                    user = Event_info(3, time.strftime('%Y-%m-%d', time.localtime(time.time())), name)
                    user.add()
                    save_jpg(image, "falldown")
                if h > w:
                    weight = 0

def is_Smile(face_location_list, names, types, image):
    for ((left, top, right, bottom), name, type) in zip(
            face_location_list,
            names, types):
        # 微笑检测
        if (type == 1):
            res = test(cv2.resize(image[top:bottom, left:right], (48, 48)))
            if (res == "happy"):
                print("wo hen hape")
                user = Event_info(0, time.strftime('%Y-%m-%d', time.localtime(time.time())), 1)
                user.add()
                save_jpg(image, "happy")


def is_Interact(types,names, is_interact,image):
    if (2 in types and is_interact == 0):
        for (name, type) in zip(names, types):
            if type == 1:
                user = Event_info(1, datetime.datetime.now(), 1)
                user.add()
                save_jpg(image, "interact")
        return 1
    elif (2 not in types):
        return 0

# def is_Fall(types,names, is_fall,image):
#     if (1 in types and is_fall == 0):
#         user = Event_info(2, datetime.datetime.now())
#         user.add()
#         save_jpg(image, "invaded")
#         return 1
#     elif ('2' not in types):
#         return 0


def is_Forbidden(names, is_forbidden, image):
    if names and is_forbidden == 0:
        user = Event_info(4, datetime.datetime.now())
        user.add()
        save_jpg(image, "forbidden")
        return 1
    else:
        return 0

def save_jpg(image, kind, path="../images"):
    # print(image)
    # img = cv2.imencode('.jpg', image)
    if not os.path.exists(path + '/' + kind + '/'):
        os.mkdir(path + '/' + kind + '/')
    cv2.imwrite(path + '/' + kind + '/' + time.strftime('%Y%m%d%H%M%S')+str(int(time.time()*100%100)) + '.jpg', image)
    # cv2.imwrite(path + '/' + kind + '/' + str(int(time.time() * 100 )) + '.jpg', img)

# save_jpg('','forbidden')