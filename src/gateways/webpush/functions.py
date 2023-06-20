from src.core import settings
from src.core.rabbitmq import RabbitMQ
from src.helpers.json_parser import Jsonify
from src.helpers.messages import get_message
from src.resources.webpush import Push


def get_public_vapid_key(channel, method, properties, body):
    """
    Receive data from 'webpush' exchange with the `get.public.vapid.*` exchange.

    Args:
        channel: The channel used for communication with RabbitMQ.
        method: The method used to deliver the message.
        properties: The message properties.
        body: The message body.

    Returns:
        A response from RabbitMQ containing an acknowledgement and a message indicating success or failure.

    Raises:
        ValueError: If the input data does not match the specified template and the subscription_info is invalid.

    """

    response = Jsonify.dict(body.decode(), Jsonify.WebPushJType.VAPID_KEY)

    public_vapid_key = Push.get_public_vapid(response=response)
    if public_vapid_key:
        msg = get_message("get_public_vapid_key", **{"app": response["application"]})
    else:
        msg = get_message("failed_get_public_vapid_key", **{"app": response["application"]})

    rpc_metadata = {
        "rpc_msg": public_vapid_key,
        "rpc_exchange": "",
        "rpc_reply_to": properties.reply_to,
        "rpc_correlation_id": properties.correlation_id,
    }

    return RabbitMQ().response(ack=method.delivery_tag, msg_to_console=msg, rpc=True, **rpc_metadata)


def send_google_webpush(channel, method, properties, body):
    """
    Receive data from 'webpush' exchange with the `send.google.*` exchange.

    Args:
        channel: The channel used for communication with RabbitMQ.
        method: The method used to deliver the message.
        properties: The message properties.
        body: The message body.

    Returns:
        A response from RabbitMQ containing an acknowledgement and a message indicating success or failure.

    Raises:
        ValueError: If the input data does not match the specified template and the subscription_info is invalid.

    """

    response = Jsonify.dict(body.decode(), Jsonify.WebPushJType.GOOGLE)

    if Push.google(response=response):
        msg = get_message("send_google_webpush", **{"subscription_info": response["subscription_info"]})
    else:
        msg = get_message("failed_send_google_webpush", **{"subscription_info": response["subscription_info"]})

    return RabbitMQ().response(ack=method.delivery_tag, msg_to_console=msg)


def send_single_chabok_webpush(channel, method, properties, body):
    """
    Receive data from 'webpush' exchange with the `send.single.chabok.*` exchange.

    Args:
        channel: The channel used for communication with RabbitMQ.
        method: The method used to deliver the message.
        properties: The message properties.
        body: The message body.

    Returns:
        A response from RabbitMQ containing an acknowledgement and a message indicating success or failure.

    Raises:
        ValueError: If the input data does not match the specified template and the user or creation time is invalid.
    """

    response = Jsonify.dict(body.decode(), Jsonify.WebPushJType.SINGLE_CHABOK)

    if Push.single_chabok(response=response):
        msg = get_message("send_single_chabok_webpush", **{"user": response["user"]})
    else:
        msg = get_message("failed_single_chabok_webpush", **{"user": response["user"]})

    return RabbitMQ().response(ack=method.delivery_tag, msg_to_console=msg)


def send_group_chabok_webpush(channel, method, properties, body):
    """
    Receive data from 'webpush' exchange with the `send.group.chabok.*` exchange.

    Args:
        channel: The channel used for communication with RabbitMQ.
        method: The method used to deliver the message.
        properties: The message properties.
        body: The message body.

    Returns:
        A response from RabbitMQ containing an acknowledgement and a message indicating success or failure.

    Raises:
        ValueError: If the input data does not match the specified template and the user or creation time is invalid.
    """

    response = Jsonify.dict(body.decode(), Jsonify.WebPushJType.GROUP_CHABOK)
    users = ", ".join(response["users"])

    if Push.group_chabok(response=response):
        msg = get_message("send_group_chabok_webpush", **{"users": users})
    else:
        msg = get_message("failed_group_chabok_webpush", **{"users": users})

    return RabbitMQ().response(ack=method.delivery_tag, msg_to_console=msg)
