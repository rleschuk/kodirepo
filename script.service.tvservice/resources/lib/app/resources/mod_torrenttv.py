# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import requests
from app.resources import ResourceBase
from app.memorize import memorize_response

class Resource(ResourceBase):
    url = 'http://torrent-tv.ru/'

    def __init__(self):
        ResourceBase.__init__(self)
        self.username = self.addon.getSetting('%s.username' % self.module)
        self.password = self.addon.getSetting('%s.password' % self.module)

    @memorize_response(600)
    def get_response(self, url, **kwargs):
        with requests.session() as session:
            if not self.cookie:
                response = session.post('http://torrent-tv.ru/auth.php', verify=False, data = {
                    'email': self.username,
                    'password': self.password,
                    'remember': 'on',
                    'enter': 'Войти',
                }, headers = {
                    'Host': self.urlparse.netloc,
                    'Referer': self.url,
                    'User-Agent': 'Opera/10.60 (X11; openSUSE 11.3/Linux i686; U; ru) Presto/2.6.30 Version/10.60',
                    'Accept': 'text/html, application/xml, application/xhtml+xml, */*',
                    'Accept-Language': 'ru-RU',
                    'Content-Type': 'application/x-www-form-urlencoded',
                }, timeout = self.timeout)
                cookies = requests.utils.dict_from_cookiejar(response.cookies)
                if 'torrenttv_remember' in cookies:
                    self.cookie = cookies
            else:
                session.cookies = self.cookie
            response = session.get(url, headers={
                'User-Agent': 'Opera/10.60 (X11; openSUSE 11.3/Linux i686; U; ru) Presto/2.6.30 Version/10.60',
                'Accept': 'text/html, application/xml, application/xhtml+xml, */*',
                'Accept-Language': 'ru,en;q=0.9',
                'Referer': url,
            }, timeout=self.timeout)
            response.encoding = 'utf-8'
            return response

    def _get_stream(self, origin):
        soup = self.get_soup(origin['link'])
        ttvp = soup.find('div', {'id': 'ttv-player'})
        return 'http://{ace_host}:{ace_port}/ace/getstream?url=%s' %\
            ttvp.get('data-stream_url') if ttvp else None
