#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ==============================================================================
# PAQUETE: canaima-instalador
# ARCHIVO: canaimainstalador/clases/barra_particiones.py
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

from canaimainstalador.clases.common import set_color
from canaimainstalador.clases.common import draw_rounded

class BarraParticiones(gtk.DrawingArea):
    def __init__(self, parent):
        super(BarraParticiones, self).__init__()
        self.set_events(
            gtk.gdk.POINTER_MOTION_MASK | gtk.gdk.POINTER_MOTION_HINT_MASK |
            gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.BUTTON_RELEASE_MASK
            )
        self.connect("expose-event", self.expose)
        self.p = parent

    def expose(self, widget=None, event=None):
        self.ancho = self.get_size_request()[0]
        self.alto = self.get_size_request()[1]
        self.particiones = self.p.particiones

        if len(self.p.particiones) > 0:
            self.total = self.p.particiones[0][9]

        cr = self.window.cairo_create()
        cr.set_source_rgb(0.925490196, 0.91372549, 0.847058824)
        cr.rectangle(0, 0, self.ancho, self.alto)
        cr.fill()

        for p in self.particiones:
            ini = p[1]
            fin = p[2]
            tipo = p[5]
            fs = p[4]

            if tipo == 'logical':
                y1 = 3
                y2 = self.alto - 3
            elif tipo == 'extended' or tipo == 'primary':
                y1 = 0
                y2 = self.alto

            x1 = ((ini * self.ancho) / self.total)
            x2 = ((fin * self.ancho) / self.total)
            r = 1

            if x2 - x1 > 12:
                x1 = x1 + 1
                x2 = x2 - 1
                r = 5

            draw_rounded(cr, (x1, y1, x2, y2), r)
            cr.set_source(set_color(fs, self.alto))
            cr.fill()

