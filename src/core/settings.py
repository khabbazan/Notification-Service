import os

########## Version Settings ##########
VERSION = "1.0.2"
BUILD_NUMBER = "67a73137"

########## Kavenegar API Settings ##########
KAVEHNEGAR_API_KEY = ""
KAVEHNEGAR_DEDICATED_NUMBER = ""
KAVEHNEGAR_OTP_TEMPLATE_NAME = ""

########## Twilio API Settings ##########
TWILIO_ACCOUNT_SID = ""
TWILIO_AUTH_TOKEN = ""
TWILIO_DEDICATED_NUMBER = ""

########## Chabok API Setting ##########
CHABOK = {"APP_ID": "", "ACCESS_TOKEN": ""}


########## RabbitMQ Settings ##########
RABBITMQ_HOST = "localhost"

########## Google API Webpush Settings ##########
DER_BASE64_ENCODED_PRIVATE_KEY_FILE_PATH = os.path.join(os.getcwd(), "openssl/private.key")
DER_BASE64_ENCODED_PUBLIC_KEY_FILE_PATH = os.path.join(os.getcwd(), "openssl/public.key")
try:
    VAPID_PRIVATE_KEY = open(DER_BASE64_ENCODED_PRIVATE_KEY_FILE_PATH, "r+").readline().strip("\n")
    VAPID_PUBLIC_KEY = open(DER_BASE64_ENCODED_PUBLIC_KEY_FILE_PATH, "r+").read().strip("\n")
except FileNotFoundError:
    raise Exception("please provide openssl public/private keys.")
else:
    VAPID_CLAIMS = {"sub": "mailto:admin@fakemail.com"}
