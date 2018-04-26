# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

from app.resources import ResourceBase


class Resource(ResourceBase):
    url = 'http://pomoyka.lib.emergate.net/trash/ttv-list/ttv.json'

    def _get_origins(self):
        data = self.get_json(self.url)
        for c in data['channels']:
            try:
                yield {
                    'name': c['name'],
                    'link': '/ace/getstream?id=%s' % c['url'],
                }
            except Exception:
                pass

    def _get_stream(self, origin):
        for orig in self._get_origins():
            if orig['name'] == origin['name']:
                return 'http://{ace_host}:{ace_port}%s' % orig['link']
