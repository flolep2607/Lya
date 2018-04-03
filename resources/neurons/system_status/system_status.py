import psutil
import platform
import datetime

import logging

from kalliope.core.NeuronModule import NeuronModule, InvalidParameterException

logging.basicConfig()
logger = logging.getLogger("kalliope")

class System_status(NeuronModule):
    def __init__(self, **kwargs):
        super(System_status, self).__init__(**kwargs)

        response = {}
        os, name, version, _, _, _ = platform.uname()
        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        response['running_since'] = boot_time.strftime("%A %d. %B %Y")
        response['os'] = os
        response['os_version'] = version.split('-')[0]
        response['system_name'] = name
        response['system_nb_cores'] = psutil.cpu_count()
        response['cpu'] = psutil.cpu_percent()
        response['memory'] = psutil.virtual_memory()[2]
        response['disk'] = psutil.disk_usage('/')[3]

        logger.debug(response)

        self.say(response)



