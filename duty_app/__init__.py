from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root123@localhost/duty_scheduler'

db = SQLAlchemy()

from routes import duty_api
app.register_blueprint(duty_api)

db.app = app
db.init_app(app)

# Create tables for corresponding models defined above
db.create_all()
