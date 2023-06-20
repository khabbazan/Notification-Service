import sys

import pika
from message_templates import CHABOK_GROUP_WEBPUSH_MESSAGE
from message_templates import CHABOK_SINGLE_WEBPUSH_MESSAGE
from message_templates import GOOGLE_WEBPUSH_MESSAGE
from message_templates import GROUP_OTP_MESSAGE
from message_templates import SINGLE_OTP_MESSAGE

exchange = sys.argv[1] if sys.argv[1:] else "webpush"
routingKey = sys.argv[2] if sys.argv[1:] else "send.group.chabok.*"  # noqa
message = sys.argv[3] if sys.argv[2:] else CHABOK_GROUP_WEBPUSH_MESSAGE

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()


channel.exchange_declare(exchange=exchange, exchange_type="topic")
channel.basic_publish(exchange=exchange, routing_key=f"{routingKey}", body=f"{message}")


print(f" [x] Sent '{message}' message to queue")
connection.close()
