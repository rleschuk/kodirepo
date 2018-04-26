# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

from app.resources import ResourceBase


class Resource(ResourceBase):
    url = 'http://only-tv.org'

    def _get_stream(self, origin):
        html = self.get_html(origin['link'])
        stream = self.research("file: '(.*?)'", html)
        if not stream: stream = self.research("file=(.*?m3u8)", html)
        return stream
