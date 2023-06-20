# flake8: NOQA

messages_dict = {
    ############################## send_sms module ##############################
    "send_single_message": {
        "sync": "single message to '{receptor}' sent successfully",
        "async": "single message to '{receptor}' added to queue successfully",
    },
    "failed_send_single_message": {
        "sync": "single message to '{receptor}' sent failed",
    },
    "send_group_message": {
        "sync": "messages to '{receptor}' sent successfully",
    },
    "failed_send_group_message": {
        "sync": "messages to '{receptor}' sent failed",
    },
    "send_single_otp_message": {
        "sync": "single otp message to '{receptor}' sent successfully",
    },
    "failed_send_single_otp_message": {
        "sync": "otp message to '{receptor}' sent failed",
    },
    "send_group_otp_message": {
        "sync": "group otp messages to '{receptor}' sent successfully",
    },
    "failed_send_group_otp_message": {
        "sync": "group otp messages to '{receptor}' sent failed",
    },
    ############################## send_webpush module ##############################
    "send_google_webpush": {
        "sync": "push notification to subscription '{subscription_info}' sent successfully by Google",
    },
    "failed_google_webpush": {
        "sync": "push notification to subscription '{subscription_info}' sent failed by Google",
    },
    "send_single_chabok_webpush": {
        "sync": "push notification to user '{user}' sent successfully by Chabok",
    },
    "failed_single_chabok_webpush": {
        "sync": "push notification to user '{user}' sent failed by Chabok",
    },
    "send_group_chabok_webpush": {
        "sync": "push notification to users '{users}' sent successfully by Chabok",
    },
    "failed_group_chabok_webpush": {
        "sync": "push notification to users '{users}' sent failed by Chabok",
    },
    # get public vapid key
    "get_public_vapid_key": {
        "sync": "public vapid key sent successfully to {app}",
    },
    " failed_get_public_vapid_key": {
        "sync": "public vapid key sent failed to {app}",
    },
}
