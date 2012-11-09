#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ==============================================================================
# PAQUETE: canaima-instalador
# ARCHIVO: canaimainstalador/pasos/bienvenida.py
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

class PasoBienvenida(gtk.Fixed):
    def __init__(self, CFG):
        gtk.Fixed.__init__(self)

        msg_titulo = 'Bienvenido al asistente de instalación'
        msg_intro = 'Mediante este asistente usted podrá instalar Canaima en su computador. Antes de continuar, asegúrese de que su equipo cumple con los siguientes requisitos:'
        msg_disco = '● 6GB de espacio en disco (como mínimo).'
        msg_memoria = '● 384MB de memoria RAM (como mínimo).'
        msg_fin = 'Lo invitamos a seguir las instrucciones que se muestran en pantalla.'

        attr = pango.AttrList()
        size = pango.AttrSize(20000, 0, -1)
        attr.insert(size)

        self.lbltitulo = gtk.Label(msg_titulo)
        self.lbltitulo.set_size_request(640, 80)
        self.lbltitulo.set_alignment(0, 0)
        self.lbltitulo.set_attributes(attr)
        self.lbltitulo.set_line_wrap(True)
        self.put(self.lbltitulo, 50, 90)

        self.lblintro = gtk.Label(msg_intro)
        self.lblintro.set_size_request(640, 40)
        self.lblintro.set_alignment(0, 0)
        self.lblintro.set_line_wrap(True)
        self.put(self.lblintro, 50, 170)

        self.lbldisco = gtk.Label(msg_disco)
        self.lbldisco.set_size_request(640, 20)
        self.lbldisco.set_alignment(0, 0)
        self.lblintro.set_line_wrap(True)
        self.put(self.lbldisco, 50, 220)

        self.lblmemoria = gtk.Label(msg_memoria)
        self.lblmemoria.set_size_request(640, 20)
        self.lblmemoria.set_alignment(0, 0)
        self.lblmemoria.set_line_wrap(True)
        self.put(self.lblmemoria, 50, 240)

        self.lblfin = gtk.Label(msg_fin)
        self.lblfin.set_size_request(640, 20)
        self.lblfin.set_alignment(0, 0)
        self.lblfin.set_line_wrap(True)
        self.put(self.lblfin, 50, 270)

