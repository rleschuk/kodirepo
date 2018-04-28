# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import re
import json
import requests
import datetime
import xbmc

from app import addon

class InternalServerError(Exception): pass
class NotFound(Exception): pass
class StreamError(Exception): pass

def get_response(url, **kwargs):
    response = requests.get(url, **kwargs)
    return response

def api_request(route):
    json = get_response('%s/%s' % (addon.getSetting('service_url'), route),
        auth = (addon.getSetting('auth_username'), addon.getSetting('auth_password')),
        timeout = (2, 5)
    ).json()
    return json

def order(origins, hd=0, p2p=0):
    print('hd = %s' % hd)
    print('p2p = %s' % p2p)
    tmp = origins
    result = []
    if hd == 1:
        result.extend([c for c in tmp \
            if re.search('HD', c['name'])])
        result.extend([c for c in tmp \
            if not re.search('HD', c['name']) \
            and c not in result])
        tmp = result
        result = []
    if p2p == 1:
        result.extend([c for c in tmp \
            if re.search('(^/ace/|acestream)', c['link']) \
            and c not in result])
        result.extend([c for c in tmp \
            if not re.search('(^/ace/|acestream)', c['link']) \
            and c not in result])
    elif p2p == 2:
        result.extend([c for c in tmp \
            if not re.search('(^/ace/|acestream)', c['link']) \
            and c not in result])
        result.extend([c for c in tmp \
            if re.search('(^/ace/|acestream)', c['link']) \
            and c not in result])
    return result if result else tmp

def test(url):
    latency = addon.getSetting('max_read_ms')
    try:
        if '/ace/' in url:
            if not addon.getSetting('p2p_check'):
                return (url, 0)
            r = requests.get('%s&format=json' % url, timeout=(1., 1.))
            xbmc.log('%s: %s' % (url, r.status_code))
            xbmc.log(r.text)
            if r.status_code == 500:
                raise InternalServerError(r.status_code)
            elif r.status_code not in [200]:
                raise StreamError(r.status_code)
            data = json.loads(r.text)['response']
            err = json.loads(r.text)['error']
            if not err:
                d = datetime.datetime.now()
                r = requests.get(data['playback_url'], stream=True, timeout=(1., latency/1000.))
                xbmc.log('%s: %s' % (r.url, r.status_code))
                delta = datetime.datetime.now() - d
                r = requests.get(data['command_url']+'?method=stop', timeout=(1., 1.))
                xbmc.log('%s: %s' % (r.url, r.status_code))
                xbmc.log(r.text)

                if json.loads(r.text)['response'] == 'ok':
                    latency = delta.seconds*1000 + delta.microseconds/1000
            else:
                raise StreamError(err)
        else:
            d = datetime.datetime.now()
            r = requests.get(url, stream=True, timeout=(1., latency/1000.))
            xbmc.log('%s: %s' % (url, r.status_code))
            if r.status_code == 404:
                raise NotFound(r.status_code)
            elif r.status_code not in [200]:
                raise StreamError(r.status_code)
            delta = datetime.datetime.now() - d
            latency = delta.seconds * 1000 + delta.microseconds / 1000
        xbmc.log('latency %s: %s' % (url, latency), level=xbmc.LOGNOTICE)
    except requests.exceptions.ReadTimeout:
        xbmc.log('ReadTimeout: %s' % url, level=xbmc.LOGERROR)
    except requests.exceptions.ConnectTimeout:
        xbmc.log('ConnectTimeout: %s' % url, level=xbmc.LOGERROR)
    except requests.exceptions.ConnectionError:
        xbmc.log('ConnectionError: %s' % url, level=xbmc.LOGERROR)
    except InternalServerError:
        xbmc.log('InternalServerError: %s' % url, level=xbmc.LOGERROR)
    except NotFound:
        xbmc.log('NotFound: %s' % url, level=xbmc.LOGERROR)
    except StreamError as err:
        xbmc.log('StreamError: %s' % err, level=xbmc.LOGERROR)
    except Exception as err:
        xbmc.log('Exception: %s - %s' % (url, repr(err)), level=xbmc.LOGERROR)
    return (url, latency)
