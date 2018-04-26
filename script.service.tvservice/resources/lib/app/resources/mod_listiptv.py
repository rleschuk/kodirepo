# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

from app.resources import ResourceBase


class Resource(ResourceBase):
    url = 'http://listiptv.ru/fork18.m3u'

    def _get_origins(self):
        data = self.get_html(self.url)
        data = data.replace('\n','|')\
                   .replace('|#','\n')
        for c in data.split('\n'):
            if not c.startswith('EXTINF'): continue
            try:
                c = self.re.sub('^EXTINF.*?,','', c)
                name, link = c.split('|')
                if name.startswith('='): continue
                name = name.replace('(18+)','')
                name = name.strip()
                yield {
                    'name': name,
                    'link': link,
                }
            except ValueError:
                pass
            except Exception:
                pass

    def _get_stream(self, origin):
        for orig in self._get_origins():
            if orig['name'] == origin['name']:
                return orig['link']
