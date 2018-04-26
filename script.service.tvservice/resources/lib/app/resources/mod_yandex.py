# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

from app.resources import ResourceBase


class Resource(ResourceBase):
    url = 'https://www.yandex.ru/portal/tvstream_json/channels?locale=ru&from=morda'

    def _get_origins(self):
        data = self.get_json(self.url)
        for c in data.get('set',[]):
            try:
                yield {
                    'name': c.get('title'),
                    'link': c.get('content_url'),
                    'logo': 'http:%s' % c.get('logo') if c.get('logo') else ''
                }
            except Exception:
                pass

    def _get_stream(self, origin):
        for orig in self._get_origins():
            if orig['name'] == origin['name']:
                return orig['link']
