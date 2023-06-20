import json
from enum import Enum


class Jsonify:
    """
    This class is for converting input data to Dictionary or JSON format according to specified templates.
    """

    class SMSJType(Enum):
        """
        An enumeration of different sms data types.
        """

        SINGLE = {"application": str, "created_time": str, "data": dict, "data.receptor": str, "data.message": str}
        GROUP = {"application": str, "created_time": str, "data": dict, "data.receptor": list, "data.message": str}
        SINGLE_OTP = {"application": str, "created_time": str, "data": dict, "data.receptor": str, "data.message": str}
        GROUP_OTP = {"application": str, "created_time": str, "data": dict, "data.receptor": list, "data.message": list}

    class WebPushJType(Enum):
        """
        An enumeration of different webpush data types.
        """

        VAPID_KEY = {"application": str, "created_time": str, "vapid_public_key": bool}

        GOOGLE = {
            "application": str,
            "created_time": str,
            "subscription_info": str,
            "data": dict,
            "data.title": str,
            "data.body": str,
            "data.icon": str,
            "data.badge": str,
        }

        SINGLE_CHABOK = {
            "application": str,
            "created_time": str,
            "user": str,
            "content": str,  # representation to the admin user in the Chabok push notification panel
            "notification": dict,
            "notification.title": str,
            "notification.body": str,
        }

        GROUP_CHABOK = {
            "application": str,
            "created_time": str,
            "users": list,
            "content": str,
            "notification": dict,
            "notification.title": str,
            "notification.body": str,
        }

    @staticmethod
    def json(data, template: Enum):
        """
        Converts a python dictionary to a JSON-formatted string, validating the data against the specified template.

        Args:
            data (dict): A Python dictionary containing the data to be converted to JSON format.
            template (Enum): An enumeration specifying the expected data types and structure of the JSON data.

        Raises:
            ValueError: If the input data does not match the specified template.

        Returns:
            str: A string representing the input data in JSON format.
        """
        if JsonParser.is_dict(data, exception=True):
            if not JsonParser.check_attribute(data=data, template=template):
                raise ValueError("Input data does not match the specified template")
        return json.dumps(data)

    @staticmethod
    def dict(data, template: Enum):  # noqa: A003
        """
        Converts a JSON-formatted string to a Python dictionary, validating the data against the specified template.

        Args:
            data (str): A string representing the data in JSON format.
            template (Enum): An enumeration specifying the expected data types and structure of the JSON data.

        Raises:
            ValueError: If the input data does not match the specified template.

        Returns:
            dict: A python dictionary containing the input data.
        """
        if JsonParser.is_json(data, exception=True):
            data = json.loads(data)
            if not JsonParser.check_attribute(data=data, template=template):
                raise ValueError("Input data does not match the specified template")
        return dict(data)


class JsonParser:
    """
    The parser class for input data.
    """

    @staticmethod
    def is_dict(data, exception=False):
        """
        Checks if the input data is a python dictionary.

        Args:
            data (dict): The data to check.
            exception (bool, optional): Whether to raise a ValueError if the data is not a dictionary. Defaults to False.

        Returns:
            bool: True if the data is a dictionary, False otherwise.

        Raises:
            ValueError: If the input data is not dictionary.
        """
        if isinstance(data, dict):
            return True
        elif exception:
            raise ValueError("Input data is not a dictionary")
        else:
            return False

    @staticmethod
    def is_json(data, exception=False):
        """
        Checks if the input data is a valid JSON-formatted string.

        Args:
            data (str): The string to check.
            exception (bool, optional): Whether to raise a TypeError if the data is not a valid JSON string. Defaults to False.

        Returns:
            bool: True if the string is a valid JSON string, False otherwise.

        Raises:
            ValueError: If the input data is not json str.
        """
        try:
            json.loads(data)
        except ValueError:
            if exception:
                raise TypeError("Input data must be a json str")
            return False
        return True

    @staticmethod
    def check_attribute(data, template: Enum):
        """
        Checks if the data matches the specified template.

        Args:
            data (dict): The data to check.
            template (Enum): The template specifying the expected data types and structure of the data.

        Returns:
            bool: True if the data matches the template, False otherwise.

        Raises:
            TypeError: If the template is not match.
        """
        # trim data
        trimmed_data = {}
        for data_key, data_value in data.items():
            if not isinstance(data[data_key], dict):
                trimmed_data[data_key] = data_value
            else:
                # when data_key is dictionary
                trimmed_data[data_key] = {}
                for key, value in data[data_key].items():
                    trimmed_data[f"{data_key}.{key}"] = value

        # template matching
        try:
            for trimmed_data_key, template_key in zip(trimmed_data.keys(), template.value.keys()):
                if not ((trimmed_data_key == template_key) and isinstance(trimmed_data[trimmed_data_key], template.value[template_key])):
                    raise TypeError("Template not match.")
        except TypeError:
            return False
        else:
            return True
