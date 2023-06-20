import sys
import traceback
import warnings
from time import sleep

from src.core.rabbitmq import RabbitMQ
from src.core.settings import *  # noqa
from src.gateways import sms
from src.gateways import webpush

warnings.filterwarnings("ignore")

while True:

    try:
        mb = RabbitMQ()
        ############# execute gateways ############
        sms.execute()
        webpush.execute()

        ############# start consuming ############
        mb.start()

    except Exception as err:  # noqa
        print(err)  # todo: move this to log table.
        traceback.print_exc()  # todo: move this to log table.
        mb.reset_channel()

    except KeyboardInterrupt:
        # todo: save interrupt to log table.
        sys.exit(1)

    finally:
        sleep(1)
