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

#off-duty model
class OffDuty(db.Model):
    name = db.Column(db.String(100),primary_key=True)
    date = db.Column(db.Date,primary_key=True)
    #constructor
    def __init__(self, name, off_date):
        self.name = name
        self.date = off_date

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
    #resp = make_response()
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
    #resp = make_response()
    data = {'message': "Success!"}
    resp = jsonify(data)
    return resp

@app.route('/schedule/swap', methods=['POST'])
def swap():
    from_user = request.json.get("from_user")
    from_date = request.json.get("from_date")
    to_user = request.json.get("to_user")
    to_date = request.json.get("to_date")
    resp = make_response()
    if (datetime.strptime(from_date ,"%Y-%m-%d").date() <= date.today() or \
                    datetime.strptime(to_date ,"%Y-%m-%d").date() <= date.today()):
        resp = jsonify({"error" : "Date cannot be today or before"})
        resp.status_code = 400
    from_schedule = Schedules.query.filter_by(name=from_user,date=from_date).first()
    to_schedule = Schedules.query.filter_by(name=to_user,date=to_date).first()
    if from_schedule and to_schedule:
        from_schedule.name = to_user
        to_schedule.name = from_user
        db.session.commit()
        resp = jsonify({})
    else:
        resp.status_code = 404
    return resp

@app.route('/schedule/off-duty', methods=['POST'])
def off_duty():
    resp = make_response()
    user = request.json.get("user")
    off_duty_date = request.json.get("date")
    schedule = Schedules.query.filter_by(name=user,date=off_duty_date).first()
    if schedule is None:
        resp = jsonify({"error":"You are not assigned for this date. No need to off-duty."})
        resp.status_code = 400
        return resp
    else:
        # find a user to replace
        tomorrow = date.today()+timedelta(days=1)
        schedule_list = Schedules.query.filter(Schedules.name != user, Schedules.date >= tomorrow)
        for schedule in schedule_list:
            print schedule.name
            replacement_in_off_duty = OffDuty.query.filter_by(name = schedule.name, date = off_duty_date).first()
            # If this user is not off-call on same date
            if replacement_in_off_duty is None:
                to_user = schedule.name
                to_date = schedule.date
                from_schedule = Schedules.query.filter_by(name=user,date=off_duty_date).first()
                to_schedule = Schedules.query.filter_by(name=to_user,date=to_date).first()
                if from_schedule and to_schedule:
                    from_schedule.name = to_user
                    to_schedule.name = user
                    db.session.commit()
                    # Now add this to off-duty table
                    off_duty = OffDuty(user, off_duty_date)
                    try:
                        db.session.add(off_duty)
                        db.session.commit()
                    except Exception as e:
                        print e
                        print "The off-call entry already exists"
                        db.session.rollback()
                    resp = jsonify({from_schedule.name:str(from_schedule.date),to_schedule.name : str(to_schedule.date)})
                    break;
                else:
                    print "The user is off call on the same date"
        resp = jsonify({"error" : "No one available for replacement"})
        resp.status_code = 400
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
    #resp = make_response()
    resp = jsonify(schedules = json_list)
    return resp

if __name__ == "__main__":
    app.run(debug=1)

