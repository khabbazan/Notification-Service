import json

import requests
from pywebpush import webpush
from src.core import settings
from src.resources.webpush.validators import chabok_validation
from src.resources.webpush.validators import google_validation
from src.resources.webpush.validators import vapid_key_validation


class Push:
    """
    This class is for pushing web notifications.
    """

    @classmethod
    def get_public_vapid(cls, response, *args, **kwargs):
        """
        Validates response properties.

        Args:
            response (dict): A dictionary containing the message information.
            *args: Any additional positional arguments.
            **kwargs: Any additional keyword arguments.

        Returns:
            bool: True if the respone are valid, False otherwise.

        Raises:
            ValueError: If the properties are invalid.

        """
        vapid_key_validation(response)

        return cls._get_public_vapid(*args, **kwargs)

    @classmethod
    def _get_public_vapid(cls, *args, **kwargs):
        """
        Returns the VAPID public key.

        Returns:
            str: The VAPID public key as a string.

        Raises:
            None.

        """
        return settings.VAPID_PUBLIC_KEY

    @classmethod
    def google(cls, response, *args, **kwargs):
        """
        Validates response properties and prepares to push a single notification by Google APIs.

        Args:
            response (dict): A dictionary containing the message information.
            *args: Any additional positional arguments.
            **kwargs: Any additional keyword arguments.

        Returns:
            bool: True if the notification is sent successfully, False otherwise.

        Raises:
            ValueError: If the properties are invalid.
            APIException: If there is an error with the KavenegarAPI.
            HTTPException: If there is an error with the HTTP request.

        Example:
            >>> Push.google(response={"application": "app", "created_time": "2023-02-28 15:30:00",
            ...                        "data": {"receptor": "09101111111", "message": "salam", "type": "single"}})
            True
        """
        google_validation(response=response)
        subscription_info = json.loads(response["subscription_info"])
        data = json.dumps(response["data"])
        return cls._google(subscription_info=subscription_info, data=data, *args, **kwargs)

    @classmethod
    def _google(cls, subscription_info, data, *args, **kwargs):
        """
        Sends a single push notification using the Google push notification service.

        Args:
            subscription_info (dict): A dictionary containing the subscription info for the user.
            data (str): A JSON-encoded string containing the data to be sent to the Google service.
            *args: Additional positional arguments to be ignored.
            **kwargs: Additional keyword arguments to be ignored.

        Returns:
            bool: True if the push notification is sent successfully.

        Raises:
            Exception: If the request to the Google service fails with a non-200 status code.
        """

        webpush(subscription_info=subscription_info, data=data, vapid_private_key=settings.VAPID_PRIVATE_KEY, vapid_claims=settings.VAPID_CLAIMS)

        return True

    @classmethod
    def single_chabok(cls, response, *args, **kwargs):
        """
        Validate response properties and prepare to push a single notification by Chabok APIs.

        Args:
            response (dict): A dictionary containing the response data from the Chabok service.
            *args: Additional positional arguments to be passed to `_single_chabok`.
            **kwargs: Additional keyword arguments to be passed to `_single_chabok`.

        Returns:
            bool: True if the push notification was successfully sent.

        Raises:
            Exception: If the request to the Chabok service fails with a non-200 status code.
        """
        chabok_validation(response=response)
        data = response
        return cls._single_chabok(data=data, *args, **kwargs)

    @classmethod
    def _single_chabok(cls, data, *args, **kwargs):
        """
        Sends a single push notification to a user using the Chabok push notification service.

        Args:
            data (dict): A dictionary containing the data to be sent to the Chabok service.
            *args: Additional positional arguments to be ignored.
            **kwargs: Additional keyword arguments to be ignored.

        Returns:
            bool: True if the push notification was successfully sent.

        Raises:
            Exception: If the request to the Chabok service fails with a non-200 status code.
        """

        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }

        json_data = (
            {
                "user": data["user"],
                "content": data["content"],
                "notification": {
                    "title": data["notification"]["title"],
                    "body": data["notification"]["body"],
                },
            },
        )

        req = requests.post(
            f"https://{settings.CHABOK['APP_ID']}.push.adpdigital.com/api/push/toUsers?access_token={settings.CHABOK['ACCESS_TOKEN']}",
            headers=headers,
            json=json_data,
        )

        if req.status_code == 200:
            return True
        else:
            raise Exception(f"Request failed with status code {req.status_code}")

    @classmethod
    def group_chabok(cls, response, *args, **kwargs):
        """
        Validate response properties and prepare to push a group notification by Chabok APIs.

        Args:
            response (dict): A dictionary containing the response data from the Chabok service.
            *args: Additional positional arguments to be passed to `_group_chabok`.
            **kwargs: Additional keyword arguments to be passed to `_group_chabok`.

        Returns:
            bool: True if the push notification was successfully sent.

        Raises:
            Exception: If the request to the Chabok service fails with a non-200 status code.
        """

        chabok_validation(response=response)
        data = response
        return cls._group_chabok(data=data, *args, **kwargs)

    @classmethod
    def _group_chabok(cls, data, *args, **kwargs):
        """
        Sends a group push notification to  users using the Chabok push notification service.

        Args:
            data (dict): A dictionary containing the data to be sent to the Chabok service.
            *args: Additional positional arguments to be ignored.
            **kwargs: Additional keyword arguments to be ignored.

        Returns:
            bool: True if the push notification was successfully sent.

        Raises:
            Exception: If the request to the Chabok service fails with a non-200 status code.
        """

        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }

        json_data = (
            {
                "users": data["users"],
                "content": data["content"],
                "notification": {
                    "title": data["notification"]["title"],
                    "body": data["notification"]["body"],
                },
            },
        )

        req = requests.post(
            f"https://{settings.CHABOK['APP_ID']}.push.adpdigital.com/api/push/toUsers?access_token={settings.CHABOK['ACCESS_TOKEN']}",
            headers=headers,
            json=json_data,
        )

        if req.status_code == 200:
            return True
        else:
            raise Exception(f"Request failed with status code {req.status_code}")
