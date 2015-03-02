__author__ = 'gauri'

import argparse
import requests

argparser = argparse.ArgumentParser(description='Duty Scheduler')

argparser.add_argument('-i','--initialize', nargs='+', help='Initialize the schedule with starting order')
argparser.add_argument('-t','--today', action="store_true", help='Displays today\'s Support Hero')
argparser.add_argument('-m','--month', action="store_true", help='Displays schedule for all users in current month')
argparser.add_argument('-u','--user', help='Displays user\'s schedule ')
options = vars(argparser.parse_args())
print options

if options['initialize']:
    url = "http://127.0.0.1:5000/schedule/init"
    headers = {'Content-type' : 'application/json'}
    data = {'users': options['initialize']}
    response = requests.post(url, json=data, headers=headers)
    print response

if options['today']:
    url = "http://127.0.0.1:5000/schedules?time_range=today"
    response = requests.get(url)
    print response

if options['month']:
    url = "http://127.0.0.1:5000/schedules?time_range=month"
    response = requests.get(url)
    print response.text

if options['user']:
    url = "http://127.0.0.1:5000/schedules?user=" + options['user']
    response = requests.get(url)
    print response.text