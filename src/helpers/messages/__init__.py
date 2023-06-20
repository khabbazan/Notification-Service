import copy

from .message_source import messages_dict


def get_message(key, **kwargs):
    """Get message.

    Args:
        key(str): exp: "send_single_message"
        **kwargs(dict): exp: **{"a_sync": a_sync, "receptor": receptor}

    Returns:
        return a dictionary based on key , that contains message include with kwargs.

    Raises:
        There is no raised exception.
    """
    msg = copy.deepcopy(messages_dict).get(key, "===== msg error =====")
    if isinstance(msg, dict):
        if "a_sync" in kwargs.keys():
            if kwargs["a_sync"]:
                msg = msg.pop("a_sync", "----- msg error -----")
            else:
                msg = msg.pop("sync", "+++++ msg error +++++")
            kwargs.pop("a_sync")
        else:
            msg = msg.pop("sync", "+++++ msg error +++++")
    return msg.format(**kwargs)
