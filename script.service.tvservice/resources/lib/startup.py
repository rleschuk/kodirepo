# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import os
import sys
import time
import requests
import xbmc, xbmcaddon
from multiprocessing import Process

monitor = xbmc.Monitor()
addon = xbmcaddon.Addon()

def main():
    from app import app
    app.run(host = '0.0.0.0',
            port = int(addon.getSetting('port')),
            threaded = True)

def stop():
    requests.post('http://%s:%s/shutdown' % \
        (addon.getSetting('host'),
         addon.getSetting('port')))

if __name__ == '__main__':
    server = Process(target=main)
    server.daemon = True
    server.start()
    while not monitor.abortRequested():
        if monitor.waitForAbort(10):
            stop()
            server.join()
            break
