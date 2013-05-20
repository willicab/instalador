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

LC_SUPPORTED_FILE = '/usr/share/i18n/SUPPORTED'


def get_country_id(lc):
    lc_split = lc.split('_')
    if len(lc_split) > 1:
        return lc_split[1][:2]
    else:
        None


def get_language_id(lc):
    return lc.split('_')[0]


class Locale():

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

    lc = Locale()
    for locale in lc.supported:
        print(locale)
        print('COUNTRY=%s' % get_country_id(locale[0]))
        print('LANGUAG=%s' % get_language_id(locale[0]))
        print()
