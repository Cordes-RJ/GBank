# -*- coding: utf-8 -*-

import time
import utilParse
from datetime import datetime


class timer:
    def __init__(self):
        self.time = time.time()
    def stop(self):
        return time.time() - self.time
    
def timeToDateString(timestamp):
    o = datetime.fromtimestamp(timestamp)
    time = str(o.time())
    delimiter = utilParse.findCharacter(time,".")
    if delimiter == -1:
        return str(o.date()) + " " + str(o.time())
    return str(o.date()) + " " + str(time[0:delimiter])
