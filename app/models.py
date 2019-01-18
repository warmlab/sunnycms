import json

from time import time
from datetime import datetime
from urllib.parse import urlencode
from urllib.request import urlopen
from urllib.request import Request

#from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

#from flask import current_app#, url_for
from flask_sqlalchemy import SQLAlchemy
#from flask_login import UserMixin
from flask_security import RoleMixin, UserMixin, SQLAlchemySessionUserDatastore
from werkzeug.security import generate_password_hash, check_password_hash

from itsdangerous import TimedJSONWebSignatureSerializer as TimedSerializer
from itsdangerous import JSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature

db = SQLAlchemy()

#from db import Column

class Corporation(db.Model):
    __tablename__ = 'corporation'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    from_time = db.Column(db.DateTime, default=datetime.now)
    end_time = db.Column(db.DateTime, default=datetime.now)
    banner = db.Column(db.String(256))

    phone = db.Column(db.String(15))
    mobile = db.Column(db.String(15))
    mail = db.Column(db.String(64))
    address = db.Column(db.String(256))
    accreditation = db.Column(db.String(32)) # 备案编号

    note = db.Column(db.Text)

staff_role = db.Table('staff_role',
        db.Column('staff_id', db.Integer(), db.ForeignKey('staff.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    note = db.Column(db.String(255))

class Staff(UserMixin, db.Model):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, primary_key=True)
    openid = db.Column(db.String(64), index=True) # used in weixin
    nickname = db.Column(db.String(128)) # 昵称
    name = db.Column(db.String(128), index=True) # 姓名
    password_hash = db.Column(db.String(128))
    gender = db.Column(db.SmallInteger, default=0) # 会员性别, 0为unkown
    phone = db.Column(db.String(12), unique=True, index=True) #手机号码
    email = db.Column(db.String(64), unique=True, index=True)
    privilege = db.Column(db.Integer, default=0) # every bit as a privilege

    # TODO share holder information
    #is_share_holder = db.Column(db.Boolean, default=False)
    #is_main = db.Column(db.Boolean, default=False)

    corporation_id = db.Column(db.Integer, db.ForeignKey('corporation.id'))
    corporation = db.relationship('Corporation', backref=db.backref('staffs', lazy='dynamic'))

    #posts = db.relationship('Post', backref='author', lazy='dynamic')
    roles = db.relationship('Role', secondary=staff_role,
                            backref=db.backref('staffs', lazy='dynamic'))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    @property
    def confirmed(self):
        if self.confirmed_at and self.confirmed_at < datetime.now():
            return True
        return False

    @property
    def is_anonymous(self):
        return False

    def is_active(self):
        #return self.active
        return True

    def is_authenticated(self):
        return True

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return self.email

staff_datastore = SQLAlchemySessionUserDatastore(db, Staff, Role)

class Province(db.Model): # just for China
    __tablename__ = 'province'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False)
    index = db.Column(db.Integer, default=0)

class City(db.Model):
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False)
    index = db.Column(db.Integer, default=0)
    province_id = db.Column(db.Integer, db.ForeignKey('province.id'))

    province = db.relationship('Province', backref=db.backref('citys', lazy='dynamic'))

class District(db.Model):
    __tablename__ = 'district'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False)
    index = db.Column(db.Integer, default=0)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))

    city = db.relationship('City', backref=db.backref('districts', lazy='dynamic'))

class Community(db.Model): # 小区或者村庄
    __tablename__ = 'community'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False)
    index = db.Column(db.Integer, default=0)
    appraisal_value = db.Column(db.BigInteger, default=0)

    district_id = db.Column(db.Integer, db.ForeignKey('district.id'))
    district = db.relationship('District', backref=db.backref('communities', lazy='dynamic'))

class Building(db.Model): # 楼座
    __tablename__ = 'building'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(7)) # 几号楼
    index = db.Column(db.Integer, default=0)
    from_year = db.Column(db.DateTime, default=datetime.now, nullable=False)
    end_year = db.Column(db.DateTime, default=datetime.now, nullable=False) # 产权到期时间
    appraisal_value = db.Column(db.BigInteger, default=0)

    community_id = db.Column(db.Integer, db.ForeignKey('community.id'))
    community = db.relationship('Community', backref=db.backref('buildings', lazy='dynamic'))

class Unit(db.Model):
    __tablename__ = 'unit'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(7)) # 几单元
    index = db.Column(db.Integer, default=0)
    appraisal_value = db.Column(db.BigInteger, default=0)

    building_id = db.Column(db.Integer, db.ForeignKey('building.id'))
    building = db.relationship('Building', backref=db.backref('units', lazy='dynamic'))

