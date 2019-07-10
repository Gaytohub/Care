from flask_cors import CORS
from flask_login import LoginManager, login_user, login_required
import json
import datetime
import os
from flask_sqlalchemy import SQLAlchemy
import pymysql
import socket
import cv2
import threading
import struct
import numpy
import _thread
from Util.JudgeInteract import faceRegniZation
from flask import Flask, render_template, Response, request


from Util import send, receive
from Vision.Face import CollectFaces
from model import Sys_user, Volunteer_info, Employee_info, Oldperson_info, Event_info
pymysql.install_as_MySQLdb()

app = Flask(__name__)
CORS(app, supports_credentials=True)
login_manager = LoginManager()
login_manager.init_app(app)

app.config['JSON_AS_ASCII'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:123456@localhost/first_flask"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=7)

db = SQLAlchemy(app)

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

@app.route('/login', methods=['POST', 'GET'])
def login():
    msg = None
    if request.method == 'POST' or request.method == 'GET':
        temp = json.dumps(request.get_json())
        data = json.loads(temp)
        user = Sys_user.query.filter(Sys_user.identify == data['id']).first()

        if user and user.check_passwd(data['password']) :
            #login_user(user)
            msg = {"valid": "done"}
        else:
            msg = {"valid": "error"}

    return json.dumps(msg)

@app.route('/register', methods=['POST', 'GET'])
def register():
    msg = None
    if request.method == 'POST' or request.method == 'GET':
        temp = json.dumps(request.get_json())
        data = json.loads(temp)
        user = Sys_user(data['id'], data['password'], data['real_name'], data['gender'], data['telephone'])

        if Sys_user.query.filter(Sys_user.identify == data['id']).first():
            msg = {"valid":"error"}
        else:
            user.add()
            msg = {"valid":"done"}

    return json.dumps(msg)

@login_required
@app.route('/modify', methods=['POST', 'GET'])
def modify():
    msg = None
    if request.method == 'POST' or request.method == 'GET':
        temp = json.dumps(request.get_json())
        data = json.loads(temp)
        #data = json.loads(data)
        user = Sys_user.query.filter(Sys_user.identify == data['name']).first()
        if user and user.check_passwd(data['password']) == False:
            user.mod(data['name'], data['password'])
            msg = {"valid": "done"}
        else:
            msg = {"valid": "error"}

    return json.dumps(msg)

@login_required
@app.route('/oldperson_required', methods=['POST', 'GET'])
def oldperson_required():
    if request.method == 'POST' or request.method == 'GET':
        data = db.session.execute("SELECT * FROM first_flask.oldperson_info")
        db.session.commit()
        data = list(data)
        payload = []
        content = {}
        for result in data:
            content = {'id': result[0], 'name': result[1].encode("unicode_escape").decode("unicode_escape"), 'gender': result[2], 'tel': result[3], 'pic_src': result[4],
                       'checkin_date': result[5].strftime("%Y-%m-%d"),'checkout_date': None, 'first_guardian_name': result[7],
                       'first_guardian_relation': result[8],'first_guardian_tel':result[9]}
            payload.append(content)
            content = {}

        return json.dumps(payload)

@login_required
@app.route('/oldperson', methods=['POST', 'GET'])
def oldperson():
    if request.method == 'POST' or request.method == 'GET':
        db.session.execute("DELETE FROM first_flask.oldperson_info")
        db.session.commit()
        temp = json.dumps(request.get_json())
        data = json.loads(temp)
        data = json.loads(data)
        for item in data:
            user = Oldperson_info(int(item['id']), item['name'],
                              item['gender'], int(item['tel']), None, datetime.datetime.now(),None,
                           item['first_guardian_name'],None, int(item['first_guardian_tel']))
            user.add()
        msg = {"valid":"done"}
        return json.dumps(msg)


@login_required
@app.route('/volunteer_required', methods=['POST', 'GET'])
def volunteer_required():
    if request.method == 'POST' or request.method == 'GET':
        data = db.session.execute("SELECT * FROM first_flask.volunteer_info")
        db.session.commit()
        data = list(data)
        payload = []
        content = {}
        for result in data:
            content = {'id': result[0], 'name': result[1].encode("unicode_escape").decode("unicode_escape"), 'gender': result[2], 'tel': result[3], 'pic_src': result[4],
                       'checkin_date': result[5].strftime("%Y-%m-%d"),'checkout_date': None}
            payload.append(content)
            content = {}
        return json.dumps(payload)


@login_required
@app.route('/volunteer', methods=['POST', 'GET'])
def volunteer():
    if request.method == 'POST' or request.method == 'GET':
        db.session.execute("DELETE FROM first_flask.volunteer_info")
        db.session.commit()
        temp = json.dumps(request.get_json())
        data = json.loads(temp)
        data = json.loads(data)
        for item in data:
            user = Volunteer_info(int(item['id']), item['name'],
                              item['gender'], int(item['tel']), None,datetime.datetime.now(),
                            None)
            user.add()
        msg = {"valid":"done"}
        return json.dumps(msg)

@login_required
@app.route('/employee_required', methods=['POST', 'GET'])
def employee_required():
    if request.method == 'POST' or request.method == 'GET':
        data = db.session.execute("SELECT * FROM first_flask.employee_info")
        db.session.commit()
        data = list(data)
        payload = []
        content = {}
        for result in data:
            content = {'id': result[0], 'name': result[1].encode("unicode_escape").decode("unicode_escape"), 'gender': result[2], 'tel': result[3], 'pic_src': result[4],
                       'hire_date': result[5].strftime("%Y-%m-%d"),'resign_date':None}
            payload.append(content)
            content = {}
        return json.dumps(payload)

@login_required
@app.route('/employee', methods=['POST', 'GET'])
def employee():
    if request.method == 'POST' or request.method == 'GET':
        db.session.execute("DELETE FROM first_flask.employee_info")
        db.session.commit()
        temp = json.dumps(request.get_json())
        data = json.loads(temp)
        data = json.loads(data)
        for item in data:
            user = Oldperson_info(int(item['id']), item['name'],
                              item['gender'], int(item['tel']), None,datetime.datetime.now(),
                            None)
            user.add()
        msg = {"valid":"done"}
        return json.dumps(msg)


@login_required
@app.route('/smile', methods=['POST', 'GET'])
def smile():
    if request.method == 'POST' or request.method == 'GET':
        data = db.session.execute("SELECT * FROM first_flask.event_info WHERE event_type = 0")
        db.session.commit()
        smile_time = {'0':0,'1':0,'2':0,'3':0,'4':0,'5':0,'6':0}
        cur_time = datetime.datetime.now()
        for item in data:
            day = (cur_time - item[2]).days
            if day <= 6:
                smile_time[str(day+2)]+=1
        return json.dumps(smile_time)

@login_required
@app.route('/invade', methods=['POST', 'GET'])
def invaded():
    if request.method == 'POST' or request.method == 'GET':
        data = db.session.execute("SELECT * FROM first_flask.event_info WHERE event_type = 2")
        db.session.commit()
        invaded_time = {'0':0,'1':0,'2':0,'3':0,'4':0,'5':0,'6':0}
        cur_time = datetime.datetime.now()
        for item in data:
            day = (cur_time - item[2]).days
            if day <= 6:
                invaded_time[str(day+2)]+=1
        print(json.dumps(invaded_time))
        return json.dumps(invaded_time)

@login_required
@app.route('/interact', methods=['POST', 'GET'])
def interact():
    if request.method == 'POST' or request.method == 'GET':
        data = db.session.execute("SELECT * FROM first_flask.event_info WHERE event_type = 1")
        db.session.commit()
        interact_time = {'0':0,'1':0,'2':0,'3':0,'4':0,'5':0,'6':0}
        cur_time = datetime.datetime.now()
        for item in data:
            day = (cur_time - item[2]).days
            if day <= 6:
                interact_time[str(day+2)]+=1
        return json.dumps(interact_time)

@login_required
@app.route('/fall', methods=['POST', 'GET'])
def fall():
    if request.method == 'POST' or request.method == 'GET':
        data = db.session.execute("SELECT * FROM first_flask.event_info WHERE event_type = 3")
        db.session.commit()
        fall_time = {'0':0,'1':0,'2':0,'3':0,'4':0,'5':0,'6':0}
        cur_time = datetime.datetime.now()
        for item in data:
            day = (cur_time - item[2]).days
            if day <= 6:
                fall_time[str(day)]+=1
        return json.dumps(fall_time)

@login_required
@app.route('/forbidden', methods=['POST', 'GET'])
def forbiddien():
    if request.method == 'POST' or request.method == 'GET':
        data = db.session.execute("SELECT * FROM first_flask.event_info WHERE event_type = 4")
        db.session.commit()
        forbiddien_time = {'0':0,'1':0,'2':0,'3':0,'4':0,'5':0,'6':0}
        cur_time = datetime.datetime.now()
        for item in data:
            day = (cur_time - item[2]).days
            if day <= 6:
                forbiddien_time[str(day+2)]+=1
        return json.dumps(forbiddien_time)

@app.route('/user/<userid>')  # 主页
def user(userid):
    CollectFaces.collect(userid)
    return "ok"


@app.route('/send/<userid>')  # 主页
def sendmessage(userid):
    if send.send(userid):
        # receive.receive(userid)
        send.socket_client('../images/'+userid+'.zip')
        return "ok"
    return "no"


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
        vout.open(constructPath(), fourcc, fps, sz, True)
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

                        vout.write(self.image)

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
    vout.release()
    camera.shut_down()
    return "ok"


if __name__ == '__main__':
    app.debug = True
    camera.addr_port[0] = "192.168.10.104"
    camera.addr_port = tuple(camera.addr_port)
    camera.Socket_Connect()
    camera.Get_Data(camera.interval)
    app.run(host='0.0.0.0', debug=True, port=5000)
