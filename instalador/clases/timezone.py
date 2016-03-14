#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
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


class TimeZoneItem():

    country_id = ''
    coordinates = ''
    name = ''
    comments = ''

    def __init__(self, tz_line=None):
        if tz_line:
            self.create_from_line(tz_line)

    def create_from_line(self, tz_line):
        '''Lee una linea del archivo zone.tab, y la convierte en un
        TimeZoneItem'''

        line = tz_line.strip().split('\t')

        self.country_id = line[0]
        self.coordinates = line[1]
        self.name = line[2]
        # Si tiene comentarios
        if len(line) >= 4:
            self.comments = line[3]

    def __lt__(self, other):
        '''Sobreescribe el ordenamiento (sort) para este tipo de dato, ordena
        los items alfabeticamente usando el nombre'''
        return self.name < other.name


class _TimeZone():

    def __init__(self):
        '''
        Constructor
        '''
        self.tzones = []
        self._parse_file()

    def _parse_file(self):
        '''Lee el archivo de zonas horarias en busca de los nombres'''
        try:
            print "Procesando archivo %s" % TZ_DATA_FILE

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
            tzi = TimeZoneItem(line)
            self.tzones.append(tzi)
        #Ordena los tz por orden alfabetico
        self.tzones.sort()

    def index_of(self, tz_name):
        'Retorna el indice de la lista donde está almacedado tz_name'
        i = 0
        exists = False
        for tz in self.tzones:
            if tz.name == tz_name:
                exists = True
                break
            i += 1
        if exists:
            return i
        else:
            return -1

    def get_country_id(self, tz_name):
        c_id = None
        for tz in self.tzones:
            if tz.name == tz_name:
                c_id = tz.country_id
        return c_id


_timezone_cache = None


def TimeZone():
    '''Este método nos permite usar la cache para el archivo de zonas \
    horarias (TZ_DATA_FILE) y de esta manera no tener que releerlo una y \
    otra vez provocando lentitud en el procesamiento.'''
    global _timezone_cache
    if not _timezone_cache:
        _timezone_cache = _TimeZone()
    return _timezone_cache


if __name__ == "__main__":

    zh = TimeZone()
    for z in zh.tzones:
        print(z.country_id, z.coordinates, z.name, z.comments)

    print(zh.get_country_id('America/Caracas'))
    print(zh.get_country_id('America/New_York'))
