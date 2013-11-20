#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# =============================================================================
# PAQUETE: canaima-instalador
# ARCHIVO: canaimainstalador/pasos/usuario.py
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

from canaimainstalador.translator import gettext_install
from gi.repository import Gtk, Pango
from canaimainstalador.mod_accesible import atk_label, atk_acc


gettext_install()


class PasoUsuario(Gtk.HBox):
    def __init__(self, CFG):
        Gtk.HBox.__init__(self)

        table = Gtk.Table(20, 2)

        # attr = Pango.AttrList()
        # size = Pango.AttrSize(18000, 0, -1)
        # attr.insert(size)

        self.lbltitle1 = Gtk.Label(_("Configuration for the administrator \
account"))
        self.lbltitle1.set_alignment(0, 0.5)
#         self.lbltitle1.set_attributes(attr)
        atk_label(self.lbltitle1)
        table.attach(self.lbltitle1, 0, 2, 0, 1)

        self.chkoem = Gtk.CheckButton(_("OEM Installation (Ignore this \
setting and makes it at the first start)."))
        self.chkoem.connect("toggled", self.oemchecked)
        table.attach(self.chkoem, 0, 2, 1, 2)

        self.chkgdm = Gtk.CheckButton(_("Enable Accessibility in the user \
login screen (GDM)."))
        table.attach(self.chkgdm, 0, 2, 2, 3)

        self.lblpassroot1 = Gtk.Label(_("Enter a password:"))
        self.lblpassroot1.set_alignment(0, 0.5)
        table.attach(self.lblpassroot1, 0, 1, 3, 4)

        self.txtpassroot1 = Gtk.Entry()
        self.txtpassroot1.set_visibility(False)
        atk_acc(self.txtpassroot1, self.lblpassroot1)
        table.attach(self.txtpassroot1, 1, 2, 3, 4)

        self.lblpassroot2 = Gtk.Label(_("Repeat the password:"))
        self.lblpassroot2.set_alignment(0, 0.5)
        table.attach(self.lblpassroot2, 0, 1, 4, 5)

        self.txtpassroot2 = Gtk.Entry()
        self.txtpassroot2.set_visibility(False)
        atk_acc(self.txtpassroot2, self.lblpassroot2)
        table.attach(self.txtpassroot2, 1, 2, 4, 5)

        self.lblmaquina = Gtk.Label(_("Machine name:"))
        self.lblmaquina.set_alignment(0, 0.5)
        table.attach(self.lblmaquina, 0, 1, 5, 6)

        self.txtmaquina = Gtk.Entry()
        self.txtmaquina.set_text('canaima-popular')
        self.txtmaquina.set_max_length(255)
        atk_acc(self.txtmaquina, self.lblmaquina)
        table.attach(self.txtmaquina, 1, 2, 5, 6)

        self.lbltitle2 = Gtk.Label(_("Configuration for the user account"))
        self.lbltitle2.set_alignment(0, 0.5)
#         self.lbltitle2.set_attributes(attr)
        atk_label(self.lbltitle2)
        table.attach(self.lbltitle2, 0, 2, 6, 7)

        self.lblnombre = Gtk.Label(_("Full name:"))
        self.lblnombre.set_alignment(0, 0.5)
        table.attach(self.lblnombre, 0, 1, 7, 8)

        self.txtnombre = Gtk.Entry()
        atk_acc(self.txtnombre, self.lblnombre)
        table.attach(self.txtnombre, 1, 2, 7, 8)

        self.lblusuario = Gtk.Label(_("User name:"))
        self.lblusuario.set_alignment(0, 0.5)
        table.attach(self.lblusuario, 0, 1, 8, 9)

        self.txtusuario = Gtk.Entry()
        atk_acc(self.txtusuario, self.lblusuario)
        table.attach(self.txtusuario, 1, 2, 8, 9)

        self.lblpassuser1 = Gtk.Label(_("Enter a password:"))
        self.lblpassuser1.set_alignment(0, 0.5)
        table.attach(self.lblpassuser1, 0, 1, 9, 10)

        self.txtpassuser1 = Gtk.Entry()
        self.txtpassuser1.set_visibility(False)
        atk_acc(self.txtpassuser1, self.lblpassuser1)
        table.attach(self.txtpassuser1, 1, 2, 9, 10)

        self.lblpassuser2 = Gtk.Label(_("Repeat the password:"))
        self.lblpassuser2.set_alignment(0, 0.5)
        table.attach(self.lblpassuser2, 0, 1, 10, 11)

        self.txtpassuser2 = Gtk.Entry()
        self.txtpassuser2.set_visibility(False)
        atk_acc(self.txtpassuser2, self.lblpassuser2)
        table.attach(self.txtpassuser2, 1, 2, 10, 11)

        self.pack_start(table, True, True, 40)

    def oemchecked(self, widget=None):
        active = not self.txtnombre.get_sensitive()
        self.txtpassroot1.set_sensitive(active)
        self.txtpassroot2.set_sensitive(active)
        self.txtnombre.set_sensitive(active)
        self.txtusuario.set_sensitive(active)
        self.txtpassuser1.set_sensitive(active)
        self.txtpassuser2.set_sensitive(active)
        self.txtmaquina.set_sensitive(active)
