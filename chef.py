'''
chef.py
Neha Gupta under Dr. Chen
Last edited: 2/14/2013
Program:
	1. Connects to MongoDB and RabbitMQ
	2. Runs message
	3. When it recieves an order, goes to function callback
		A. prints message that order recieved
		B. Sleeps to stimulate cooking
		C. Updates order in DB
		D. Prints that order completed
		E. Repeats
'''

import pika			#connect to rabbit
from time import strftime	#used for clocktime of orders
import pymongo			#used to connect to MongoDB
import ast			#Used to convert dictionary to string
import os			#Runs a message while waiting for order

#Connects to MongoDB
c = pymongo.Connection('localhost, 27017')
db = c.bbb
orders_bbb = db.orders_bbb		

#Connects to Rabbit MQ
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='kitchen', durable=True)

#Prints message in Unix
os.system('echo "[*] I am waiting for an order. To exit press CTRL+C"')


def callback(ch, method, properties, body):
    
    print " [x] Received %r" % (body,)
    time.sleep(10)
    finish_time = strftime("%Y-%m-%d %H:%M:%S")
    body = body[:-1]	#Removes last } character from string
    body = body + ", 'time completed': '" + finish_time + "' }"	#Adds time completed to 							string and adds } character 
    body_dict = ast.literal_eval(body)	#Converts this to a dictionary
    orders_bbb.insert(body_dict)	#Sends that dictionary to DB
    print " [x] Done with %r" %(body)	
    ch.basic_ack(delivery_tag = method.delivery_tag)	#Acknowledges to Rabbit that 								done with order
    os.system('echo "[*] I am waiting for an order. To exit press CTRL+C"')

#Recieves one message at a time from queue kitchen and sends to callback function
channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='kitchen')
channel.start_consuming()


