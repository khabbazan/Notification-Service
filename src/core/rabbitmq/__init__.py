import pika
from src.core import settings


class RabbitMQ:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(RabbitMQ, cls).__new__(cls)
            cls.instance._exchanges = []
            cls.instance._connect()
        return cls.instance

    def _connect(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(settings.RABBITMQ_HOST))
        self.channel = self.connection.channel()
        return True

    def add_exchange(self, exchange_name):
        self.get_exchange(exchange_name, exist_exception=True)
        obj = Exchange(self.channel, exchange_name)
        self._exchanges.append(obj)
        return True

    def get_exchange(self, exchange_name, notfound_exception=False, exist_exception=False):
        for exchange in self._exchanges:
            if exchange.name == exchange_name:
                if exist_exception:
                    raise Exception("Exchange exist")
                else:
                    return exchange
        if notfound_exception:
            raise Exception("Exchange not found.")

    def add_callbacks(self, exchange_name, routing_key, auto_ack, **callbacks):
        exchange = self.get_exchange(exchange_name, notfound_exception=True)
        exchange.bind(routing_key, auto_ack, **callbacks)
        return True

    def response(self, ack=None, msg_to_console=None, msg_to_log=None, rpc=None, rpc_msg=None, rpc_exchange=None, rpc_reply_to=None, rpc_correlation_id=None):

        if rpc is not None:
            if not all([rpc, rpc_msg, rpc_reply_to, rpc_correlation_id]):
                raise ValueError("rpc metadata include {`rpc_msg`, `rpc_correlation_id`, `rpc_replay_to`, `rpc_exchange` are not mentioned}")

            self.channel.basic_publish(
                exchange=rpc_exchange,
                routing_key=rpc_reply_to,
                properties=pika.BasicProperties(correlation_id=rpc_correlation_id),
                body=rpc_msg,
            )

        if ack is not None:
            self.channel.basic_ack(delivery_tag=ack)

        if msg_to_console is not None:
            print(msg_to_console)

    def start(self):
        print("[*] Waiting for messages. To exit press CTRL+C")
        self.channel.start_consuming()

    def reset_channel(self):
        print("[*] Waiting for reset channel.")
        if not self.channel.is_open:
            self.channel = self.connection.channel()

        self._exchanges = []
        print("[*] Channel reset successfully.")
        return True


class Exchange:
    def __init__(self, channel, name):
        self.bind_queue = None
        self.channel = channel
        self.name = name
        self.channel.exchange_declare(exchange=self.name, exchange_type="topic")

    def bind(self, routing_key, auto_ack, **callbacks):
        result = self.channel.queue_declare(queue="", exclusive=True)
        self.bind_queue = result.method.queue
        self.channel.queue_bind(exchange=self.name, queue=self.bind_queue, routing_key=routing_key)

        for _, callback in callbacks.items():
            self.channel.basic_consume(queue=self.bind_queue, auto_ack=auto_ack, on_message_callback=callback)
        return True
