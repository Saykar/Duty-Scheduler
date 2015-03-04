__author__ = 'gauri'

import unittest
from flask.ext.testing import TestCase

from duty_app import app, db
from duty_app.workcalendar import get_working_day

from duty_app.models import Schedules, OffDuty
import json
from datetime import date, timedelta


class MyTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root123@localhost/duty_scheduler_test'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class SomeTest(MyTest):
    def init_schedules(self, data):
        headers = {'content-type': 'application/json'}
        response = self.client.post('/schedule/init', data=data, headers=headers)
        return response

    def test_root(self):
        response = self.client.get("/")
        # print self.app.url_map
        self.assert200(response)

    def test_schedule_model(self):
        schedule = Schedules('2015-03-03', "TestUser1")
        db.session.add(schedule)
        db.session.commit()
        assert schedule in db.session

    def test_off_duty_model(self):
        off_schedule = OffDuty("OffDutyUser1", '2015-03-04')
        db.session.add(off_schedule)
        db.session.commit()
        assert off_schedule in db.session

    def test_init_schedule(self):
        data = '{"users": ["User1", "User2"]}'
        response = self.init_schedules(data)
        self.assert200(response)

    def test_init_schedule_bad_data(self):
        data = '{"users": ["User1" "User2"]}'
        response = self.init_schedules(data)
        self.assert400(response)

    def test_get_all_schedules(self):
        data = '{"users": ["User1", "User2"]}'
        self.init_schedules(data)
        response = self.client.get("/schedules?time_range=month")
        schedules = response.json.get("schedules")
        day1 = get_working_day(date.today())
        day2 = get_working_day(day1+timedelta(days=1))
        user1 = schedules[0][str(day1)]
        user2 = schedules[1][str(day2)]
        self.assertEqual(user1, "User1", "Incorrect user")
        self.assertEqual(user2, "User2", "Incorrect user")
        self.assert200(response)

    def test_schedule_today(self):
        data = '{"users": ["User1"]}'
        self.init_schedules(data)
        response = self.client.get("/schedules?time_range=today")
        resp_data = json.loads(response.data)
        day = get_working_day(date.today())
        user = resp_data['schedules'][0][str(day)]
        self.assertEqual(user, "User1", "Incorrect user")
        self.assert200(response)

    def test_schedule_month(self):
        data = '{"users": ["User1", "User2", "User3"]}'
        self.init_schedules(data)
        response = self.client.get("/schedules?time_range=month")
        schedules = response.json.get("schedules")
        day1 = get_working_day(date.today())
        day2 = get_working_day(day1+timedelta(days=1))
        resp_data = json.loads(response.data)
        returned_user1 = resp_data['schedules'][0][str(day1)]
        returned_user2 = resp_data['schedules'][1][str(day2)]
        self.assertEqual(returned_user1, "User1", "Incorrect date")
        self.assertEqual(returned_user2, "User2", "Incorrect date")
        self.assert200(response)

    def test_schedule_for_user(self):
        data = '{"users": ["User1", "User1"]}'
        self.init_schedules(data)
        test_user = "User1"
        response = self.client.get("/schedules?user="+test_user)
        day1 = get_working_day(date.today())
        day2 = get_working_day(day1+timedelta(days=1))
        resp_data = json.loads(response.data)
        returned_user1 = resp_data['schedules'][0][str(day1)]
        returned_user2 = resp_data['schedules'][1][str(day2)]
        self.assertEqual(returned_user1, test_user, "Incorrect date")
        self.assertEqual(returned_user2, test_user, "Incorrect date")
        self.assert200(response)

if __name__ == '__main__':
    unittest.main()