#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# =============================================================================
# PAQUETE: instalador
# ARCHIVO: instalador/config.py
# COPYRIGHT:
#       (C) 2012 William Abrahan Cabrera Reyes <william@linux.es>
#       (C) 2012 Erick Manuel Birbe Salazar <erickcion@gmail.com>
#       (C) 2012 Luis Alejandro Martínez Faneyth <luis@huntingbears.com.ve>
# LICENCIA: GPL-2
# =============================================================================
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import gtk
import pango
from instalador.translator import gettext_install
from instalador.mod_accesible import atk_acc_vd


gettext_install()


class PasoBienvenida(gtk.Fixed):
    def __init__(self, CFG):
        gtk.Fixed.__init__(self)

        msg_titulo = _("Welcome to the Install Wizard")
        msg_intro = _("With this wizard you can easily install Canaima \
GNU/Linux on your computer. We invite you to follow the instructions \
displayed on screen.")

        attr = pango.AttrList()
        size = pango.AttrSize(20000, 0, -1)
        attr.insert(size)

        self.lbltitulo = gtk.Label(msg_titulo)
        self.lbltitulo.set_size_request(640, 80)
        self.lbltitulo.set_alignment(0, 0)
        self.lbltitulo.set_attributes(attr)
        self.lbltitulo.set_line_wrap(True)
        #self.lbltitulo.set_selectable(True)
        self.put(self.lbltitulo, 50, 90)

        self.lblintro = gtk.Label(msg_intro)
        self.lblintro.set_size_request(640, 40)
        self.lblintro.set_alignment(0, 0)
        self.lblintro.set_line_wrap(True)
        #self.lblintro.set_selectable(True)
        self.put(self.lblintro, 50, 170)

        self.set_flags(gtk.CAN_FOCUS)
        atk_acc_vd(self, msg_titulo + " " + msg_intro)
