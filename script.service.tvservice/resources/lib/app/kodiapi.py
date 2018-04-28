# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import xbmc
from kodijson import Kodi

def play(name):
    try:
        kodi = Kodi("http://{}:{}/jsonrpc".format('localhost', '8080'))
        channels = kodi.PVR.GetChannels(channelgroupid = 1)
        channels = channels.get('result', {}).get('channels', []) if channels else []
        labels = [i['label'] for i in channels]
        if name in labels:
            channel = channels[labels.index(name)]
            kodi.Player.Stop(playerid=1)
            return kodi.Player.Open({'item': {'channelid': channel['channelid']}})
    except:
        pass

def notification(text, title='TVService'):
    try:
        kodi = Kodi("http://{}:{}/jsonrpc".format('localhost', '8080'))
        kodi.GUI.ShowNotification(title=title, message=text)
    except:
        #xbmc.executebuiltin(("Notification(%s,%s,5000)" % (title, text)).encode('utf8'))
        pass
