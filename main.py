import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


channel.exchange_declare(exchange="hospital", exchange_type='direct')

channel.queue_declare(queue='kneeQ')
channel.queue_declare(queue='hipQ')
channel.queue_declare(queue='elbowQ')


channel.queue_bind(exchange="hospital", queue="kneeQ", routing_key="knee")
channel.queue_bind(exchange="hospital", queue="hipQ", routing_key="hip")
channel.queue_bind(exchange="hospital", queue="elbowQ", routing_key="elbow")

