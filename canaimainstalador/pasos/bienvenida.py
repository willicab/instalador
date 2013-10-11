#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# =============================================================================
# PAQUETE: canaima-instalador
# ARCHIVO: canaimainstalador/pasos/bienvenida.py
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

#import gtk
from gi.repository import Gtk as gtk
import pango
from canaimainstalador.translator import gettext_install
from canaimainstalador.mod_accesible import atk_acc_vd


gettext_install()


class PasoBienvenida(gtk.Fixed):
    def __init__(self, CFG):
        gtk.Fixed.__init__(self)

        msg_titulo = _("Welcome to the Install Wizard")
        msg_intro = _("With this wizard you can easily install Canaima \
GNU/Linux on your computer. We invite you to follow the instructions \
displayed on screen.")

        #attr = pango.AttrList()
        #size = pango.AttrSize(20000, 0, -1)
        #attr.insert(size)

        self.lbltitulo = gtk.Label(label=msg_titulo)
        self.lbltitulo.set_size_request(640, 80)
        self.lbltitulo.set_alignment(0, 0)
        #self.lbltitulo.set_attributes(attr)
        self.lbltitulo.set_markup("<span font_size='20000'>"+msg_titulo+"</span>")


        self.lbltitulo.set_line_wrap(True)
        #self.lbltitulo.set_selectable(True)
        self.put(self.lbltitulo, 50, 90)

        self.lblintro = gtk.Label(label=msg_intro)
        self.lblintro.set_size_request(640, 40)
        self.lblintro.set_alignment(0, 0)
        self.lblintro.set_line_wrap(True)
        #self.lblintro.set_selectable(True)
        self.put(self.lblintro, 50, 170)

        #self.set_state_flags(gtk.CAN_FOCUS)
        self.set_can_focus(True)
        atk_acc_vd(self, msg_titulo + " " + msg_intro)
