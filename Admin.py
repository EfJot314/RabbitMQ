import pika
import threading



connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()


#consuming
con2 = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
ch2 = con2.channel()
queue_name = ch2.queue_declare(queue='', exclusive=True).method.queue
ch2.queue_bind(exchange="hospital", queue=queue_name, routing_key="log")


def listen():
    
    def callback(ch, method, properties, body):
        result = str(body)[2:-1:]
        print()
        print(result, end="\nA > ")


    ch2.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    ch2.start_consuming()


t = threading.Thread(target=listen)
t.start()



#sending
print("==============================")
print("Send broadcast info")
print("==============================")


#main looop
while True:
    #get command
    print("A > ", end="")
    body = input().strip()

    #execute command
    if body == "x":
        break
    else:
        channel.basic_publish(exchange='hospital', routing_key='info', body=body)
    


#end connections
t.join()
connection.close()
con2.close()
