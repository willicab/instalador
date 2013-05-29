#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
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
import subprocess
import xml.dom.minidom
from canaimainstalador.config import GUIDIR

XKB_FILE = '/usr/share/X11/xkb/rules/base.xml'
KB_SCRIPT = GUIDIR + '/data/scripts/keyboard.sh'


def guess_configuration(locale):
    assert locale  # Valida que locale contenga algo

    return subprocess.check_output([KB_SCRIPT, locale]).strip().split('/')


class XKB_Layout():

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __lt__(self, other):
        '''Sobreescribe el ordenamiento (sort) para este tipo de dato, ordena
        los items alfabeticamente usando el nombre'''
        return self.description < other.description


class _XKB_Rules(object):

    layouts = []

    def __init__(self):

        print "Procesando archivo %s" % XKB_FILE

        document = xml.dom.minidom.parse(XKB_FILE)
        layout_entries = document.getElementsByTagName('layoutList')[0]
        self._handle_entries(layout_entries)

        self.layouts.sort()

    def _handle_entries(self, entries):
        for entry in entries.getElementsByTagName('layout'):
            self._handle_entry(entry.getElementsByTagName('configItem')[0])

    def _handle_entry(self, entry):
        n_name = self._getText(
                              entry.getElementsByTagName('name')[0].childNodes)
        n_desc = self._getText(
                       entry.getElementsByTagName('description')[0].childNodes)
        self.layouts.append(XKB_Layout(n_name, n_desc))

    def _getText(self, nodelist):
        rc = []
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
        return str(''.join(rc))


class Keyboard(object):
    def __init__(self):
        self.xkb_rules = XKB_Rules()

    def all_layouts(self):
        return self.xkb_rules.layouts

    def index_of(self, layout):
        'Retorna el indice de la lista donde está almacedado layout'
        i = 0
        exists = False
        for lay in self.all_layouts():
            if lay.name == layout:
                exists = True
                break
            i += 1
        if exists:
            return i
        else:
            return -1


_xkb_rules_cache = None


def XKB_Rules():
    '''Este método nos permite usar la cache para el archivo de \
    configuraciones de teclado soportadas (XKB_FILE) y de esta manera no \
    tener que releerlo una y otra vez provocando lentitud en el \
    procesamiento.'''
    global _xkb_rules_cache
    if not _xkb_rules_cache:
        _xkb_rules_cache = _XKB_Rules()
    return _xkb_rules_cache

if __name__ == "__main__":

    k = Keyboard()
    for ly in k.all_layouts():
        print "%s - (%s)" % (ly.description, ly.name)
