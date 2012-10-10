#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ==============================================================================
# PAQUETE: canaima-instalador
# ARCHIVO: canaimainstalador/pasos/teclado.py
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

import gtk

from canaimainstalador.config import TECLADOS, KEY_IMAGE_TMPL
from canaimainstalador.clases.common import ProcessGenerator

class PasoTeclado(gtk.Fixed):
    def __init__(self, CFG):
        gtk.Fixed.__init__(self)

        self.lst_distribuciones = []
        self.distribucion = ''

        self.lbl1 = gtk.Label("Escoja una distribución de teclado")
        self.lbl1.set_size_request(690, 20)
        self.put(self.lbl1, 0, 0)

        self.cmb_dist = gtk.combo_box_new_text()

        for l1, l2 in TECLADOS.items():
            self.lst_distribuciones.append(l1)
            self.cmb_dist.append_text(l2)

        self.cmb_dist.set_active(0)
        self.cmb_dist.connect("changed", self.change_distribucion)
        self.cmb_dist.set_size_request(690, 30)
        self.put(self.cmb_dist, 0, 25)
        
        self.img_distribucion = gtk.Image()
        self.img_distribucion.set_size_request(690, 210)
        self.put(self.img_distribucion, 0, 70)

        self.lbl2 = gtk.Label("Presione algunas teclas para probar la distribución de teclado elegida")
        self.lbl2.set_size_request(690, 20)
        self.put(self.lbl2, 0, 285)

        self.txt_prueba = gtk.Entry()
        self.txt_prueba.set_size_request(690, 30)
        self.put(self.txt_prueba, 0, 305)

        self.change_distribucion()

    def change_distribucion(self, widget=None):
        self.distribucion = self.lst_distribuciones[self.cmb_dist.get_active()]
        ProcessGenerator('setxkbmap {0}'.format(self.distribucion))
        self.img_distribucion.set_from_file(KEY_IMAGE_TMPL.format(self.distribucion))

