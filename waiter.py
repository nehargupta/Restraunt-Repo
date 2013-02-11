import pika #connect to rabbit
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))	#insert machine name at 'localhost'
channel = connection.channel()

channel.queue_declare(queue = 'kitchen', durable = True) #kitchen = queue name

message = ' '.join(sys.argv[1:])
channel.basic_publish(exchange = '', routing_key = 'kitchen', body = message, properties = pika.BasicProperties(delivery_mode = 2))
print "[x] Sent order %r" % (message,)
connection.close()
