# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

from app.resources import ResourceBase

class Resource(ResourceBase):
    url = 'http://allfon-tv.com'

    def _get_stream(self, origin):
        stream = self.research('acestream://(.*?)"',
            self.get_html(origin['link']))
        return 'http://{ace_host}:{ace_port}/ace/getstream?id=%s' % stream