class Room(db.Model):
    __tablename__ = 'room'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(8), index=True)
    decorator_style = db.Column(db.DateTime, default=datetime.now, nullable=False) # 装修风格
    decorator_time = db.Column(db.DateTime, default=datetime.now, nullable=False) # 装修时间
    appraisal_value = db.Column(db.BigInteger, default=0) # 评估后的价值，单位元
    appraisal_time = db.Column(db.DateTime, default=datetime.now, nullable=False) # 评估时间

    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'))
    unit = db.relationship('Unit', backref=db.backref('rooms', lazy='dynamic'))

    owners = db.relationship('UserRoom', back_populates='room')

class UserRoom(db.Model):
    __tablename__ = 'user_name'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), primary_key=True)
    from_time = db.Column(db.DateTime, default=datetime.now)
    end_time = db.Column(db.DateTime, default=datetime.now)
    bought_value = db.Column(db.BigInteger, default=0) # 购买时的价格

    user = db.relationship('User', back_populates='rooms')
    room = db.relationship('Room', back_populates='owners')

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    openid = db.Column(db.String(64), unique=True)
    nickname = db.Column(db.String(128))
    avatar_url = db.Column(db.String(2048))
    name = db.Column(db.String(128)) # 会员姓名
    phone = db.Column(db.String(12)) # 会员电话
    mobile = db.Column(db.String(12)) # 会员另一个电话
    id_number = db.Column(db.String(18), index=True) # 身份证号码
    # TODO 是否需要身份证照片

    # 针对小程序登录需要的参数
    session_key = db.Column(db.String(256)) # 第三方返回的session key
    access_token = db.Column(db.String(256)) # 用户登录需要的令牌
    expires_time = db.Column(db.BigInteger) # timestamp, 有效期是2hours

    rooms = db.relationship('UserRoom', back_populates='user')

    def generate_auth_token(self, secret_key, expiration=7200):
        s = TimedSerializer(secret_key, expires_in=expiration)

        return s.dumps({'openid': self.openid})

    def generate_access_token(self, secret_key):
        s = Serializer(secret_key)#, expires_in=expiration)
        self.access_token = s.dumps({'session_key': self.session_key}).decode('UTF-8')

    def verify_access_token(self, secret_key):
        s = Serializer(secret_key)
        try:
            data = s.loads(self.access_token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token

        #print('session_keys:', self.session_key, data['session_key'])
        return self.session_key == data['session_key']

    @staticmethod
    def verify_auth_token(token, secret_key):
        s = TimedSerializer(secret_key)
        try:
            data = s.loads(s)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token

        return MemeberOpenid.query.get(data['openid'])

class Post(db.Model): # 最新咨询
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(32))
    type = db.Column(db.Integer, default=0) # 1 - 咨询； 2 - 业绩
    title = db.Column(db.String(64))
    summary = db.Column(db.String(256))
    body = db.Column(db.Text)
    modify_time = db.Column(db.DateTime, default=datetime.now, index=True)
    publish_time = db.Column(db.DateTime, default=datetime.now, index=True)

    author_id = db.Column(db.Integer, db.ForeignKey('staff.id'))
    author = db.relationship('Staff', backref=db.backref('posts', lazy=True))

    corporation_id = db.Column(db.Integer, db.ForeignKey('corporation.id'))
    corporation = db.relationship('Corporation', backref=db.backref('posts', lazy=True))

class Appraisal(db.Model):
    __tablename__ = 'appraisal'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(16))
    name = db.Column(db.String(64), nullable=False)
    summary = db.Column(db.String(256))
    note = db.Column(db.Text)

    corporation_id = db.Column(db.Integer, db.ForeignKey('corporation.id'))
    corporation = db.relationship('Corporation', backref=db.backref('apps', lazy=True))

class Job(db.Model):
    __tablename__ = 'job'
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.SmallInteger, default=0) # 在页面中的排序
    name = db.Column(db.String(64))
    min_experience_years = db.Column(db.Integer, default=0) # 最少工作年限
    max_age = db.Column(db.Integer, default=60)
    salary_from = db.Column(db.Integer, default=1000)
    salary_to = db.Column(db.Integer, default=1000)
    duty = db.Column(db.Text) # 工作职责
    summary = db.Column(db.Text) # 工作描述
    skills = db.Column(db.Text) # 工作描述
    modify_date = db.Column(db.DateTime, default=datetime.now)
    publish_date = db.Column(db.DateTime, default=datetime.now)

    corporation_id = db.Column(db.Integer, db.ForeignKey('corporation.id'))
    corporation = db.relationship('Corporation', backref=db.backref('jobs', lazy=True))

#class Tendency(db.Model): # 
#    __tablename__ = 'tendency'
#    id = db.Column(db.Integer, primary_key=True)
#
#    corporation_id = db.Column(db.Integer, db.ForeignKey('corporation.id'))
#    corporation = db.relationship('Corporation', backref=db.backref('apps', lazy=True))
