# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

from app.resources import ResourceBase


class Resource(ResourceBase):
    url = 'https://www.glaz.tv/online-tv/'

    def _get_stream(self, origin):
        stream = None
        html = self.get_html(origin['link'])
        if 'wmsAuthSign' in html:
            sig = self.research('var signature = "(.*?)"', html)
            stream = self.research('url: "(.*?)" \+ signature', html)
            if stream: stream += sig
        elif 'rosshow' in html:
            soup = self._get_soup(html)
            id_ = soup.find('iframe').get('src').replace('//rosshow.ru/iframe/','')
            stream = r'https://live-rmg.cdnvideo.ru/rmg/%s_new.sdp/chunklist.m3u8?hls_proxy_host=pub1.rtmp.s01.l.rmg' % id
        else:
            soup = self._get_soup(html)
            param = soup.find('param', dict(name = 'flashvars'))
            if param:
                stream = self.research('file=(.*)',
                    soup.find('param', dict(name = 'flashvars')).get('value'))
        return stream
