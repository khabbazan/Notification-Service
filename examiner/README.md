## Examiner Directory


This directory contains scripts and templates for testing the message publishing functionality of the microservice. The publisher.py script can be used to send messages to a specific exchange and routing key for testing purposes.


### Usage

To use the publisher.py script, first run the notif project from the root directory of the project using the following command:

```sh
    python .
```

Next, navigate to the Examiner directory:

```sh
    cd examiner
```

#### publisher.py : <br/>
To send a message to a specific exchange and routing key, use the following command with the required arguments:

```sh
    python publisher.py <exchange_name> <routing_key> <message>
```

The <exchange_name> and <routing_key> arguments are optional and will default to "webpush" and "send.google.*", respectively, if not specified. The <message> argument is also optional and will default to the GOOGLE_WEBPUSH_MESSAGE template defined in message_templates.py if not specified.


For example, to send the SINGLE_OTP_MESSAGE template to the "sms" exchange with a routing key of "send.single.otp.*", run the following command:

```sh
    python publisher.py sms send.single.otp.* '{
        "application": "MY-APP",
        "created_time": "2020-01-01 20:22:00",
        "data": {"receptor": "09101111111", "message": "hello"},
    }'

```
#### publisherRPC.py : <br/>
The publisherRPC.py script can be used to make RPC calls to microservices. It sends a request message and waits for a response message before returning a result. To use publisherRPC.py, use the following command with the required arguments:

```sh
    python publisherRPC.py <exchange_name> <routing_key> <message>
```

The <exchange_name> and <routing_key> arguments are optional and will default to "webpush" and "get.google.*", respectively, if not specified. The <message> argument is also optional and will default to the PUBLIC_VAPID_KEY template defined in message_templates.py if not specified.

For example, to send the PUBLIC_VAPID_KEY template to the "webpush" exchange with a routing key of "get.google.*", run the following command:

```sh
        python publisherRPC.py webpush get.google.* '{"application": "MY-APP", "created_time": "2020-01-01 20:22:00", "vapid_public_key": True}'

```


### Message Templates

The message_templates.py file contains predefined message templates that can be used with publisher.py for testing. The following templates are available:


- SINGLE_MESSAGE: A single message template.
- GROUP_MESSAGE: A group message template.
- SINGLE_OTP_MESSAGE: A single OTP message template.
- GROUP_OTP_MESSAGE: A group OTP message template.
- PUBLIC_VAPID_KEY: A public vapid key template.
- GOOGLE_WEBPUSH_MESSAGE: A Google Web Push message template.
- CHABOK_SINGLE_WEBPUSH_MESSAGE: A single chabok Web Push message template.
- CHABOK_GROUP_WEBPUSH_MESSAGE: A group chabok Web Push message template.
