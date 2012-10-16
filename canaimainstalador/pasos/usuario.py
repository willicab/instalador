#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ==============================================================================
# PAQUETE: canaima-instalador
# ARCHIVO: canaimainstalador/pasos/usuario.py
# COPYRIGHT:
#       (C) 2012 William Abrahan Cabrera Reyes <william@linux.es>
#       (C) 2012 Erick Manuel Birbe Salazar <erickcion@gmail.com>
#       (C) 2012 Luis Alejandro Martínez Faneyth <luis@huntingbears.com.ve>
# LICENCIA: GPL-3
# ==============================================================================
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

import gtk, pango

class PasoUsuario(gtk.Fixed):
    def __init__(self, CFG):
        gtk.Fixed.__init__(self)

        attr = pango.AttrList()
        size = pango.AttrSize(18000, 0, -1)
        attr.insert(size)

        self.lbltitle1 = gtk.Label("Configuración de la cuenta de administrador")
        self.lbltitle1.set_size_request(690, 40)
        self.lbltitle1.set_alignment(0, 0)
        self.lbltitle1.set_attributes(attr)
        self.put(self.lbltitle1, 50, 0)

        self.lblpassroot1 = gtk.Label("Escriba una contraseña")
        self.lblpassroot1.set_size_request(690, 30)
        self.lblpassroot1.set_alignment(0, 0)
        self.put(self.lblpassroot1, 50, 40)

        self.txtpassroot1 = gtk.Entry()
        self.txtpassroot1.set_visibility(False)
        self.txtpassroot1.set_size_request(350, 25)
        self.put(self.txtpassroot1, 300, 40)

        self.lblpassroot2 = gtk.Label("Repita la contraseña")
        self.lblpassroot2.set_size_request(690, 30)
        self.lblpassroot2.set_alignment(0, 0)
        self.put(self.lblpassroot2, 50, 70)

        self.txtpassroot2 = gtk.Entry()
        self.txtpassroot2.set_visibility(False)
        self.txtpassroot2.set_size_request(350, 25)
        self.put(self.txtpassroot2, 300, 70)

        self.lblmaquina = gtk.Label('Nombre de la máquina')
        self.lblmaquina.set_size_request(690, 25)
        self.lblmaquina.set_alignment(0, 0)
        self.put(self.lblmaquina, 50, 100)

        self.txtmaquina = gtk.Entry()
        self.txtmaquina.set_text('canaima-popular')
        self.txtmaquina.set_size_request(350, 25)
        self.txtmaquina.set_max_length(255)
        self.put(self.txtmaquina, 300, 100)

        self.chkgdm = gtk.CheckButton("Activar accesibilidad en la pantalla de acceso de usuario (GDM).")
        self.chkgdm.set_size_request(690, 20)
        self.put(self.chkgdm, 50, 130)

        self.chkoem = gtk.CheckButton("Instalación OEM (ignora esta configuración y la realiza al primer inicio).")
        self.chkoem.connect("toggled", self.oemchecked)
        self.chkoem.set_size_request(690, 20)
        self.put(self.chkoem, 50, 150)

        self.lbltitle2 = gtk.Label("Configuración de la cuenta de usuario")
        self.lbltitle2.set_size_request(690, 40)
        self.lbltitle2.set_alignment(0, 0)
        self.lbltitle2.set_attributes(attr)
        self.put(self.lbltitle2, 50, 180)

        self.lblnombre = gtk.Label("Nombre Completo")
        self.lblnombre.set_size_request(690, 30)
        self.lblnombre.set_alignment(0, 0)
        self.put(self.lblnombre, 50, 220)

        self.txtnombre = gtk.Entry()
        self.txtnombre.set_size_request(350, 25)
        self.put(self.txtnombre, 300, 220)

        self.lblusuario = gtk.Label('Nombre de usuario')
        self.lblusuario.set_size_request(690, 25)
        self.lblusuario.set_alignment(0, 0)
        self.put(self.lblusuario, 50, 250)

        self.txtusuario = gtk.Entry()
        self.txtusuario.set_size_request(350, 25)
        self.put(self.txtusuario, 300, 250)

        self.lblpassuser1 = gtk.Label("Escriba una contraseña")
        self.lblpassuser1.set_size_request(690, 25)
        self.lblpassuser1.set_alignment(0, 0)
        self.put(self.lblpassuser1, 50, 280)

        self.txtpassuser1 = gtk.Entry()
        self.txtpassuser1.set_visibility(False)
        self.txtpassuser1.set_size_request(350, 25)
        self.put(self.txtpassuser1, 300, 280)

        self.lblpassuser2 = gtk.Label("Repita la contraseña")
        self.lblpassuser2.set_size_request(690, 25)
        self.lblpassuser2.set_alignment(0, 0)
        self.put(self.lblpassuser2, 50, 310)

        self.txtpassuser2 = gtk.Entry()
        self.txtpassuser2.set_visibility(False)
        self.txtpassuser2.set_size_request(350, 25)
        self.put(self.txtpassuser2, 300, 310)

    def oemchecked(self, widget=None):
        active = not self.txtnombre.get_sensitive()
        self.txtpassroot1.set_sensitive(active)
        self.txtpassroot2.set_sensitive(active)
        self.txtnombre.set_sensitive(active)
        self.txtusuario.set_sensitive(active)
        self.txtpassuser1.set_sensitive(active)
        self.txtpassuser2.set_sensitive(active)
        self.txtmaquina.set_sensitive(active)
        self.chkgdm.set_sensitive(active)

