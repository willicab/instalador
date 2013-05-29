#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
        # Saneamos el nombre del pais (quitamos '@' y '.')
        countryid = lc_split[1].split('@')[0]
        countryid = countryid.split('.')[0]

        return countryid
    else:
        None


def get_language_id(lc):
    # Usamos split('.') para sanear los lenguajes como Esperanto (eo.UTF-8)
    # los cuales no tienen notación de pais, sino solo el lenguaje
    return lc.split('_')[0].split('.')[0]


def locale_content(localeitem):
    'Genera el contenido para el archivo /etc/default/locale'
    data = '''# Archivo generado por el Instalador de Canaima GNU/Linux
LANG="{0}"
LANGUAGE="{1}:{2}"
LC_ALL="{0}"
'''.format(localeitem.line[0], localeitem.get_locale(),
           get_language_id(localeitem.get_locale()))
    return data


def locale_gen_content(localeitem):
    'Genera el contenido para el archivo /etc/locale.gen'
    data = '''# Archivo generado por el Instalador de Canaima GNU/Linux
#
# This file lists locales that you wish to have built. You can find a list
# of valid supported locales at /usr/share/i18n/SUPPORTED, and you can add
# user defined locales to /usr/local/share/i18n/SUPPORTED. If you change
# this file, you need to rerun locale-gen.

{0} {1}
'''.format(localeitem.line[0], localeitem.line[1])
    return data


class _Iso_369_3(object):

    def __init__(self):
        ''
        self.names = {}

        print "Procesando archivo %s" % ISO_639_3_FILE

        document = xml.dom.minidom.parse(ISO_639_3_FILE)
        entries = document.getElementsByTagName('iso_639_3_entries')[0]
        self._handle_entries(entries)

    def _handle_entries(self, entries):
        for entry in entries.getElementsByTagName('iso_639_3_entry'):
            self._handle_entry(entry)

    def _handle_entry(self, entry):

        if entry.hasAttribute('part1_code'):
            code = entry.getAttribute('part1_code')
        elif entry.hasAttribute('part2_code'):
            code = entry.getAttribute('part2_code')
        else:
            code = entry.getAttribute('id')

        name = entry.getAttribute('name')

        self.names[code] = name


class Language(object):

    langs = []

    def __init__(self):
        self._get_all()

    def _get_all(self):
        isoxml = Iso_369_3()
        for entry in isoxml.names.items():
            self.langs.append(entry)

    def get_all(self):
        return self.langs

    def index_of(self, lang):
        'Retorna el indice de la lista donde está almacedado lang'
        i = 0
        exists = False
        for l in self.langs:
            if l[0] == lang:
                exists = True
                break
            i += 1
        if exists:
            return i
        else:
            return -1


class LocaleItem(object):
    line = None
    lang_id = None
    country_id = None
    collation = None

    def __init__(self, line):
        self.line = line.strip().split(' ')

        locale = self.line[0]

        self.collation = self.line[1]
        self.lang_id = get_language_id(locale)
        self.country_id = get_country_id(locale)

    def __lt__(self, other):
        '''Sobreescribe el ordenamiento (sort) para este tipo de dato, ordena
        los items alfabeticamente usando el nombre'''
        return self.line < other.line

    def get_locale(self):
        return '%s_%s' % (self.lang_id, self.country_id)

    def get_name(self):
        if self.lang_id in Iso_369_3().names:
            name = Iso_369_3().names[self.lang_id]
            return '%s - (%s)' % (name, self.country_id)
        else:
            print 'No se reconoce: %s' % self.line
            return self.lang_id


class _Locale(object):

    def __init__(self):
        '''
        Constructor
        '''
        self.supported = []
        self._parse_file()

    def _parse_file(self):
        try:
            print "Procesando archivo %s" % LC_SUPPORTED_FILE

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
            lci = LocaleItem(line)

            # FILTRO
            # Sólo UTF-8 por favor!
            if not lci.collation == "UTF-8":
                continue

            self.supported.append(lci)
        self.supported.sort()

    def index_of(self, locale):
        'Retorna el indice de la lista donde está almacedado locale'
        i = 0
        exists = False
        for l in self.supported:
            if l.get_locale() == locale:
                exists = True
                break
            i += 1
        if exists:
            return i
        else:
            return -1


_iso_369_3_cache = None
_locale_cache = None


def Iso_369_3():
    '''Este método nos permite usar la cache para el archivo de la ISO 369-3 \
    y de esta manera no tener que releerlo una y otra vez provocando lentitud \
    en el procesamiento.'''
    global _iso_369_3_cache
    if not _iso_369_3_cache:
        _iso_369_3_cache = _Iso_369_3()
    return _iso_369_3_cache


def Locale():
    '''Este método nos permite usar la cache para el archivo de locales \
    soportados (LC_SUPPORTED_FILE) y de esta manera no tener que releerlo una \
    y otra vez provocando lentitud en el procesamiento.'''
    global _locale_cache
    if not _locale_cache:
        _locale_cache = _Locale()
    return _locale_cache


if __name__ == "__main__":

    lang = Language()
    #print lang.get_all()

    lc = Locale()
    #print lc.supported

    isoxml = Iso_369_3()
    #print isoxml.names

    for locale in lc.supported:
        if locale.get_name():
            print locale.get_name()
            print locale.line
            print locale.lang_id
            print locale.country_id
            print locale.collation
            print locale_content(locale)
            print "----"
            print locale_gen_content(locale)
            print "----"
