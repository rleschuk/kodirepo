# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import xbmc
from kodijson import Kodi

def kodiapi(method, data):
    result = None
    if method == 'play':
        name = data.get('name')
        if name:
            kodi = Kodi("http://{}:{}/jsonrpc".format('localhost', '8080'))
            channels = kodi.PVR.GetChannels(channelgroupid = 1)
            channels = channels.get('result', {}).get('channels', []) if channels else []
            labels = [i['label'] for i in channels]
            if name in labels:
                channel = channels[labels.index(name)]
                kodi.Player.Stop(playerid=1)
                result = kodi.Player.Open({'item': {'channelid': channel['channelid']}})
    return {method: result}

def notification(text, title='TVService'):
    #xbmc.executebuiltin(("Notification(%s,%s,5000)" % (title, text)).encode('utf8'))
    kodi = Kodi("http://{}:{}/jsonrpc".format('localhost', '8080'))
    kodi.GUI.ShowNotification(title=title, message=text)
