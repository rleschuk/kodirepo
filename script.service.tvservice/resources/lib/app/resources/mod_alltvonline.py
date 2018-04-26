# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import base64
from app.resources import ResourceBase


class Resource(ResourceBase):
    url = 'http://www.alltvonline.ru/api/channels?language_id=2'

    def _get_stream(self, origin):
        html = self.get_html(origin['link'])
        stream = self.research("var m_link = '(.*?)'", html)
        if stream.endswith('flv'): return
        stream = base64.decodestring(stream)
        if 'tvrec' in stream: return
        if 'peers' in stream: return
        return stream
