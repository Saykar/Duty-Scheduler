__author__ = 'gauri'

from flask import url_for

from flask_testing import TestCase

from duty_app import app
from duty_app.models import db, Users


class BaseTestCase(TestCase):
    """A base test case for flask-tracking."""

    def create_app(self):
        return app

    def setUp(self):
        db.app = self.app
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_duty_api_root(self):
        response = self.client.get(url_for('.hello'))
        self.assert200(response, "Should hit the / endpoint")

    def test_duty_api_today(self):
        response = self.client.get(url_for('.get_schedules', data={"time_range":"today"}))
        self.assert200(response, "Should hit the / endpoint")

    def test_duty_api_month(self):
        response = self.client.get(url_for('.get_schedules', data={"time_range":"month"}))
        print response
        self.assert200(response, "Should hit the / endpoint")
'''
    def test_duty_api_init(self):
        response = self.client.post('/schedule/init', data={"users" : ["User1", "User2"]},
                                    headers={"content-type":"application/json"})
        print response
        self.assert200(response, "Should initialize with the starting order")
'''