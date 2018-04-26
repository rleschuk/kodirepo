# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

from app.resources import ResourceBase


class Resource(ResourceBase):
    url = 'http://tv-only.org'

    def _get_stream(self, origin):
        html = self.get_html(origin['link'])
        stream = self.research("var src = \"(.*?)\"", html)
        return stream
