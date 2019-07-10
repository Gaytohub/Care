import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import pymysql
import datetime
import time
from werkzeug.security import generate_password_hash,check_password_hash
#from flask_login import UserMixin
pymysql.install_as_MySQLdb()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:123456@localhost/first_flask"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=7)

# 创建数据库的操作对象
db = SQLAlchemy(app)

class Sys_user(db.Model):
    __tablename__ = "Sys_user"
    identify = db.Column(db.String(16),primary_key=True)
    _password = db.Column(db.String(256), nullable=False)
    real_name = db.Column(db.String(16), nullable=False)
    gender = db.Column(db.String(16))
    tel = db.Column(db.BigInteger)

    def __init__(self, identify, pwd, real_name, gender = None, tel = None):
        self.identify = identify
        self._password = generate_password_hash(pwd)
        self.real_name = real_name
        self.gender = gender
        self.tel = tel

    def check_passwd(self, pwd):
        return check_password_hash(self._password, pwd)

    def add(self):
        db.session.add(self)
        return db.session.commit()

    def search(self, identify):
        return Sys_user.query.filter(Sys_user.identify == identify).first()

    def mod(self,identify, pwd):
        user = Sys_user.query.filter(Sys_user.identify == identify).first()
        user._password = generate_password_hash(pwd)
        return db.session.commit()


class Volunteer_info(db.Model):
    __tablename__ = "Volunteer_info"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True,nullable=False)
    name = db.Column(db.String(16))
    gender = db.Column(db.String(16))
    tel = db.Column(db.BigInteger)
    pic_src = db.Column(db.String(128))
    checkin_date = db.Column(db.DateTime)
    checkout_date = db.Column(db.DateTime)

    def __init__(self, id, name = None, gender = None, tel = None, pic_src = None, checkin_date = None, checkout_date = None):
        self.id = id
        self.name = name
        self.gender = gender
        self.tel = tel
        self.pic_src = pic_src
        self.checkin_date = checkin_date
        self.checkout_date = checkout_date

    def add(self):
        db.session.add(self)
        return db.session.commit()

    def delete(self, id):
        db.session.delete(Volunteer_info.search(id))
        return db.session.commit()

    def search(self, id):
        return Sys_user.query.filter(Volunteer_info.id == id)

    def mod(self, id, name, gender, tel, pic_src, checkin_date, checkout_date):
        user = Sys_user.query.filter_by(Sys_user.identify == id).first()
        user.name = name
        user.pic_src = pic_src
        user.gender = gender
        user.tel = tel
        user.checkin_date = checkin_date
        user.checkout_date = checkout_date
        return db.session.commit()

class Employee_info(db.Model):
    __tablename__ = "Employee_info"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True,nullable=False)
    name = db.Column(db.String(16))
    gender = db.Column(db.String(16))
    tel = db.Column(db.BigInteger)
    pic_src = db.Column(db.String(128))
    hire_date = db.Column(db.DateTime)
    resign_date = db.Column(db.DateTime)

    def __init__(self, id, name=None, gender=None, tel=None, pic_src=None, hire_date=None, resign_date=None):
        self.id = id
        self.name = name
        self.gender = gender
        self.tel = tel
        self.pic_src = pic_src
        self.hire_date = hire_date
        self.resign_date = resign_date

    def add(self):
        db.session.add(self)
        return db.session.commit()

    def delete(self, id):
        db.session.delete(Employee_info.search(id))
        return db.session.commit()

    def search(self, id):
        return Sys_user.query.filter(Employee_info.id == id)

    def mod(self, id, name, gender, tel, pic_src, hire_date, resign_date):
        user = Sys_user.query.filter_by(Sys_user.identify == id).first()
        user.name = name
        user.pic_src = pic_src
        user.gender = gender
        user.tel = tel
        user.hire_date = hire_date
        user.resign_date = resign_date
        return db.session.commit()

class Oldperson_info(db.Model):
    __tablename__ = "Oldperson_info"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True,nullable=False)
    name = db.Column(db.String(16))
    gender = db.Column(db.String(16))
    tel = db.Column(db.BigInteger)
    pic_src = db.Column(db.String(128))
    checkin_date = db.Column(db.DateTime)
    checkout_date = db.Column(db.DateTime)
    first_guardian_name = db.Column(db.String(16))
    first_guardian_relation = db.Column(db.Integer)
    first_guardian_tel = db.Column(db.Integer)

    def __init__(self, id, name=None, gender=None, tel=None, pic_src=None, checkin_date=None,
                 checkout_date=None, first_guardian_name = None, first_guardian_relation = None,
                 first_guardian_tel = None):
        self.id = id
        self.name = name
        self.gender = gender
        self.tel = tel
        self.pic_src = pic_src
        self.checkin_date = checkin_date
        self.checkout_date = checkout_date
        self.first_guardian_name = first_guardian_name
        self.first_guardian_relation = first_guardian_relation
        self.first_guardian_tel = first_guardian_tel

    def add(self):
        db.session.add(self)
        return db.session.commit()

    def delete(self, id):
        db.session.delete(Oldperson_info.search(id))
        return db.session.commit()

    def search(self, id):
        return Sys_user.query.filter(Oldperson_info.id == id)

    def mod(self, id, name, gender, tel, pic_src, checkin_date, checkout_date,
            first_guardian_name, first_guardian_relation, first_guardian_tel):
        user = Sys_user.query.filter_by(Sys_user.identify == id).first()
        user.name = name
        user.pic_src = pic_src
        user.gender = gender
        user.tel = tel
        user.checkin_date = checkin_date
        user.checkout_date = checkout_date
        user.first_guardian_name = first_guardian_name
        user.first_guardian_relation = first_guardian_relation
        user.first_guardian_tel = first_guardian_tel
        return db.session.commit()

class Event_info(db.Model):
    __tablename__ = "Event_info"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True,nullable=False)
    event_type = db.Column(db.Integer, nullable=False)
    event_date = db.Column(db.DateTime, nullable=False)
    oldperson_id = db.Column(db.Integer)

    def __init__(self, event_type, event_date, oldperson_id = None):
        self.event_type = event_type
        self.event_date = event_date
        self.oldperson_id = oldperson_id

    def add(self):
        db.session.add(self)
        return db.session.commit()

    def search(self, event_date):
        smile_time = Sys_user.query.filter(Event_info.event_date == event_date and Event_info.event_type == 0)
        fall_time = Sys_user.query.filter(Event_info.event_date == event_date and Event_info.event_type == 3)
        return {"smile_time":smile_time, "fall_time":fall_time}


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    db.session.commit()
