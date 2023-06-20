import inspect
import sys

from src.core.rabbitmq import RabbitMQ
from src.gateways.sms.functions import send_group_messages as send_group_messages_func
from src.gateways.sms.functions import send_group_otp as send_group_otp_func
from src.gateways.sms.functions import send_single_message as send_single_message_func
from src.gateways.sms.functions import send_single_otp as send_single_otp_func


def send_single_message():
    return RabbitMQ().add_callbacks(exchange_name="sms", routing_key="send.single.*", auto_ack=True, callback=send_single_message_func)


def send_group_messages():
    return RabbitMQ().add_callbacks(exchange_name="sms", routing_key="send.group.*", auto_ack=True, callback=send_group_messages_func)


def send_single_otp():
    return RabbitMQ().add_callbacks(exchange_name="sms", routing_key="send.single.otp.*", auto_ack=False, callback=send_single_otp_func)


def send_group_otp():
    return RabbitMQ().add_callbacks(exchange_name="sms", routing_key="send.group.otp.*", auto_ack=False, callback=send_group_otp_func)


def execute():
    mb = RabbitMQ()
    mb.add_exchange("sms")

    gateways = [
        obj for name, obj in inspect.getmembers(sys.modules["src.gateways.sms"]) if (inspect.isfunction(obj) and not (name.endswith("_func") or name.endswith("execute")))
    ]

    for gateway in gateways:
        print(f"Gateway '{gateway.__name__}' is registered.")
        gateway()
