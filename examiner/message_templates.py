import json

PUBLIC_VAPID_KEY = json.dumps({"application": "MY-APP", "created_time": "2020-01-01 20:22:00", "vapid_public_key": True})


GOOGLE_WEBPUSH_MESSAGE = json.dumps(
    {
        "application": "MY-APP",
        "created_time": "2020-01-01 20:22:00",
        "subscription_info": '{"endpoint":"https://fcm.googleapis.com/fcm/send/fzSRCOGWEns:APA91bH78MuDr1pnxHsukzlN415_D6CdwPXohueC-OpYZl-ViThup9rClcA7ac3hOswIwC0laYbpTbbbxeFLtFfcpLX0cT_bIN6h7t6Y8Ia3m3d-uvDDqO27Z0MfYFgcP0A_FC-3_zA2","expirationTime":null,"keys":{"p256dh":"BOiZ9aq-ABL79Wtno9hr4RnqKLztKWISVN7vtHjMaHPLKCHsFX3Z1GNYcniAMaQYeY_6YjWNP2KeTlb6X4MUpIA","auth":"-yWBVcaOtL6LXtMSgWB8iA"}}',  # noqa
        "data": {
            "title": "MY-APP PUSH",
            "body": "my push notification",
            "icon": "https://www.pngfind.com/pngs/b/168-1682511_notification-icon-png.png",
            "badge": "https://www.pngfind.com/pngs/b/168-1682511_notification-icon-png.png",
        },
    }
)

CHABOK_SINGLE_WEBPUSH_MESSAGE = json.dumps(
    {
        "application": "MY-APP",
        "created_time": "2020-01-01 20:22:00",
        "user": "USER_ID",
        "content": "test notif in app with examiner",
        "notification": {
            "title": "MY-APP chabok push",
            "body": "single push notif by notif app",
        },
    }
)

CHABOK_GROUP_WEBPUSH_MESSAGE = json.dumps(
    {
        "application": "MY-APP",
        "created_time": "2020-01-01 20:22:00",
        "users": ["ali", "reza"],
        "content": "test notif in app with examiner",
        "notification": {
            "title": "MY-APP chabok push",
            "body": "group push notif by notif app",
        },
    }
)

SINGLE_OTP_MESSAGE = json.dumps(
    {
        "application": "MY-APP",
        "created_time": "2020-01-01 20:22:00",
        "data": {"receptor": "+989101111111", "message": "hello"},
    }
)

GROUP_OTP_MESSAGE = json.dumps(
    {
        "application": "MY-APP",
        "created_time": "2020-01-01 20:22:00",
        "data": {"receptor": ["+989101111111", "+989101111112"], "message": ["1111", "2222"]},
    }
)

SINGLE_SMS_MESSAGE = json.dumps(
    {
        "application": "MY-APP",
        "created_time": "2020-01-01 20:22:00",
        "data": {"receptor": "+13431111111", "message": "Welcome to MY-APP.\nYour code is: 1111"},
    }
)
