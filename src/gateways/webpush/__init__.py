import inspect
import sys

from src.core.rabbitmq import RabbitMQ
from src.gateways.webpush.functions import get_public_vapid_key as get_public_vapid_key_func
from src.gateways.webpush.functions import send_google_webpush as send_google_webpush_func
from src.gateways.webpush.functions import send_group_chabok_webpush as send_group_chabok_webpush_func
from src.gateways.webpush.functions import send_single_chabok_webpush as send_single_chabok_webpush_func


def get_public_vapid_key():
    return RabbitMQ().add_callbacks(exchange_name="webpush", routing_key="get.public.vapid.*", auto_ack=True, callback=get_public_vapid_key_func)


def send_google_webpush():
    return RabbitMQ().add_callbacks(exchange_name="webpush", routing_key="send.google.*", auto_ack=True, callback=send_google_webpush_func)


def send_single_chabok_webpush():
    return RabbitMQ().add_callbacks(exchange_name="webpush", routing_key="send.single.chabok.*", auto_ack=True, callback=send_single_chabok_webpush_func)


def send_group_chabok_webpush():
    return RabbitMQ().add_callbacks(exchange_name="webpush", routing_key="send.group.chabok.*", auto_ack=True, callback=send_group_chabok_webpush_func)


def execute():
    mb = RabbitMQ()
    mb.add_exchange("webpush")

    gateways = [
        obj
        for name, obj in inspect.getmembers(sys.modules["src.gateways.webpush"])
        if (inspect.isfunction(obj) and not (name.endswith("_func") or name.endswith("execute")))
    ]

    for gateway in gateways:
        print(f"Gateway '{gateway.__name__}' is registered.")
        gateway()
