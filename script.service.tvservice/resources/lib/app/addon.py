
from __future__ import print_function, unicode_literals

import json
import xbmc, xbmcaddon

class singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Addon():
    __metaclass__ = singleton
    def __init__(self):
        self._addon = xbmcaddon.Addon('script.service.tvservice')

    def __getattr__(self, attr):
        return getattr(self._addon, attr)

    def getSetting(self, key):
        try: return json.loads(self._addon.getSetting(key))
        except: return self._addon.getSetting(key)


addon = Addon()
