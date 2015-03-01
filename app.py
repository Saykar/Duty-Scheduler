__author__ = 'gauri'

from flask import Flask
from flask import make_response
from flask import jsonify
from flask import request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timedelta
from workalendar.usa import California
import calendar

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

def get_next_working_day(working_date):
    cal = California()
    holidays = cal.holidays(working_date.year)
    holiday_dates = []
    for holiday in holidays:
        holiday_dates.append(holiday[0])
    while working_date.weekday() > 4 or working_date in holiday_dates:
        working_date = working_date + timedelta(days=1)
    return working_date

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/users', methods=['POST'])
def add_users():
    print request.headers
    print request.data
    for data in request.json.get("users"):
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
        #check if day to be assigned is weekend/holiday
        day = get_next_working_day(day)
        schedule = Schedules(day,item)
        db.session.add(schedule)
        db.session.commit()
        day = day + timedelta(days=1)
    resp = make_response()
    data = {'message': "Success!"}
    resp = jsonify(data)
    return resp

@app.route('/schedules', methods=['GET'])
def get_schedules():
    user = request.args.get('user')
    time_range = request.args.get('time_range')
    today_date = date.today()
    schedule_list = []
    if user:
        schedule_list = Schedules.query.filter_by(name = user)
    elif time_range:
        if time_range == "today":
            schedule_list = Schedules.query.filter_by(date = today_date)
        elif time_range == "month":
            first_day = date(today_date.year, today_date.month, 1)
            days_in_month = calendar.monthrange(today_date.year,today_date.month)[1]
            last_day = date(today_date.year, today_date.month, days_in_month)
            schedule_list = Schedules.query.filter(Schedules.date.between(first_day,last_day))
    else:
        schedule_list = Schedules.query.all()
    #Display the query result as JSON
    json_list = []
    for schedule in schedule_list:
        json_obj = {str(schedule.date): schedule.name}
        json_list.append(json_obj)
    resp = make_response()
    resp = jsonify(schedules = json_list)
    return resp

if __name__ == "__main__":
    app.run(debug=1)

