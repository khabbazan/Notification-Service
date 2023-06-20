from src.core.rabbitmq import RabbitMQ
from src.helpers.json_parser import Jsonify
from src.helpers.messages import get_message
from src.resources.sms import Send


def send_single_message(channel, method, properties, body):
    """
    Receive data from 'sms' exchange with the `send.single.*` routing key.

    Args:
        channel: The channel used for communication with RabbitMQ.
        method: The method used to deliver the message.
        properties: The message properties.
        body: The message body.

    Returns:
        A response from RabbitMQ containing an acknowledgement and a message indicating success or failure.

    Raises:
        ValueError: If the input data does not match the specified template and the phone number or creation time is invalid.

    """

    response = Jsonify.dict(body.decode(), Jsonify.SMSJType.SINGLE)

    if Send.single(response=response):
        msg = get_message("send_single_message", **{"receptor": response["data"]["receptor"]})
    else:
        msg = get_message("failed_send_single_message", **{"receptor": response["data"]["receptor"]})

    return RabbitMQ().response(ack=method.delivery_tag, msg_to_console=msg)


def send_group_messages(channel, method, properties, body):
    """
    Receive data from 'sms' exchange with the `send.group.*` routing key.

    Args:
        channel: The channel used for communication with RabbitMQ.
        method: The method used to deliver the message.
        properties: The message properties.
        body: The message body.

    Returns:
        A response from RabbitMQ containing an acknowledgement and a message indicating success or failure.

    Raises:
        ValueError: If the input data does not match the specified template and the phone number or creation time is invalid.

    """
    response = Jsonify.dict(body.decode(), Jsonify.SMSJType.GROUP)

    if Send.group(response=response):
        msg = get_message("send_group_message", **{"receptor": ", ".join(response["data"]["receptor"])})
    else:
        msg = get_message("failed_send_group_message", **{"receptor": ", ".join(response["data"]["receptor"])})

    return RabbitMQ().response(ack=method.delivery_tag, msg_to_console=msg)


def send_single_otp(channel, method, properties, body):
    """
    Receive data from 'sms' exchange with the `send.single.otp.*` routing key.

    Args:
        channel: The channel used for communication with RabbitMQ.
        method: The method used to deliver the message.
        properties: The message properties.
        body: The message body.

    Returns:
        A response from RabbitMQ containing an acknowledgement and a message indicating success or failure.

    Raises:
        ValueError: If the input data does not match the specified template and the phone number or creation time is invalid.

    """
    response = Jsonify.dict(body.decode(), Jsonify.SMSJType.SINGLE_OTP)

    if Send.single_otp(response=response):
        msg = get_message("send_single_otp_message", **{"receptor": response["data"]["receptor"]})
    else:
        msg = get_message("failed_send_single_otp_message", **{"receptor": response["data"]["receptor"]})

    return RabbitMQ().response(ack=method.delivery_tag, msg_to_console=msg)


def send_group_otp(channel, method, properties, body):
    response = Jsonify.dict(body.decode(), Jsonify.SMSJType.GROUP_OTP)

    if Send.group_otp(response=response):
        msg = get_message("send_group_otp_message", **{"receptor": ", ".join(response["data"]["receptor"])})
    else:
        msg = get_message("failed_send_group_otp_message", **{"receptor": ", ".join(response["data"]["receptor"])})

    return RabbitMQ().response(ack=method.delivery_tag, msg_to_console=msg)
