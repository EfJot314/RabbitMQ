import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


queue_name = channel.queue_declare(queue='', exclusive=True).method.queue
channel.queue_bind(exchange="hospital", queue=queue_name, routing_key="info")



#get specializations
print("Avalaible specializations: knee, elbow, hip")
print("1. ", end="")
s1 = input().strip() + "Q"
print("2. ", end="")
s2 = input().strip() + "Q"



def callback(ch, method, properties, body):
    input_val = str(body)[2:-1:].split(sep=" ")
    print("request:", input_val[1] + " -> " + input_val[0])
    result = input_val[1] + " -> " + input_val[0] + " -> done"
    channel.basic_publish(exchange='hospital', routing_key=input_val[2], body=result)
    channel.basic_publish(exchange='hospital', routing_key='log', body=result)


def info_callback(ch, method, properties, body):
    print(str(body)[2:-1:])


channel.basic_consume(queue=s1, on_message_callback=callback, auto_ack=True)
channel.basic_consume(queue=s2, on_message_callback=callback, auto_ack=True)
channel.basic_consume(queue=queue_name, on_message_callback=info_callback, auto_ack=True)

channel.start_consuming()