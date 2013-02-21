'''
initial_equations.py
Neha Gupta under Dr. Chen
Last edited: 2/19/2013
Similar to waiter.py program in /Restraunt-Repo
Program:
	1. establishes a connection to the MongoDB database and rabbitMQ channel
	2. prompts user to enter equations.
	3. sends these equations to the unsolved_equations queue
	4. saves these equations in DB
	5. closes
'''

import pika 			#connect to rabbit
from time import strftime	#used for clocktime of orders
import pymongo			#used to connect to MongoDB
import ast			#Used to convert dictionary to string

import pika

class connect_to_rabbit:
	'''This function will connect to rabbit_rq for both chef and waiter programs
	'''
	def __init__(self, name):
		self.namequeue = name
	def connect(self):
		connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))	
		channel = connection.channel()
		channel.queue_declare(queue = self.namequeue, durable = True)
		return connnection,channel
	def add_message(self, initial_eq_str, channel):
		channel.basic_publish(exchange = '', routing_key = self.namequeue, body = intial_eq_str, properties = pika.BasicProperties(delivery_mode = 2))
	def disconnect(self, connection):
		coneection.close()

#Connect to database:
connect_eqsolver_ng = pymongo.Connection('localhost, 27017')
db = connect_eqsolver_ng.will_solve_ng
equation_will_solve_ng = db.will_solve_ng		

#Connect to rabbitMQ channel
#unsolved_equations = queue name
MQ_connection = rabbit_mq_connect('unsolved_equations')
connection, channel = MQ_connection.connect()

#Defining the things to go into the order from user input:
#start_time = strftime("%Y-%m-%d %H:%M:%S")
name_str = raw_input("What is the first equation? ")
food_str = raw_input("What is the second equation? ")

#Joins user input into a string
intial_eq_str = "{'first equation': '" + name_str + "', 'second equation': '" + food_str + "'}" 
initial_eq_dict = ast.literal_eval(initial_eq_str)	#Converts string to dict

#Sends the string to the queue, where it will be picked up by to_from_h3.py
#channel.basic_publish(exchange = '', routing_key = 'unsolved_equations', body = intial_eq_str, properties = pika.BasicProperties(delivery_mode = 2))
MQ_connection.add_message(initail_eq_str, channel)
equation_will_solve_ng.insert(initial_eq_dict)		#Adds dictionary order to DB
equation_will_solve_ng.insert({t : <time_t>, i : <ordinal> })

#Prints in shell that order has been sent
print "[x] Sent order %r" % (intial_eq_str,)

#Closes connection to channel to queue and then quits program
MQ_connection.disconnect(connection)




