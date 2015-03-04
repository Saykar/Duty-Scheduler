__author__ = 'gauri'

from duty_app import db

# User model
class Users(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), primary_key=True)
    #schedules = db.relationship('Schedules',backref='Users')
    #constructor
    def __init__(self, name):
        self.name = name


#Schedule model
class Schedules(db.Model):
    date = db.Column(db.Date, primary_key=True)
    name = db.Column(db.String(100))  #, db.ForeignKey('users.name'))
    #constructor
    def __init__(self, date, name):
        self.date = date
        self.name = name


#off-duty model
class OffDuty(db.Model):
    name = db.Column(db.String(100), primary_key=True)
    date = db.Column(db.Date, primary_key=True)
    #constructor
    def __init__(self, name, off_date):
        self.name = name
        self.date = off_date

