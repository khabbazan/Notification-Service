import requests
from kavenegar import APIException
from kavenegar import HTTPException
from kavenegar import KavenegarAPI
from src.core import settings
from src.resources.sms.validators import group_validation
from src.resources.sms.validators import otp_group_validation
from src.resources.sms.validators import otp_single_validation
from src.resources.sms.validators import single_validation


class Send:
    """
    This class is for sending message.
    """

    @classmethod
    def single(cls, response, *args, **kwargs):
        """
        Validate response properties and prepare to send a single message.

        Args:
            response (dict): The message information.
            *args: Any additional positional arguments.
            **kwargs: Any additional keyword arguments.

        Returns:
            bool: True if the SMS message is sent successfully, False otherwise.

        Raises:
            ValueError: If the properties are invalid.
            APIException: If there is an error with the KavenegarAPI.
            HTTPException: If there is an error with the HTTP request.

        Exp:
            >>> Send.single(response={"application": "app", "created_time": "2023-02-28 15:30:00",
            "data": { "receptor": "09101111111", "message": "salam", "type": "single"}})
            True

        """
        single_validation(response=response)
        phone_nubmer = response["data"]["receptor"]
        text = response["data"]["message"]
        return cls._single(phone_number=phone_nubmer, text=text, *args, **kwargs)

    @classmethod
    def _single(cls, phone_number, text, *args, **kwargs):
        """
        Sends a single SMS message to a specified phone number with the given text message.

        Args:
            phone_number (str): The phone number to which the SMS message will be sent.
            text (str): The text message to be sent.
            *args: Any additional positional arguments.
            **kwargs: Any additional keyword arguments.

        Returns:
            bool: True if the SMS message is sent successfully, False otherwise.

        Raises:
            APIException: If there is an error with the KavenegarAPI.
            HTTPException: If there is an error with the HTTP request.

        Exp:
            >>> Send._single(phone_number="09101111111", text="Hello, world!")
            True
        """
        try:
            api = KavenegarAPI(settings.KAVEHNEGAR_API_KEY)

            params = {
                "sender": settings.DEDICATED_NUMBER,
                "receptor": phone_number,
                "message": text,
            }
            api.sms_send(params)
        except APIException as e:
            raise Exception(e)
        except HTTPException as e:
            raise Exception(e)
        return True

    @classmethod
    def group(cls, response, *args, **kwargs):
        """
        Validate response properties and prepare to send group messages.

        Args:
            response (dict): The message information.
            *args: Any additional positional arguments.
            **kwargs: Any additional keyword arguments.

        Returns:
            bool: True if the SMS message is sent successfully, False otherwise.

        Raises:
            ValueError: If the properties are invalid.
            APIException: If there is an error with the KavenegarAPI.
            HTTPException: If there is an error with the HTTP request.

        Example:
            >>> Send.group(response={"application": "app", "created_time": "2023-02-28 15:30:00",
            "data": { "receptor": ["09101111111", "09101111112"], "message": "Hello, world!", "type": "group"}})
            True
        """

        group_validation(response=response)

        phone_nubmers = response["data"]["receptor"]
        text = response["data"]["message"]
        return cls._group(phone_numbers=phone_nubmers, text=text, *args, **kwargs)

    @classmethod
    def _group(cls, phone_numbers, text, *args, **kwargs):
        """
        Sends a group SMS message to a list of specified phone numbers with the given text message.

        Args:
            phone_numbers (list): A list of phone numbers to which the SMS message will be sent.
            text (str): The text message to be sent.
            *args: Any additional positional arguments.
            **kwargs: Any additional keyword arguments.

        Returns:
            bool: True if the SMS message is sent successfully, False otherwise.

        Raises:
            APIException: If there is an error with the KavenegarAPI.
            HTTPException: If there is an error with the HTTP request.

        Example:
            >>> Send._group(phone_numbers=["09101111111", "09101111112"], text="Hello world")
            True
        """
        try:
            api = KavenegarAPI(settings.KAVEHNEGAR_API_KEY)
            params = {"sender": settings.DEDICATED_NUMBER, "receptor": phone_numbers, "message": [text] * len(phone_numbers)}
            api.sms_sendarray(params)
        except APIException as e:
            raise Exception(e)
        except HTTPException as e:
            raise Exception(e)
        return True

    @classmethod
    def single_otp(cls, response, *args, **kwargs):
        """
        Validate response properties and prepare to send a otp message.

        Args:
            response (dict): The message information.
            *args: Any additional positional arguments.
            **kwargs: Any additional keyword arguments.

        Returns:
            bool: True if the SMS message is sent successfully, False otherwise.

        Raises:
            ValueError: If the properties are invalid.
            APIException: If there is an error with the KavenegarAPI.
            HTTPException: If there is an error with the HTTP request.

        Exp:
            >>> Send.single_otp(response={"application": "app", "created_time": "2023-02-28 15:30:00",
            "data": { "receptor": "09101111111", "message": "42351", "type": "otp"}})
            True

        """
        otp_single_validation(response=response)
        phone_nubmer = response["data"]["receptor"]
        text = response["data"]["message"]
        return cls._single_otp(phone_number=phone_nubmer, text=text, *args, **kwargs)

    @classmethod
    def _single_otp(cls, phone_number, text, *args, **kwargs):
        """
        Sends a otp SMS message to a specified phone number with the given a otp message.

        Args:
            phone_number (str): The phone number to which the SMS message will be sent.
            text (str): The text message to be sent.
            *args: Any additional positional arguments.
            **kwargs: Any additional keyword arguments.

        Returns:
            bool: True if the SMS message is sent successfully, False otherwise.

        Raises:
            APIException: If there is an error with the KavenegarAPI.
            HTTPException: If there is an error with the HTTP request.

        Exp:
            >>> Send._single_otp(phone_number="09101111111", text="5438")
            True
        """
        try:
            api = KavenegarAPI(settings.KAVEHNEGAR_API_KEY)
            params = {"receptor": phone_number, "token": text, "template": "test"}
            api.verify_lookup(params)
        except APIException as e:
            raise Exception(e)
        except HTTPException as e:
            raise Exception(e)
        return True

    @classmethod
    def group_otp(cls, response, *args, **kwargs):
        """
        Validate response properties and prepare to send group otp message.

        Args:
            response (dict): The message information.
            *args: Any additional positional arguments.
            **kwargs: Any additional keyword arguments.

        Returns:
            bool: True if the SMS message is sent successfully, False otherwise.

        Raises:
            ValueError: If the properties are invalid.
            APIException: If there is an error with the KavenegarAPI.
            HTTPException: If there is an error with the HTTP request.

        Example:
            >>> Send.group_otp(response={"application": "app", "created_time": "2023-02-28 15:30:00",
            "data": { "receptor": ["09101111111", "09101111112"], "message": ["32423","45379"], "type": "group_otp"}})
            True
        """
        otp_group_validation(response=response)
        phone_nubmers = response["data"]["receptor"]
        texts = response["data"]["message"]
        return cls._group_otp(phone_numbers=phone_nubmers, texts=texts, *args, **kwargs)

    @classmethod
    def _group_otp(cls, phone_numbers, texts, *args, **kwargs):
        """
        Sends a group otp SMS message to a list of specified phone numbers with the given otp messages.

        Args:
            phone_numbers (list): A list of phone numbers to which the SMS message will be sent.
            texts (list): A list of otp messages to be sent.
            *args: Any additional positional arguments.
            **kwargs: Any additional keyword arguments.

        Returns:
            bool: True if the SMS message is sent successfully, False otherwise.

        Raises:
            APIException: If there is an error with the KavenegarAPI.
            HTTPException: If there is an error with the HTTP request.

        Example:
            >>> Send._group_otp(phone_numbers=["09101111111", "09101111112"], texts=["7589", "1234"])
            True
        """
        try:
            api = KavenegarAPI(settings.KAVEHNEGAR_API_KEY)
            for phone_number, text in zip(phone_numbers, texts):
                params = {"receptor": phone_number, "token": text, "template": "test"}
                api.verify_lookup(params)
        except APIException as e:
            raise Exception(e)
        except HTTPException as e:
            raise Exception(e)
        return True
