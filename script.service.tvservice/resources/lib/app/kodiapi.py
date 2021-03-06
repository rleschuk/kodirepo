# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import json
import xbmc, xbmcaddon, xbmcgui
import requests
import base64
from app import addon
from app import exceptions


def play(name):
    channels = json.loads(xbmc.executeJSONRPC('''{
        "jsonrpc": "2.0",
        "method": "PVR.GetChannels",
        "params": {"channelgroupid": 1},
        "id": 1
    }''')).get('result', {})
    if not channels:
        dialog = xbmcgui.Dialog()
        dialog.ok('TVService', 'Каналы отсутствуют. Перезапустите плагин "PVR IPTV Simple Clinet"')
        raise exceptions.ChannelNotFound()
    channels = channels.get('channels', []) if channels else []
    for channel in channels:
        if name == channel['label']:
            xbmc.executeJSONRPC('{"params":{"playerid":1},"jsonrpc":"2.0","id":1,"method":"Player.Stop"}')
            return json.loads(xbmc.executeJSONRPC('''{
                "jsonrpc": "2.0",
                "method": "Player.Open",
                "params": {"item": {"channelid": %s}},
                "id": 2
            }''' % channel['channelid']))
    raise exceptions.ChannelNotFound()

def notification(text, title='TVService'):
    xbmc.executebuiltin(("Notification(\"%s\",\"%s\",5000)" % (title, text)).encode('utf8'))

def check_pvr():
    if not addon.getSetting('pvr.iptvsimple'): return
    try:
        pvr = xbmcaddon.Addon('pvr.iptvsimple')
    except RuntimeError:
        dialog = xbmcgui.Dialog()
        dialog.ok('TVService', 'Не включен плагин "PVR IPTV Simple Clinet". Включите его и перезапустите сервис')
        raise Exception('enable "PVR IPTV Simple Clinet"')
    key = base64.b64encode('%s:%s' % (addon.getSetting('auth_username'), addon.getSetting('auth_password')))
    m3uurl = '%s/playlist?key=%s&host=%s&port=%s' % (
        addon.getSetting('service_url'),
        key,
        addon.getSetting('host'),
        addon.getSetting('port'),
    )
    epgurl = '%s/epgs?key=%s' % (
        addon.getSetting('service_url'),
        key
    )
    if pvr.getSetting('m3uPathType') != '1' or\
        pvr.getSetting('m3uUrl') != m3uurl or\
        pvr.getSetting('epgPathType') != '1' or\
        pvr.getSetting('epgUrl') != epgurl:
       dialog = xbmcgui.Dialog()
       if dialog.yesno('TVService', 'Изменить настройки клиента "PVR IPTV Simple Clinet"?'):
           if pvr.getSetting('m3uPathType') != '1': pvr.setSetting('m3uPathType', '1')
           if pvr.getSetting('m3uUrl') != m3uurl: pvr.setSetting('m3uUrl', m3uurl)
           if pvr.getSetting('epgPathType') != '1': pvr.setSetting('epgPathType', '1')
           if pvr.getSetting('epgUrl') != m3uurl: pvr.setSetting('epgUrl', epgurl)
