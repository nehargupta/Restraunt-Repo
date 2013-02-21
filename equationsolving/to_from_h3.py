'''
to_from_h3.py
Neha Gupta under Dr. Chen
Last edited: 2/21/2013
Program:
	1. Connects to MongoDB and RabbitMQ
	2. Runs message
	3. When it recieves equations, goes to function callback
		A. prints message that order recieved
		B. Calls h3 program
		C. Updates order in DB
		D. Prints that order completed
		E. Repeats
'''

import pika			#connect to rabbit
from time import strftime	#used for clocktime of when equations recieved/finished
import pymongo			#used to connect to MongoDB
import ast			#Used to convert dictionary to string
import os			#Runs a message while processing equations
import time			#Allows for time.sleep
from initial_equations import MessageQ
#Connects to MongoDB
connect_eqsolver_ng = pymongo.Connection('localhost, 27017')
db = connect_eqsolver_ng.will_solve_ng
equation_will_solve_ng = db.will_solve_ng		


#Connects to Rabbit MQ
MQ_connection1 = MessageQ('unsolved_equations')
unsolved_connection, unsolved_channel  = MQ_connection1.connect()
MQ_connection2 = MessageQ('solutions')
solved_connection, solved_channel = MQ_connection2.connect()
#Prints message in Unix
#os.system('echo "[*] I am waiting for equations. To exit press CTRL+C"')



def callback(ch, method, properties, body):
    
    print " [x] Received %r" % (body,)

    os.system('h3 --version')
    #finish_time = strftime("%Y-%m-%d %H:%M:%S")
    #body = body[:-1]	#Removes last } character from string
    #body = body + ", 'time completed': '" + finish_time + "' }"	#Adds time completed to string and adds } character 
    body_dict = ast.literal_eval(body)	#Converts this to a dictionary
    equation_will_solve_ng.insert(body_dict)	#Sends that dictionary to DB
    # equation_will_solve_ng.insert({t : <time_t>, i : <ordinal> })
    print " [x] Done with %r" %(body)	
    ch.basic_ack(delivery_tag = method.delivery_tag)	#Acknowledges to Rabbit that done with order - accounts for sudden death

    solution = "the solutions to these equations are 5430" 	#See run_h3 function in solvemail.py??
    MQ_connection2.add_message(solution, solved_channel)

    os.system('echo "[*] I am waiting for equations. To exit press CTRL+C"')

#Recieves one message at a time from queue initial_equations and sends to callback function




MQ_connection1.consume(unsolved_channel, 'unsolved_equations')

