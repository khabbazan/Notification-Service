import re
from datetime import datetime
from typing import List


def single_validation(response, *args, **kwargs):
    """
    Validate response properties.

    Args:
        response (dict): The message information.
        *args: Any additional positional arguments.
        **kwargs: Any additional keyword arguments.

    Returns:
        bool: True if the SMS message is valid, False otherwise.

    Raises:
        ValueError: If the response properties are invalid.

    Exp:
        >>> single_validation(response={"application": "app", "created_time": "2023-02-28 15:30:00",
        "data": { "receptor": "09101111111", "message": "salam"}})
        True

    """
    validation_functions = [
        {"name": validate_phone_number, "args": [response["data"]["receptor"]]},
        {"name": validate_created_time, "args": [response["created_time"]]},
    ]
    for func in validation_functions:
        func["name"](*func["args"])
    return True


def group_validation(response, *args, **kwargs):
    """
    Validate response properties.

    Args:
        response (dict): The message information.
        *args: Any additional positional arguments.
        **kwargs: Any additional keyword arguments.

    Returns:
        bool: True if the SMS message is valid, False otherwise.

    Raises:
        ValueError: If the response properties are invalid.

    Exp:
        >>> group_validation(response={"application": "app", "created_time": "2023-02-28 15:30:00",
        "data": { "receptor": ["09101111111","09101111112"], "message": "salam"}})
        True

    """
    validation_functions = [
        {"name": validate_phone_numbers, "args": [response["data"]["receptor"]]},
        {"name": validate_created_time, "args": [response["created_time"]]},
    ]
    for func in validation_functions:
        func["name"](*func["args"])
    return True


def otp_single_validation(response, *args, **kwargs):
    """
    Validate response properties.

    Args:
        response (dict): The message information.
        *args: Any additional positional arguments.
        **kwargs: Any additional keyword arguments.

    Returns:
        bool: True if the SMS message is valid, False otherwise.

    Raises:
        ValueError: If the response properties are invalid.

    Exp:
        >>> otp_single_validation(response={"application": "app", "created_time": "2023-02-28 15:30:00",
        "data": { "receptor": "09101111111", "message": "salam"}})
        True

    """
    validation_functions = [
        {"name": validate_phone_number, "args": [response["data"]["receptor"]]},
        {"name": validate_created_time, "args": [response["created_time"]]},
    ]
    for func in validation_functions:
        func["name"](*func["args"])
    return True


def otp_group_validation(response, *args, **kwargs):
    """
    Validate response properties.

    Args:
        response (dict): The message information.
        *args: Any additional positional arguments.
        **kwargs: Any additional keyword arguments.

    Returns:
        bool: True if the SMS message is valid, False otherwise.

    Raises:
        ValueError: If the response properties are invalid.

    Exp:
        >>> otp_group_validation(response={"application": "app", "created_time": "2023-02-28 15:30:00",
        "data": { "receptor": ["09101111111","09101111112"], "message": "salam"}})
        True

    """
    validation_functions = [
        {"name": validate_phone_numbers, "args": [response["data"]["receptor"]]},
        {"name": validate_created_time, "args": [response["created_time"]]},
    ]
    for func in validation_functions:
        func["name"](*func["args"])
    return True


def validate_phone_number(phonenumber: str):
    """
    Validates a phone number for an SMS message.

    Args:
        phonenumber (str): The phone number to validate. Must be a string of 11 digits, starting with '09', followed by any digit except 4, 5, 6, or 7.

    Returns:
        bool: True if the phone number is valid, False otherwise.

    Raises:
        ValueError: If the phone number is invalid.

    Exp:
        >>> validate_phone_number('09101111111')
        True

    """
    pattern = r"^09[0-3,9]\d{8}$"
    match = re.match(pattern, phonenumber)
    if not match:
        raise ValueError("Invalid phone number")
    return True


def validate_phone_numbers(phonenumbers: List[str]):
    """
    Validates a list of phone numbers for SMS messages.

    Args:
        phonenumbers: A list of phone numbers to validate. Each phone number must be a string of 11 digits,
        starting with '09', followed by any digit except 4, 5, 6, or 7.

    Returns:
        bool: True if all phone numbers are valid, False otherwise.

    Raises:
        ValueError: If any phone number is invalid.

    Expl:
        >>> validate_phone_numbers(['09101111111', '09101111112'])
        Traceback (most recent call last):
        ...
        ValueError: Invalid phone number
    """
    for phonenumber in phonenumbers:
        validate_phone_number(phonenumber=phonenumber)
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
