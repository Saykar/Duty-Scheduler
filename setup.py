__author__ = 'gauri'

from sqlalchemy import create_engine

engine = create_engine("mysql://root:root123@localhost",echo=True)
engine.execute("CREATE DATABASE IF NOT EXISTS duty_scheduler")
engine.execute("CREATE DATABASE IF NOT EXISTS duty_scheduler_test")
