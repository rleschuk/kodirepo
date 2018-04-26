# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

from app.resources import ResourceBase


class Resource(ResourceBase):
    url = 'http://www.trambroid.com/playlist.xspf'

    def _get_origins(self):
        soup = self.get_soup(self.url)
        for c in soup.findAll('track'):
            try:
                yield {
                    'name': c.find('title').string.strip(),
                    'link': '/ace/getstream?url=%s' % \
                        c.find('location').string.strip()
                }
            except Exception:
                pass

    def _get_stream(self, origin):
        for orig in self._get_origins():
            if orig['name'] == origin['name']:
                return 'http://{ace_host}:{ace_port}%s' % orig['link']
