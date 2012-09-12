#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gtk, cairo

from canaimainstalador.clases.common import floatify

class BarraManual(gtk.DrawingArea):
    def __init__(self, parent):
        super(BarraManual, self).__init__()
        self.set_events(
            gtk.gdk.POINTER_MOTION_MASK | gtk.gdk.POINTER_MOTION_HINT_MASK |
            gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.BUTTON_RELEASE_MASK
            )
        self.connect("expose-event", self.expose)
        self.p = parent

    def expose(self, widget = None, event = None):
        self.ancho = floatify(self.get_size_request()[0])
        self.alto = floatify(self.get_size_request()[1])

        cr = self.window.cairo_create()
        cr.set_source_rgb(1.0, 1.0, 1.0)
        cr.rectangle(0, 0, self.ancho, self.alto)
        cr.fill()
