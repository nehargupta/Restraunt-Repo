'''
waiter.py
Neha Gupta under Dr. Chen
Last edited: 2/14/2013
Program:
	1. establishes a connection to the MongoDB database and rabbitMQ channel
	2. prompts user for a customer name and food.
	3. sends this order to the kitchen queue
	4. saves order in DB
	5. closes
'''

import pika 			#connect to rabbit
from time import strftime	#used for clocktime of orders
import pymongo			#used to connect to MongoDB
import ast			#Used to convert dictionary to string

#Connect to database:
c = pymongo.Connection('localhost, 27017')
db = c.bbb
orders_bbb = db.orders_bbb		

#Connect to rabbitMQ channel
connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))	
channel = connection.channel()
channel.queue_declare(queue = 'kitchen', durable = True) #kitchen = queue name

#Defining the things to go into the order from user input:
start_time = strftime("%Y-%m-%d %H:%M:%S")
name_str = raw_input("What is the customer's name? ")
food_str = raw_input("What food does the customer want? ")

#Joins user input into a string
order_John_str = "{'customer': '" + name_str + "', 'food': '" + food_str + "', 'time ordered': '" + (start_time) + "' }" 
order_John_dict = ast.literal_eval(order_John_str)	#Converts string to dict

#Sends the string to the queue, where it will be picked up by chef.py
channel.basic_publish(exchange = '', routing_key = 'kitchen', body = order_John_str, properties = pika.BasicProperties(delivery_mode = 2))
orders_bbb.insert(order_John_dict)		#Adds dictionary order to DB

#Prints in shell that order has been sent
print "[x] Sent order %r" % (order_John_str,)

#Closes connection to channel to queue and then quits program
connection.close()




