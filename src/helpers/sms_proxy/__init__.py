from src.core import settings
from src.helpers.sms_proxy.services import KavenegarService
from src.helpers.sms_proxy.services import MessagingService
from src.helpers.sms_proxy.services import TwilioService


class SMSServiceProxy(MessagingService):
    """A proxy service for sending SMS messages using Kavenegar or Twilio based on the recipient's phone number prefix.

    This class extends `MessagingService` and is designed to send SMS messages using either the Kavenegar or Twilio service
    based on the recipient's phone number prefix (e.g., +98 for Iranian phone numbers). It contains methods for sending single
    messages, OTP messages, and group messages.

    Methods:
        send_single_message(recipient, message):
            Sends a single SMS message to the specified recipient.

        send_otp_message(recipient, otp_code):
            Sends an OTP (One-Time Password) SMS message to the specified recipient.

        send_group_message(recipients, message):
            Sends a group SMS message to a list of recipients.

    """

    def __init__(self):
        self.kavenegar_service = KavenegarService(settings.KAVEHNEGAR_API_KEY)
        self.twilio_service = TwilioService(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    def send_single_message(self, recipient, message):
        """Send a single SMS message to the specified recipient.

        Args:
            recipient (str): The recipient's phone number.
            message (str): The message content to be sent.

        Returns:
            bool: True if the message was successfully sent, False otherwise.
        """
        if recipient.startswith("+98"):  # Iranian phone numbers
            self.kavenegar_service.send_single_message(recipient, message)
        else:
            self.twilio_service.send_single_message(recipient, message)
        return True

    def send_otp_message(self, recipient, otp_code):
        """Send an OTP (One-Time Password) SMS message to the specified recipient.

        Args:
            recipient (str): The recipient's phone number.
            otp_code (str): The OTP code to be sent.

        Returns:
            bool: True if the OTP message was successfully sent, False otherwise.
        """
        if recipient.startswith("+98"):  # Iranian phone numbers
            self.kavenegar_service.send_otp_message(recipient, otp_code)
        else:
            self.twilio_service.send_otp_message(recipient, otp_code)
        return True

    def send_group_message(self, recipients, message):
        """Send a group SMS message to a list of recipients.

        Args:
            recipients (list): A list of recipient phone numbers.
            message (str): The message content to be sent to all recipients.

        Returns:
            bool: True if the group message was successfully sent, False otherwise.
        """
        if all("+98" in recipient for recipient in recipients):  # Iranian phone numbers
            self.kavenegar_service.send_group_message(recipients, message)
        else:
            self.twilio_service.send_group_message(recipients, message)
        return True
