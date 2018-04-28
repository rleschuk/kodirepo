# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import os
import sys
import time
import requests
import xbmc, xbmcaddon
from threading import Thread
from app import app, addon, monitor

def main():
    app.run(host = '0.0.0.0',
            port = addon.getSetting('port'),
            threaded = True)

def stop():
    requests.post('http://%s:%s/shutdown' % \
        (addon.getSetting('host'),
         addon.getSetting('port')))

if __name__ == '__main__':
    server = Thread(target=main)
    server.daemon = True
    server.start()
    while not monitor.abortRequested():
        if monitor.waitForAbort(10):
            stop()
            server.join()
            break
