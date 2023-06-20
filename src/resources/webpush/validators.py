import json
from datetime import datetime


def vapid_key_validation(response, *args, **kwargs):

    validation_functions = [
        {"name": validate_created_time, "args": [response["created_time"]]},
    ]
    for func in validation_functions:
        func["name"](*func["args"])

    return True


def google_validation(response, *args, **kwargs):
    """
    Validates the properties of a Google Cloud Messaging response.

    Args:
        response (dict): A dictionary containing the response properties.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.

    Returns:
        bool: True if the GCM response is valid, False otherwise.

    Raises:
        ValueError: If the response properties are invalid.

    Example:
    {
        "application": "MY-APP",
        "created_time": "2020-01-01 20:22:00",
        "subscription_info": ... ,
        "data": {
            "title": "MY-APP PUSH",
            "body": "my push notification",
            "icon": "https://www.pngfind.com/pngs/b/168-1682511_notification-icon-png.png",
            "badge": "https://www.pngfind.com/pngs/b/168-1682511_notification-icon-png.png",
        },
    }
        >>> google_validation(response)
        True
    """

    validation_functions = [
        {"name": validate_google_subscription_info, "args": [response["subscription_info"]]},
        {"name": validate_created_time, "args": [response["created_time"]]},
    ]
    for func in validation_functions:
        func["name"](*func["args"])
    return True


def chabok_validation(response, *args, **kwargs):
    """
    Validates the properties of a Chabok notification request.

    Args:
        response: A dictionary object containing data related to a notification.
        *args: Additional positional arguments to pass to the validation functions.
        **kwargs: Additional keyword arguments to pass to the validation functions.

    Returns:
        A boolean value indicating whether all validation functions passed without raising an exception.

    Raises:
        Exception: If any of the validation functions fail to validate the data in `response`.

    Example:
        response = {
            "application": "MY-APP",
            "created_time": "2020-01-01 20:22:00",
            'user': "mehrshad",
            'content': "test notif in app with examiner",
            'notification': {
                'title': "MY-APP chabok push",
                'body': "push notif by notif app",
            }
        }
        >>> chabok_validation(response)
        True
    """
    validation_functions = [
        {"name": validate_created_time, "args": [response["created_time"]]},
    ]
    for func in validation_functions:
        func["name"](*func["args"])
    return True


def validate_google_subscription_info(subscription_info):
    """
    Validates a subscription info dictionary for a Google push notification.

    Args:
        subscription_info (str): A JSON-encoded string representing the subscription info dictionary.

    Returns:
        bool: True if the subscription info dictionary is valid, False otherwise.

    Raises:
        Exception: If the subscription info dictionary is invalid.

    Example:
        subscription_info = '{"endpoint": "https://fcm.googleapis.com/fcm/send/cXNtMTZfYz...","expirationTime": null,"keys": {"p256dh": "...", "auth": "..."}}'
        validate_google_subscription_info(subscription_info)
    """

    try:
        subscription_dict = json.loads(subscription_info)
        subscription_dict["expirationTime"] = "" if subscription_dict["expirationTime"] is None else subscription_dict["expirationTime"]

    except json.decoder.JSONDecodeError:
        raise Exception("subscription info can't be decode to dictionary")

    else:
        for key, value_type in {"endpoint": str, "expirationTime": str, "keys": dict}.items():
            if key not in subscription_dict.keys():
                raise Exception("subscription info doesn't have sufficient properties")
            if not isinstance(subscription_dict[key], value_type):
                raise Exception(f"subscription info doesn't have match property datatype, `{key}`")

    return True


def validate_created_time(created_time):
    """
    Validates a creation time for an SMS message.

    Args:
        created_time (str): The creation time to validate, in the format "%Y-%m-%d %H:%M:%S".

    Returns:
        bool: True if the creation time is valid, False otherwise.

    Raises:
        ValueError: If the creation time is invalid.

    Exp:
        >>> validate_created_time('2023-04-11 12:00:00')
        True

    """
    datetime_format = "%Y-%m-%d %H:%M:%S"
    try:
        datetime.strptime(created_time, datetime_format)

    except ValueError:
        raise ValueError("Invalid date time")
    else:
        return True
