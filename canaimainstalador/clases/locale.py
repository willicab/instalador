#!/usr/bin/env python
''' -*- coding: utf-8 -*-

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
COPYING file for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

@author: Erick Birbe <erickcion@gmail.com>
'''


import xml.dom.minidom

LC_SUPPORTED_FILE = '/usr/share/i18n/SUPPORTED'
ISO_639_3_FILE = "/usr/share/xml/iso-codes/iso_639_3.xml"


def get_country_id(lc):
    lc_split = lc.split('_')
    if len(lc_split) > 1:
        return lc_split[1][:2]
    else:
        None


def get_language_id(lc):
    return lc.split('_')[0]


#TODO erickcion: Optimizar la lectura de estos archivos para evitar relecturas
class Iso_369_3(object):

    def __init__(self):
        self.names = {}
        document = xml.dom.minidom.parse(ISO_639_3_FILE)
        entries = document.getElementsByTagName('iso_639_3_entries')[0]
        self.handle_entries(entries)

    def handle_entries(self, entries):
        for entry in entries.getElementsByTagName('iso_639_3_entry'):
            self.handle_entry(entry)

    def handle_entry(self, entry):
        if (entry.hasAttribute('part1_code')
            and entry.hasAttribute('name')
            and entry.hasAttribute('status')
            and entry.getAttribute('status') == 'Active'):

            code = str(entry.getAttribute('part1_code'))
            name = str(entry.getAttribute('name'))

            self.names[code] = name


class Language(object):
    def __init__(self):
        pass

    def get_all(self):
        isoxml = Iso_369_3()
        data = []
        for entry in isoxml.names.items():
            data.append(entry)
        return data


#TODO erickcion: Optimizar la lectura de estos archivos para evitar relecturas
class Locale(object):

    def __init__(self):
        '''
        Constructor
        '''
        self.supported = []
        self._parse_file()

    def _parse_file(self):
        try:
            lf = open(LC_SUPPORTED_FILE, 'r')
            locales = lf.readlines()
        except Exception, msg:
            print(msg)
            print "No se pudo leer el archivo de idiomas"
        # Busca las zonas horarias en el archivo
        for line in locales:
            # Obvia los comentarios
            if line.startswith('#'):
                continue
            self.supported.append(line.strip().split(' '))
        self.supported.sort()


if __name__ == "__main__":

    lang = Language()
    print lang.get_all()

    lc = Locale()
    print lc.supported

    isoxml = Iso_369_3()
    print isoxml.names

    for locale in lc.supported:
        if get_language_id(locale[0]) in isoxml.names:
            print(locale)
            print('COUNTRY=%s' % get_country_id(locale[0]))
            print('LANGUAG=%s' % get_language_id(locale[0]))
            print
