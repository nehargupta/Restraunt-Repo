import pika
import time

# Create the connection to the server
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='kitchen', durable=True)
print ' [*] Waiting for orders. To exit press CTRL+C'

def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)
    time.sleep(10)
    print " [x] Done"
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos (prefetch_count=1)
channel.basic_consume (callback,
                       queue='kitchen')

channel.start_consuming()

