__author__ = 'gauri'

from flask import Flask
from flask import make_response
from flask import jsonify
from flask import request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timedelta

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root123@localhost/duty_scheduler'
db = SQLAlchemy(app)

#User model
class Users(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), primary_key=True)
    #schedules = db.relationship('Schedules',backref='Users')
    #constructor
    def __init__(self,name):
        self.name = name

#Schedule model
class Schedules(db.Model):
    date = db.Column(db.Date, primary_key=True)
    name = db.Column(db.String(100))#, db.ForeignKey('users.name'))
    #constructor
    def __init__(self, date, name):
        self.date = date
        self.name = name

db.create_all()

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/users', methods=['POST'])
def add_users():
    print request.headers
    print request.data
    for data in request.json.get("users"):
        print data
        user = Users(data)
        db.session.add(user)
    db.session.commit()
    resp = make_response()
    data = {'message': "Success!"}
    resp = jsonify(data)
    return resp

@app.route('/users', methods=['GET'])
def get_all_users():
    userList = Users.query.all()
    list = []
    for user in userList:
        list.append(user.name)
    resp = make_response()
    resp = jsonify(users = list)
    return resp

@app.route('/schedule/init', methods=['POST'])
def init_schedule():
    print request.headers
    print request.data
    Schedules.query.delete()
    day = date.today()
    for item in request.json.get("users"):
        print item
        schedule = Schedules(day,item)
        db.session.add(schedule)
        day = day + timedelta(days=1)
        db.session.commit()
    resp = make_response()
    data = {'message': "Success!"}
    resp = jsonify(data)
    return resp

@app.route('/schedules', methods=['GET'])
def get_schedules():
    scheduleList = Schedules.query.all()
    list = []
    for schedule in scheduleList:
        json_obj = {}
        json_obj[str(schedule.date)] = schedule.name
        list.append(json_obj)
    resp = make_response()
    resp = jsonify(schedules = list)
    return resp

if __name__ == "__main__":
    app.run(debug=1)

