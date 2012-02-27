"""
Small classes to assist with timezone calculations, LOGGER configuration,
and other common operations.
"""

import datetime
import pytz
import logging
import logging.handlers

LOGGER = logging.getLogger('ZiplineLogger')

def configure_logging(loglevel=logging.DEBUG):
    """
    Configures zipline.util.LOGGER to write a rotating file
    (10M per file, 5 files) to `` /var/log/zipline.log ``.
    """
    LOGGER.setLevel(loglevel)
    handler = logging.handlers.RotatingFileHandler(
        "/var/log/zipline/{lfn}.log".format(lfn="zipline"),
        maxBytes=10*1024*1024, backupCount=5
    )
    handler.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)s %(filename)s %(funcName)s - %(message)s",
        "%Y-%m-%d %H:%M:%S %Z")
    )
    LOGGER.addHandler(handler)
    LOGGER.info("logging started...")

def parse_date(dt_str):
    """
    Parse strings according to the same format as generated by
    format_date.
    """
    if(dt_str == None):
        return None
    parts = dt_str.split(".")
    dt = datetime.datetime.strptime(parts[0], '%Y/%m/%d-%H:%M:%S').replace(
        microsecond=int(parts[1]+"000")).replace(tzinfo = pytz.utc
    )
    return dt

def format_date(dt):
    """
    Format the date into a date with millesecond resolution and
    string/alphabetical sorting that is equivalent to datetime sorting.
    """
    if(dt == None):
        return None
    dt_str = dt.strftime('%Y/%m/%d-%H:%M:%S') + "." + str(dt.microsecond / 1000)
    return dt_str

class DocWrap():
    def __init__(self, store=None):
        if(store == None):
            self.store = {}
        else:
            self.store = store.copy()
        if(self.store.has_key('_id')):
            self.store['id'] = self.store['_id']
            del(self.store['_id'])
        
    def __setitem__(self,key,value):
        if(key == '_id'):
            self.store['id'] = value
        else:
            self.store[key] = value
        
    def __getitem__(self, key):
        if self.store.has_key(key):
            return self.store[key]
            
    def __getattr__(self,attrname):
        if self.store.has_key(attrname):
            return self.store[attrname]
        else:
            raise AttributeError("No attribute named {name}".format(name=attrname))
