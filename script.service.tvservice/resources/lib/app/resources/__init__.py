# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import os
import re
import json
import time
import requests
import logging
import traceback
import datetime
from BeautifulSoup import BeautifulSoup
import xbmc, xbmcaddon

from app.memorize import memorize_response


class Base(object):
    def __init__(self):
        self.addon = xbmcaddon.Addon()
        self.json = json
        self.re = re
        self.traceback = traceback
        self.datetime = datetime
        self._cost = 99
        self._timeout = (5, 10)
        self._cookie = None

    @property
    def module(self):
        return self.__module__.split('.')[-1]

    @property
    def now_timestamp(self):
        return time.time()

    @property
    def now_datetime(self):
        return datetime.datetime.now()

    @property
    def timeout(self):
        return (int(self.addon.getSetting('max_connect_ms')) / 1000.,
                int(self.addon.getSetting('max_read_ms')) / 1000. )

    @property
    def cookie(self):
        return self._cookie


    def _get_soup(self, html):
        return BeautifulSoup(html)

    def _get_stream(self, origin):
        return origin.get('link')


    @staticmethod
    def research(pattern, string, group=1):
        try:
            return re.search(pattern, string, re.I).group(group)
        except Exception:
            return ''

    @staticmethod
    def _urlparse(url):
        return requests.urllib3.util.parse_url(url)


class ResourceBase(Base):
    def __init__(self, **kwargs):
        Base.__init__(self)
        self.urlparse = requests.urllib3.util.parse_url(self.url)
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def cookie(self):
        try:
            if self._cookie is None:
                with open(os.path.join(config.get('TMP_DIR', 'tmp'),
                        '%s.cookie' % self.urlparse.netloc), 'r') as cs:
                    self._cookie = requests.utils.cookiejar_from_dict(json.load(cs))
        except Exception:
            pass
        return self._cookie

    @cookie.setter
    def cookie(self, value):
        try:
            if isinstance(value, dict):
                self._cookie = requests.utils.cookiejar_from_dict(value)
            else:
                self._cookie = value
                value = requests.utils.dict_from_cookiejar(value)
            with open(os.path.join(config.get('TMP_DIR', 'tmp'),
                    '%s.cookie' % self.urlparse.netloc), 'w') as cs:
                json.dump(value, cs)
        except:
            pass

    @memorize_response(600)
    def get_response(self, url, referer=None, **kwargs):
        headers = {
            'User-Agent': 'Opera/10.60 (X11; openSUSE 11.3/Linux i686; U; ru) Presto/2.6.30 Version/10.60',
            'Accept': 'text/html, application/xml, application/xhtml+xml, */*',
            'Accept-Language': 'ru,en;q=0.9',
            'Referer': self.url,
        }
        if referer: headers['Referer'] = referer
        response = requests.get(url, headers=headers, timeout=self.timeout, **kwargs)
        xbmc.log(response.url)
        response.encoding = 'utf-8'
        return response

    def get_html(self, url, **kwargs):
        response = self.get_response(url, **kwargs)
        return response.text

    def get_json(self, url, **kwargs):
        response = self.get_response(url, **kwargs)
        return response.json()

    def get_soup(self, url):
        return self._get_soup(self.get_html(url))

    def get_stream(self, origin):
        return self._get_stream(origin)
