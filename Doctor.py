import pika
import threading



connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()


#consuming
con2 = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
ch2 = con2.channel()
queue_name = ch2.queue_declare(queue='', exclusive=True).method.queue
ch2.queue_bind(exchange="hospital", queue=queue_name, routing_key="info")
ch2.queue_bind(exchange="hospital", queue=queue_name, routing_key=queue_name)


def listen():
    
    def callback(ch, method, properties, body):
        result = str(body)[2:-1:]
        print()
        print(result, end="\nD > ")


    ch2.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    ch2.start_consuming()


t = threading.Thread(target=listen)
t.start()



#sending
print("==============================")
print("Command format:")
print("command_type last_name")
print("==============================")


#main looop
while True:
    #get command
    print("D > ", end="")
    command = input().strip()
    input_val = command.split(sep=" ")

    body = command+" "+queue_name

    #execute command
    if input_val[0] == "x":
        break
    elif input_val[0] == "knee":
        channel.basic_publish(exchange='hospital', routing_key='knee', body=body)
        channel.basic_publish(exchange='hospital', routing_key='log', body=body)
    elif input_val[0] == "elbow":
        channel.basic_publish(exchange='hospital', routing_key='elbow', body=body)
        channel.basic_publish(exchange='hospital', routing_key='log', body=body)
    elif input_val[0] == "hip":
        channel.basic_publish(exchange='hospital', routing_key='hip', body=body)
        channel.basic_publish(exchange='hospital', routing_key='log', body=body)
    else:
        print(f"Type '{input_val[0]}' is not implemented!")
    


#end connections
t.join()
connection.close()
con2.close()
