# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import json
import requests
import importlib
from flask import Flask, Response, request, jsonify, redirect, abort
from flask_cors import CORS, cross_origin
from app.addon import addon
import xbmc

app = Flask(__name__)
cors = CORS(app)


from app.utils import order, test, api_request
from app import kodiapi
from app import exceptions


@app.route('/shutdown', methods=['POST'])
def shutdown():
    request.environ.get('werkzeug.server.shutdown')()
    return Response('Server shutting down...', status=200)

@app.route('/')
def playlist():
    response = api_request('api/userchannels')
    m3u = []
    m3u.append('#EXTM3U')
    for channel in response.get('channels', []):
        m3u.append('#EXTINF:-1 group-title="%s" tvg-logo="%s", %s' % (
            channel['group_name'], channel['logo'], channel['name']))
        url = 'http://{host}:{port}/channel/{channel_id}'.format(
                host = addon.getSetting('host'),
                port = addon.getSetting('port'),
                channel_id = channel['id'])
        m3u.append(url)
    return ('\n'.join(m3u)).encode('utf8')

@app.route('/channel/<int:channel_id>')
def channel(channel_id):
    response = api_request('api/userchannels/%s' % channel_id)
    ace_host = addon.getSetting('ace_host')
    ace_port = addon.getSetting('ace_port')
    if response.get('origins', []):
        origins = order(response.get('origins'),
            hd = addon.getSetting('hd'),
            p2p = addon.getSetting('p2p'))
        for origin in origins:
            if not addon.getSetting(origin['resource']): continue
            module = 'app.resources.%s' % origin['resource']
            try:
                url = importlib.import_module(module).Resource().get_stream(origin)
                xbmc.log("%s: %s" % (origin['resource'], url), level=xbmc.LOGNOTICE)
            except Exception as err:
                xbmc.log("%s: %s" % (origin['resource'], repr(err)), level=xbmc.LOGERROR)
                continue
            if url:
                if 'ace_host' in url:
                    url = url.format(ace_host = ace_host, ace_port = ace_port)
                result = test(url)
                if result[1] < addon.getSetting('max_read_ms'):
                    kodiapi.notification('%s: %s' % (origin['resource'], result[0]), title=response['name'])
                    return redirect(result[0])
        kodiapi.notification('нет рабочих потоков', title=response['name'])
        xbmc.log(("%s: no working streams" % response['name']).encode('utf8'), level=xbmc.LOGERROR)
    else:
        kodiapi.notification('потоки не найдены', title=response['name'])
    return abort(403)

@app.route('/kodi/<method>', methods=['POST'])
@cross_origin()
def kodi(method):
    data = request.get_json()
    if method == 'play':
        try:
            return jsonify(kodiapi.play(data.get('name')))
        except exceptions.ChannelNotFound:
            return jsonify(error="Канал не найден в доступных каналах PVR. Обновите плейлист на Kodi."), 400
