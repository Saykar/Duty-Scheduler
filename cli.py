__author__ = 'gauri'

import argparse
import requests
import json

argparser = argparse.ArgumentParser(description='Duty Scheduler')

argparser.add_argument('-t','--today', action="store_true", help='Displays today\'s Support Hero')
argparser.add_argument('-m','--month', action="store_true", help='Displays schedule for all users in current month')
argparser.add_argument('-i','--initialize', nargs='+', help='Initialize the schedule with starting order.  '
                                                            'Usage: cli -i <user1 user2 user3 user4 ...>')
argparser.add_argument('-u','--user', help='Displays user\'s schedule ')
argparser.add_argument('-s','--swap', nargs='+',
                       help='Usage: cli -s <user1 date1 user2 date2>. The date should be in YYYY-mm-dd format')
argparser.add_argument('-r','--reschedule', nargs='+',
                       help='Usage: cli -s <user1 date1>. Mark as undoable and reschedule to new date.')
options = vars(argparser.parse_args())
#print options

if options['today']:
    url = "http://127.0.0.1:5000/schedules?time_range=today"
    response = requests.get(url)
    json_data = json.loads(response.text)
    for schedule  in json_data['schedules']:
        for key, value in schedule.items():
            print key, value

if options['month']:
    url = "http://127.0.0.1:5000/schedules?time_range=month"
    response = requests.get(url)
    json_data = json.loads(response.text)
    for schedule  in json_data['schedules']:
        for key, value in schedule.items():
            print key, value

if options['initialize']:
    url = "http://127.0.0.1:5000/schedule/init"
    headers = {'Content-type' : 'application/json'}
    data = {'users': options['initialize']}
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        print "Success"
    else:
        print "Error"

if options['user']:
    url = "http://127.0.0.1:5000/schedules?user=" + options['user']
    response = requests.get(url)
    # print response.text
    print "Schedule for " + options['user']
    json_data = json.loads(response.text)
    for schedule in json_data['schedules']:
        for key in schedule.keys():
            print key

if options['swap']:
    url = "http://127.0.0.1:5000/schedule/swap"
    headers = {'Content-type' : 'application/json'}
    data = {'from_user': options['swap'][0],
            'from_date': options['swap'][1],
            'to_user': options['swap'][2],
            'to_date': options['swap'][3]}
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        print "Success"
    else:
        json_data = json.loads(response.text)
        for key, value in json_data.items():
            print key, value

if options['reschedule']:
    url = "http://127.0.0.1:5000/schedule/off-duty"
    headers = {'Content-type' : 'application/json'}
    data = {'user': options['reschedule'][0],
            'date': options['reschedule'][1]}
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        print "Success. New assignments:"
        # print response.text
        json_data = json.loads(response.text)
        for key, value in json_data.items():
            print key, value
    else:
        json_data = json.loads(response.text)
        for key, value in json_data.items():
            print key, value
