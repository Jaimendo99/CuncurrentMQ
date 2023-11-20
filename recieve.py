import pika
import sys
import email_api


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='topic_logs', exchange_type='topic')
result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

subs_email = sys.argv[1]

binding_keys = sys.argv[2:]
if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

for binding_key in binding_keys:
    channel.queue_bind(
        exchange='topic_logs', queue=queue_name, routing_key=binding_key)


def callback(ch, method, properties, body):
    body = body.decode('utf-8')
    subject = f"New message from {binding_key}"
    if email_api.send_email(subject, body, subs_email):
        print(" [x] Sent email")
    else:
        print(" [x] Error sending email")

    print(f" [x] Received {body}")


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
