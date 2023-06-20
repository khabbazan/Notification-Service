import sys
import uuid

import pika
from message_templates import PUBLIC_VAPID_KEY


class RpcClient(object):
    def __init__(self):  # connect to rabbitMQ server and declare new queue.
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue="", exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(queue=self.callback_queue, on_message_callback=self.on_response, auto_ack=True)

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, msg, exchange, routing_key):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(msg),
        )
        self.connection.process_data_events(time_limit=None)
        return str(self.response)


exchange = sys.argv[1] if sys.argv[1:] else "webpush"
routingKey = sys.argv[2] if sys.argv[1:] else "get.public.vapid.*"  # noqa
message = sys.argv[3] if sys.argv[2:] else PUBLIC_VAPID_KEY

client = RpcClient()
message_name = [i for i, a in locals().items() if a == PUBLIC_VAPID_KEY][0]

print(f" [x] Requesting ({message_name})")
response = client.call(message, exchange, routingKey)
print(f" [.] Got {response} ")
