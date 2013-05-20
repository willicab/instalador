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

TZ_DATA_FILE = '/usr/share/zoneinfo/zone.tab'


class TimeZone():

    def __init__(self):
        '''
        Constructor
        '''
        self.tzones = []
        self._parse_file()

    def _parse_file(self):
        '''
        Lee el archivo de zonas horarias en busca de los nombres
        '''
        try:
            zf = open(TZ_DATA_FILE, 'r')
            zones = zf.readlines()
        except Exception, msg:
            print(msg)
            print "No se pudo leer el archivo de zonas horarias"
        # Busca las zonas horarias en el archivo
        for line in zones:
            # Obvia los comentarios
            if line.startswith('#'):
                continue
            # Extrae solo el nombre de la zona (Columna 3)
            self.tzones.append(line.strip().split('\t'))
        self.tzones.sort()

    def get_country_id(self, tz):
        c_id = None
        for line in self.tzones:
            if line[2] == tz:
                c_id = line[0]
        return c_id

if __name__ == "__main__":

    zh = TimeZone()
    for z in zh.tzones:
        print(z)

    print(zh.get_country_id('America/Caracas'))
    print(zh.get_country_id('America/New_York'))
