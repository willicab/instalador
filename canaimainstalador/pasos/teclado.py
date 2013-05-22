#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# =============================================================================
# PAQUETE: canaima-instalador
# ARCHIVO: canaimainstalador/pasos/teclado.py
# COPYRIGHT:
#       (C) 2012 William Abrahan Cabrera Reyes <william@linux.es>
#       (C) 2012 Erick Manuel Birbe Salazar <erickcion@gmail.com>
#       (C) 2012 Luis Alejandro Martínez Faneyth <luis@huntingbears.com.ve>
# LICENCIA: GPL-3
# =============================================================================
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# COPYING file for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# CODE IS POETRY

import gtk

from canaimainstalador.config import TECLADOS, KEY_IMAGE_TMPL
from canaimainstalador.clases.common import ProcessGenerator
from canaimainstalador.clases.timezone import TimeZone
from canaimainstalador.clases.locale import Language


class PasoTeclado(gtk.VBox):
    'Presenta todo el proceso configuración de idioma y teclado'

    def __init__(self, CFG):
        'Constructor'
        gtk.VBox.__init__(self)

        self._lst_distribuciones = []
        self.distribucion = ''

        lbl_lang = gtk.Label("Idioma")
        self.add(lbl_lang)
        self._cmb_lang = gtk.combo_box_new_text()
        self._build_cmb_lang()
        self.add(self._cmb_lang)

        lbl_tz = gtk.Label("Zona Horaria")
        self.add(lbl_tz)
        self._cmb_tz = gtk.combo_box_new_text()
        self._build_cmb_tz()
        self.add(self._cmb_tz)

        lbl_keyboard = gtk.Label("Escoja una distribución de teclado")
        self.add(lbl_keyboard)
        self._cmb_keyboard = gtk.combo_box_new_text()

        for dist_id, dist_name in TECLADOS.items():
            self._lst_distribuciones.append(dist_id)
            self._cmb_keyboard.append_text(dist_name)

        self._cmb_keyboard.set_active(0)
        self._cmb_keyboard.connect("changed", self._change_distribucion)
        self.add(self._cmb_keyboard)

        self._img_distribucion = gtk.Image()
        self.add(self._img_distribucion)

        lbl2 = gtk.Label("Presione algunas teclas para probar la \
distribución de teclado elegida")
        self.add(lbl2)

        txt_prueba = gtk.Entry()
        self.add(txt_prueba)

        self._change_distribucion()

    def _build_cmb_tz(self):
        tz = TimeZone()
        for tz_item in tz.tzones:
            self._cmb_tz.append_text(tz_item.name)

    def _build_cmb_lang(self):
        lang = Language()
        for l in lang.get_all():
            print l
            self._cmb_lang.append_text(l[1])

    def _change_distribucion(self, widget=None):
        ''
        self.distribucion = self._lst_distribuciones[self._cmb_keyboard.get_active()]
        ProcessGenerator('setxkbmap {0} -model pc105'.format(
                                                            self.distribucion))
        self._img_distribucion.set_from_file(
                                      KEY_IMAGE_TMPL.format(self.distribucion))
