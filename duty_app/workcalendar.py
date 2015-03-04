__author__ = 'gauri'

from datetime import timedelta
from workalendar.usa import California

# Function to account for holidays/weekends
# If the current day is working day it returns current day otherwise returns the next working day
def get_working_day(working_date):
    cal = California()
    holidays = cal.holidays(working_date.year)
    holiday_dates = []
    for holiday in holidays:
        holiday_dates.append(holiday[0])
    while working_date.weekday() > 4 or working_date in holiday_dates:
        working_date = working_date + timedelta(days=1)
    return working_date
