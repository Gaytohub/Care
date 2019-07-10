from flask import Flask, request, render_template
from flask_cors import CORS
from flask_login import LoginManager, login_user, login_required
import json
import datetime
import os
from flask_sqlalchemy import SQLAlchemy
import pymysql

from Util import send
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
        user = Sys_user(data['id'], data['password'], data['real_name'],
                              data['gender'], data['telephone'])

        if Sys_user.query.filter(Sys_user.identify == data['id']).first():
            msg = {"valid": "error"}
        else:
            user.mod(data['id'], data['password'], data['real_name'],
                     data['gender'], data['telephone'])
            msg = {"valid": "done"}

    return json.dumps(msg)

@login_required
@app.route('/oldperson_required', methods=['POST', 'GET'])
def oldperson_required():
    if request.method == 'POST' or request.method == 'GET':
        data = db.session.execute("SELECT * FROM first_flask.oldperson_info")
        db.session.commit()
        payload = []
        content = {}
        for result in data:
            content = {'id': result[0], 'name': result[1].encode("unicode_escape").decode("unicode_escape"), 'gender': result[2], 'tel': result[3], 'pic_src': result[4],
                       'checkin_date': result[5].strftime("%Y-%m-%d"),'checkout_date': result[6].strftime("%Y-%m-%d"), 'first_guardian_name': result[7],
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
        for item in data:
            user = Oldperson_info(int(item['id']), item['name'],
                              item['gender'], int(item['telephone']), item['avatarUrl'],datetime.datetime.strptime(item['check_in_date'],"%Y-%m-%d"),
                            datetime.datetime.strptime(item['check_out_date'],"%Y-%m-%d"),item['firstguardian'], int(item['relationship']), int(item['phoneOfFirstGuardian']))
            user.add()
        msg = {"valid":"done"}
        return json.dumps(msg)


@login_required
@app.route('/volunteer_required', methods=['POST', 'GET'])
def volunteer_required():
    if request.method == 'POST' or request.method == 'GET':
        data = db.session.execute("SELECT * FROM first_flask.volunteer_info")
        db.session.commit()
        payload = []
        content = {}
        for result in data:
            content = {'id': result[0], 'name': result[1].encode("unicode_escape").decode("unicode_escape"), 'gender': result[2], 'tel': result[3], 'pic_src': result[4],
                       'checkin_date': result[5].strftime("%Y-%m-%d"),'checkout_date': result[6].strftime("%Y-%m-%d")}
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
        for item in data:
            user = Oldperson_info(int(item['id']), item['name'],
                              item['gender'], int(item['telephone']), item['avatarUrl'],datetime.datetime.strptime(item['check_in_date'],"%Y-%m-%d"),
                            datetime.datetime.strptime(item['check_out_date'],"%Y-%m-%d"))
            user.add()
        msg = {"valid":"done"}
        return json.dumps(msg)

@login_required
@app.route('/employee_required', methods=['POST', 'GET'])
def employee_required():
    if request.method == 'POST' or request.method == 'GET':
        data = db.session.execute("SELECT * FROM first_flask.employee_info")
        db.session.commit()
        payload = []
        content = {}
        for result in data:
            content = {'id': result[0], 'name': result[1].encode("unicode_escape").decode("unicode_escape"), 'gender': result[2], 'tel': result[3], 'pic_src': result[4],
                       'hire_date': result[5].strftime("%Y-%m-%d"),'resign_date': result[6].strftime("%Y-%m-%d")}
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
        for item in data:
            user = Oldperson_info(int(item['id']), item['name'],
                              item['gender'], int(item['telephone']), item['avatarUrl'],datetime.datetime.strptime(item['hire_date'],"%Y-%m-%d"),
                            datetime.datetime.strptime(item['resign_date'],"%Y-%m-%d"))
            user.add()
        msg = {"valid":"done"}
        return json.dumps(msg)

@app.route('/user/<userid>')  # 主页
def user(userid):
    CollectFaces.collect(userid)
    return "ok"


@app.route('/send/<userid>')  # 主页
def sendmessage(userid):
    # print(os.path.exists('images/' + userid + '.zip'))
    if send.send(userid):
        # print(os.path.exists('images/'+userid+'.zip'))
        send.socket_client('images/'+userid+'.zip',ip='192.168.43.68',port=7777)
        return "ok"
    return "no"



if __name__ == '__main__':
    app.debug = True
    app.run(host = "0.0.0.0")
