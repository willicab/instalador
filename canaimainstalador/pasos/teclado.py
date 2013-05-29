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

from canaimainstalador.clases.keyboard import Keyboard
from canaimainstalador.clases.i18n import Locale
from canaimainstalador.clases.timezone import TimeZone
from canaimainstalador.translator import gettext_install
import gobject
import gtk

gettext_install()


class ComboBoxObject(gtk.ComboBox):

    def __init__(self):

        self._store = gtk.ListStore(str, gobject.TYPE_PYOBJECT)
        gtk._gtk.ComboBox.__init__(self, self._store)

        cell = gtk.CellRendererText()
        self.pack_start(cell, True)
        self.add_attribute(cell, "text", 0)

    def append(self, value, obj):
        self._store.append([value, obj])

    def get_active_object(self):
        return self._store.get(self.get_active_iter(), 1)[0]


class PasoTeclado(gtk.VBox):
    'Presenta todo el proceso configuración de idioma y teclado'

    def __init__(self, CFG):
        'Constructor'
        gtk.VBox.__init__(self)

        self.keyboard = ''
        self.timezone = ''
        self.locale = ''

        lbl_lang = gtk.Label(_("Idioma"))
        self.pack_start(lbl_lang, False, False)
        self._cmb_lang = ComboBoxObject()
        self._build_cmb_lang()
        self.pack_start(self._cmb_lang, False, False)

        lbl_tz = gtk.Label(_("Zona Horaria"))
        self.pack_start(lbl_tz, False, False)
        self._cmb_tz = ComboBoxObject()
        self._build_cmb_tz()
        self.pack_start(self._cmb_tz, False, False)

        lbl_keyboard = gtk.Label(_("Teclado"))
        self.pack_start(lbl_keyboard, False, False)
        self._cmb_kbd = ComboBoxObject()
        self._build_cmb_keyboard()
        self.pack_start(self._cmb_kbd, False, False)

        hsep1 = gtk.HSeparator()
        self.pack_start(hsep1)

        #======================================================================
        # self._img_distribucion = gtk.Image()
        # self.add(self._img_distribucion)
        #======================================================================

        vbox1 = gtk.VBox()
        lbl2 = gtk.Label(_("Presione algunas teclas para probar la \
distribución de teclado elegida"))
        vbox1.pack_start(lbl2, False, False)
        txt_prueba = gtk.Entry()
        vbox1.pack_start(txt_prueba, False, False)
        self.pack_end(vbox1, False, False)

        self.reset_form()

    def _build_cmb_lang(self):

        lc = Locale()

        for l in lc.supported:
            self._cmb_lang.append(l.get_name(), l)

        self._cmb_lang.connect('changed', self._cmb_lang_changed)

    def _build_cmb_tz(self):
        tz = TimeZone()
        for tz_item in tz.tzones:
            self._cmb_tz.append(tz_item.name, tz_item)

        self._cmb_tz.connect('changed', self._cmb_tz_changed)

    def _build_cmb_keyboard(self):
        kbd = Keyboard()
        for lay in kbd.all_layouts():
            self._cmb_kbd.append(lay.description, lay)

        self._cmb_kbd.connect("changed", self._cmb_kbd_changed)

    def _cmb_lang_changed(self, widget=None):
        ''
        self.locale = widget.get_active_object().get_locale()
        print self.locale

    def _cmb_tz_changed(self, widget=None):
        ''
        self.timezone = widget.get_active_object().name
        print self.timezone

    def _cmb_kbd_changed(self, widget=None):
        ''
        self.keyboard = widget.get_active_object().name
        print self.keyboard

    def reset_form(self):
        '''Reinicia los campos a sus valores predeterminados'''
        # Lenguaje predeterminado
        i = Locale().index_of('es_VE')
        self._cmb_lang.set_active(i)

        # Zona horaria predeterminada
        i = TimeZone().index_of('America/Caracas')
        self._cmb_tz.set_active(i)

        # Teclado predeterminado
        i = Keyboard().index_of('latam')
        self._cmb_kbd.set_active(i)
