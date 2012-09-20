#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gtk, cairo, gobject, math

from canaimainstalador.clases.common import floatify, set_color, process_color
from canaimainstalador.clases.common import hex_to_rgb, draw_rounded

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
        self.total = self.p.particiones[0][9]

        cr = self.window.cairo_create()
        cr.set_source_rgb(0.925490196, 0.91372549, 0.847058824)
        cr.rectangle(0, 0, self.ancho, self.alto)
        cr.fill()

        for p in self.particiones:
            ini = p[1]
            fin =  p[2]
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

