#encoding=utf-8
import cv2
#CAMERA_STAT = False
#VEDIO_DIR
import threading


class myThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.capture = None
        self.flag = True

    def open_camera(self):
        #CAMERA_STAT = True
        self.capture = cv2.VideoCapture(0)
        while self.flag:
            # for i in range(0, 10000000):
            # 获取一帧
            ret, frame = self.capture.read()
            # 将这帧转换为灰度图
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow('frame', gray)
            if cv2.waitKey(1) == ord('q'):
                break
            # if i == 100:
            #     capture.release()
            #     return
        self.capture.release()

    def get_frame(self):
        return

    def close_camera(self):
        #CAMERA_STAT = False
        if self.capture is not None:
            self.flag = False

    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        self.open_camera()






# # 创建新线程
thread1 = myThread(1, "Thread-1", 1)
#
# # 开启线程
thread1.start()
# import time
# time.sleep(2)
# thread1.close_camera()


