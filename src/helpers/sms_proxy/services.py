from abc import ABC
from abc import abstractmethod

from kavenegar import KavenegarAPI
from src.core import settings
from twilio.rest import Client


class MessagingService(ABC):
    """Abstract base class for messaging services.

    This abstract base class defines the interface for messaging services, including methods for sending single messages,
    OTP (One-Time Password) messages, and group messages. Subclasses must implement these methods.

    Methods:
        send_single_message(self, recipient, message):
            Send a single message to a recipient.

        send_otp_message(self, recipient, otp_code):
            Send an OTP (One-Time Password) message to a recipient.

        send_group_message(self, recipients, message):
            Send a group message to a list of recipients.
    """

    @abstractmethod
    def send_single_message(self, recipient, message):
        """Send a single message to a recipient.

        Args:
            recipient (str): The recipient's phone number.
            message (str): The message content to be sent.
        """

    @abstractmethod
    def send_otp_message(self, recipient, otp_code):
        """Send an OTP (One-Time Password) message to a recipient.

        Args:
            recipient (str): The recipient's phone number.
            otp_code (str): The OTP code to be sent.
        """

    @abstractmethod
    def send_group_message(self, recipients, message):
        """Send a group message to a list of recipients.

        Args:
            recipients (list): A list of recipient phone numbers.
            message (str): The message content to be sent to all recipients.
        """


class KavenegarService(MessagingService):
    """Messaging service using Kavenegar API for sending SMS messages.

    This class implements the methods required by the `MessagingService` abstract base class to send SMS messages using the
    Kavenegar API.
    """

    def __init__(self, api_key):

        self.kavenegar_api = KavenegarAPI(api_key)

    def send_single_message(self, recipient, message):
        """Send a single SMS message using the Kavenegar service.

        Args:
            recipient (str): The recipient's phone number.
            message (str): The message content to be sent.

        Returns:
            bool: True if the message was successfully sent, False otherwise.
        """

        params = {
            "sender": settings.KAVEHNEGAR_DEDICATED_NUMBER,
            "receptor": recipient,
            "message": message,
        }
        try:
            if self.kavenegar_api is not None:
                self.kavenegar_api.sms_send(params)
        except Exception as e:
            raise Exception(f"Kavenegar: Error sending single message: {e}")

        return True

    def send_otp_message(self, recipient, otp_code):
        """Send an OTP (One-Time Password) SMS message using the Kavenegar service.

        Args:
            recipient (str): The recipient's phone number.
            otp_code (str): The OTP code to be sent.

        Returns:
            bool: True if the OTP message was successfully sent, False otherwise.
        """

        params = {
            "receptor": recipient,
            "token": otp_code,
            "template": settings.KAVEHNEGAR_OTP_TEMPLATE_NAME,
        }
        try:
            self.kavenegar_api.verify_lookup(params)
        except Exception as e:
            raise Exception(f"Kavenegar: Error sending OTP message: {e}")

        return True

    def send_group_message(self, recipients, message):
        """Send a group SMS message using the Kavenegar service.

        Args:
            recipients (list): A list of recipient phone numbers.
            message (str): The message content to be sent to all recipients.

        Returns:
            bool: True if the group message was successfully sent, False otherwise.
        """

        params = {
            "sender": settings.KAVEHNEGAR_DEDICATED_NUMBER,
            "receptor": recipients,
            "message": [message] * len(recipients),
        }
        try:
            self.kavenegar_api.sms_sendarray(params)
        except Exception as e:
            raise Exception(f"Kavenegar: Error sending group messages: {e}")

        return True


class TwilioService(MessagingService):
    """Messaging service using Twilio for sending SMS messages.

    This class implements the methods required by the `MessagingService` abstract base class to send SMS messages using the
    Twilio service.
    """

    def __init__(self, account_sid, auth_token):

        self.twilio_client = Client(account_sid, auth_token)

    def send_single_message(self, recipient, message):
        """Send a single SMS message using the Twilio service.

        Args:
            recipient (str): The recipient's phone number.
            message (str): The message content to be sent.

        Returns:
            bool: True if the message was successfully sent, False otherwise.
        """

        params = {
            "body": message,
            "from_": settings.TWILIO_DEDICATED_NUMBER,
            "to": recipient,
        }
        try:
            self.twilio_client.messages.create(**params)
        except Exception as e:
            raise Exception(f"Twilio: Error sending single message: {e}")

        return True

    def send_otp_message(self, recipient, otp_code):
        """Send an OTP (One-Time Password) SMS message using the Twilio service.

        Args:
            recipient (str): The recipient's phone number.
            otp_code (str): The OTP code to be sent.

        Returns:
            bool: True if the OTP message was successfully sent, False otherwise.
        """

        params = {
            "body": f"Your OTP code is: {otp_code}",
            "from_": settings.TWILIO_DEDICATED_NUMBER,
            "to": recipient,
        }
        try:
            self.twilio_client.messages.create(**params)
        except Exception as e:
            raise Exception(f"Twilio: Error sending OTP message: {e}")

        return True

    def send_group_message(self, recipients, message):
        """Send a group SMS message using the Twilio service.

        Args:
            recipients (list): A list of recipient phone numbers.
            message (str): The message content to be sent to all recipients.

        Returns:
            bool: True if the group message was successfully sent, False otherwise.
        """

        try:
            for recipient in recipients:
                params = {
                    "body": message,
                    "from_": settings.TWILIO_DEDICATED_NUMBER,
                    "to": recipient,
                }
                self.twilio_client.messages.create(**params)

        except Exception as e:
            raise Exception(f"Twilio: Error sending group message: {e}")

        return True
