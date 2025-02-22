import hashlib
import requests
import re
import json
from collections import defaultdict
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from flask import Flask, render_template,jsonify,request,abort,Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from datetime import datetime
import time
import pika	#Import rabbitmq
#import os

credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('rabbitmq')
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue='syncQ')

'''import threading

def print_hello():
    print('Hello')
    timer = threading.Timer(2, print_hello) # # Call `print_hello` in 2 seconds.
    timer.start()

print_hello()'''

app=Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pdb/mydatabase.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}".format(os.path.join(os.path.dirname(os.path.abspath(__file__)),"sdb/mydatabase.db'
#db_path = os.path.join(os.path.dirname(__file__), 'mydatabase.db')
#db_uri = 'sqlite:///{}'.format('/sdb/')
db_uri = 'sqlite:////code/sdb/mydatabase.db'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

db = SQLAlchemy(app)

class user(db.Model):
	__tablename__ = 'user'
	username = db.Column(db.String(50), primary_key=True)
	password = db.Column(db.String(50))

class ride(db.Model):
	__tablename__ = 'rides'
	rideId = db.Column(db.Integer, primary_key=True)
	created_by = db.Column(db.String(50))
	timestamp = db.Column(db.DateTime)
	source = db.Column(db.Integer)
	destination = db.Column(db.Integer)

class ride_users(db.Model):
	__tablename__ = 'ride_users'
	rideId = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), primary_key=True)

db.create_all()



def callback(ch, method, properties, body):

	statement = str(body).strip("b")
	statement = statement.strip("\'")
	statement = statement.strip("\"")
	if "DELETE" in statement:
		statement = text(statement)
		result = db.engine.execute(statement.execution_options(autocommit=True))

	else:
		statement = text(statement)
		
		try:
			result = db.engine.execute(statement.execution_options(autocommit=True))
			res = {"code": 200, "msg": "Insertion Successful"}

		except IntegrityError:
			res = {"code": 400, "msg": "Duplicate entry"}
	
	print(" [x] Received %r \n" % body)


channel.basic_consume(on_message_callback = callback, queue = 'syncQ',auto_ack = True)
print(' [*] Waiting for -----WRITE---- messages. To exit press CTRL+C')
channel.start_consuming()

if __name__ == '__main__':
	
	app.debug=True
	app.run(host="0.0.0.0", debug = True)