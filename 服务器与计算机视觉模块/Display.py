import socket
import cv2
import threading
import struct
import numpy
import _thread

from flask_cors import CORS

from Util.JudgeInteract import faceRegniZation
from flask import Flask, render_template, Response


app = Flask(__name__)
CORS(app, supports_credentials=True)
status = 0
sz = (640, 480)
fps = 5
fourcc = cv2.VideoWriter_fourcc(*'XVID')
vout = cv2.VideoWriter()

count = 0

def constructPath():
    global count
    count += 1
    return  'C:/Users/Administrator/Desktop/Cares/Vision/output' + str(count) + '.avi'


class Camera_Connect_Object:

    temp = None

    def __init__(self,D_addr_port=["",8880]):
        self.resolution=[640,480]
        self.addr_port=D_addr_port
        self.src=888+15                 #双方确定传输帧数，（888）为校验值
        self.interval=0                 #图片播放时间间隔
        self.img_fps=5                 #每秒传输多少帧数

    def Set_socket(self):
        self.client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

    def Socket_Connect(self):
        self.Set_socket()
        self.client.connect(self.addr_port)
        print("IP is %s:%d" % (self.addr_port[0],self.addr_port[1]))

    def shut_down(self):
        self.client.close()

    def RT_Image(self):
        #按照格式打包发送帧数和分辨率
        self.name=self.addr_port[0]+" Camera"
        self.client.send(struct.pack("lhh", self.src, self.resolution[0], self.resolution[1]))
        while(True):
            info=struct.unpack("lhh",self.client.recv(8))
            buf_size=info[0]                    #获取读的图片总长度
            if buf_size:
                try:
                    self.buf=b""                #代表bytes类型
                    temp_buf=self.buf
                    while(buf_size):            #读取每一张图片的长度
                        temp_buf=self.client.recv(buf_size)
                        buf_size-=len(temp_buf)
                        self.buf+=temp_buf      #获取图片
                        data = numpy.fromstring(self.buf, dtype='uint8')    #按uint8转换为图像矩阵
                        self.image = cv2.imdecode(data, 1)                  #图像解码

                        Camera_Connect_Object.temp = self.image

                        _thread.start_new_thread(faceRegniZation, ( self.image, ))
                        cv2.imshow("Face Recongnition", self.image)

                        # cv2.imshow(self.name, self.image)                   #展示图片
                except:
                    pass
                finally:
                    if(cv2.waitKey(10)==27):        #每10ms刷新一次图片，按‘ESC’（27）退出
                        self.client.close()
                        cv2.destroyAllWindows()
                        break

    def get_frame(self):
        # info = struct.unpack("lhh", self.client.recv(8))
        # buf_size = info[0]
        # temp_buf = self.client.recv(buf_size)
        # buf_size -= len(temp_buf)
        # self.buf += temp_buf  # 获取图片
        # data = numpy.fromstring(self.buf, dtype='uint8')  # 按uint8转换为图像矩阵
        # self.image = cv2.imdecode(data, 1)  # 图像解码
        # ret, jpeg = cv2.imencode('.jpg', self.image)

        ret, jpeg = cv2.imencode('.jpg', Camera_Connect_Object.temp)
        return jpeg.tobytes()

    def Get_Data(self,interval):
        showThread=threading.Thread(target=self.RT_Image)
        showThread.start()

@app.route('/')  # 主页
def index():
    # jinja2模板，具体格式保存在index.html文件中
    # return render_template('index.html')
    return "hello world"
def gen(camera):
    while True:
        frame = camera.get_frame()
        # 使用generator函数输出视频流， 每次请求输出的content类型是image/jpeg
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

camera = Camera_Connect_Object()
@app.route('/video_feed')  # 这个地址返回视频流响应
def video_feed():
    global status
    if (status == 1):
        camera.Socket_Connect()
        camera.Get_Data(camera.interval)
        status = status -  1
    return Response(gen(camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/release')
def release():
    global status
    status = status + 1
    camera.shut_down()
    return "ok"

if __name__ == '__main__':
    # camera = Camera_Connect_Object()
    # camera.get_frame()
    camera.addr_port[0]="192.168.10.104"
    camera.addr_port=tuple(camera.addr_port)
    camera.Socket_Connect()
    camera.Get_Data(camera.interval)
    #app.run(host='0.0.0.0', debug=True, port=)