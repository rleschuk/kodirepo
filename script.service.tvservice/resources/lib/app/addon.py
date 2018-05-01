
from __future__ import print_function, unicode_literals

import os
import json
import xbmc, xbmcaddon
import elementtree.ElementTree as ET

class singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Addon():
    __metaclass__ = singleton
    def __init__(self):
        self._addon = xbmcaddon.Addon('script.service.tvservice')

    @property
    def xml(self):
        xml = xbmc.translatePath('special://masterprofile/addon_data/script.service.tvservice/settings.xml')
        #if os.path.exists(xml):
        return xml

    def _getSetting(self, key):
        return self.json_loads(self._addon.getSetting(key))

    def getSetting(self, param, default=None, root=None):
        try:
            if root is None: root = ET.parse(self.xml).getroot()
            elements = root.findall('setting')
            for elem in elements:
                if param == elem.attrib.get('id'):
                    return self.json_loads(elem.attrib.get('value'))
        except IOError:
            return self._getSetting(param)

    def get_settings(self):
        root = ET.parse(self.xml).getroot()
        return [{'label': cat.get('label'),
            'items': [{
                'label': param.get('label'),
                'id': param.get('id'),
                'type': param.get('type'),
                'values': param.get('values').split('|') if param.get('values') else [],
                'value': self.get_setting(param.get('id'), param.get('default'), root=root),
                'option': param.get('option', '')
            } for param in cat.findall('setting')]
        } for cat in root.findall('category')]

    #def save_settings(self, data):
    #    root = ET.parse(self.xml).getroot()
    #    for k, v in data.items():
    #        try: root.find('setting[@id="%s"]' % k).attrib['value'] = re.sub('^"|"$', '', json.dumps(v))
    #        except: ET.SubElement(root, "setting", id=k, value=re.sub('^"|"$', '', json.dumps(v)))
    #    tree = ET.ElementTree(root)
    #    tree.write(self.xml, encoding="UTF-8", xml_declaration=True)

    def json_loads(self, data):
        try: return json.loads(data)
        except Exception: return data

addon = Addon()
