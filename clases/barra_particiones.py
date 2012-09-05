# -*- coding: utf-8 -*-

import gtk
import cairo
import clases.general as gen
import gobject
from math import pi

class Main(gtk.DrawingArea):

    def __init__(self, parent):
        super(Main, self).__init__()
        self.par = parent
        self.set_events(gtk.gdk.POINTER_MOTION_MASK |
                      gtk.gdk.POINTER_MOTION_HINT_MASK |
                      gtk.gdk.BUTTON_PRESS_MASK |
                	  gtk.gdk.BUTTON_RELEASE_MASK )
        self.connect("expose-event", self.expose)

    def expose(self, widget=None, event=None):
        # Establece ancho y alto
        self.ancho = gen.h2kb(self.get_size_request()[0])
        self.alto = gen.h2kb(self.get_size_request()[1])
        self.total = gen.h2kb(self.par.total)
        self.particiones = self.par.particiones
        w = 0

        cr = self.window.cairo_create()
        cr.rectangle(0, 0, self.ancho, self.alto)
        cr.set_source_rgb(1.0, 1.0, 1.0)
        cr.fill()

#       print 'part, ini, fin, tam, fs, tipo, flags, usado, libre, total, num'

        for p in self.particiones:
            ini = gen.h2kb(p[1])
            fin = gen.h2kb(p[2])
            tipo = p[5]
            fs = p[4]

            if tipo == 'logical':
                y1 = 4
                y2 = self.alto - 8
            else:
                y1 = 1.5
                y2 = self.alto - 3

            x1 = ((ini * self.ancho) / self.total) + 1.5
            x2 = ((fin * self.ancho) / self.total) - 3

            if x2 - x1 > 1.5:
                self.draw_rounded(cr, (x1, y1, x2, y2), 5)
                cr.set_source(self.set_color(fs, tipo))
                cr.fill()

    def draw_rounded(self, cr, area, radius):
        x1, y1, x2, y2 = area
        cr.arc(x1 + radius, y1 + radius, radius, 2*(pi/2), 3*(pi/2))
        cr.arc(x2 - radius, y1 + radius, radius, 3*(pi/2), 4*(pi/2))
        cr.arc(x2 - radius, y2 - radius, radius, 0*(pi/2), 1*(pi/2))
        cr.arc(x1 + radius, y2 - radius, radius, 1*(pi/2), 2*(pi/2))
        cr.close_path()

    def hex_to_rgb(self, value):
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i+lv/3], 16) for i in range(0, lv, lv/3))

    def process_color (self, item, start, end):
        start = self.hex_to_rgb(start)+(0,)
        end = self.hex_to_rgb(end)+(1,)

        r1, g1, b1, pos = start
        r3, g3, b3, pos = end
        r2, g2, b2, pos = (int(r1+r3)/2, int(g1+g3)/2, int(b1+b3)/2, 0.5)
        mid = (r2, g2, b2, pos)

        for i in start, mid, end:
            rgb = float(i[3]), float(i[0])/255, float(i[1])/255, float(i[2])/255
            item.add_color_stop_rgb(*rgb)

    def set_color(self, fs, tipo_part):
        libre = cairo.LinearGradient(0, 0, 0, self.alto)

        if fs == 'ntfs':
            self.process_color(libre, '#00cc00', '#00ff00')
        if fs == 'fat32':
            self.process_color(libre, '#009900', '#00cc00')
        if fs == 'fat16':
            self.process_color(libre, '#005200', '#009900')
        elif fs == 'ext2':
            #colores 0.6, 0.7, 0.8
            libre.add_color_stop_rgb(0, 0.2, 0.3, 0.4)
            libre.add_color_stop_rgb(0.3, 0.4, 0.5, 0.6)
            libre.add_color_stop_rgb(0.7, 0.6, 0.7, 0.8)

#            usado.add_color_stop_rgb(0, 0, 0.1, 0.2)
#            usado.add_color_stop_rgb(0.3, 0.2, 0.3, 0.4)
#            usado.add_color_stop_rgb(0.7, 0.4, 0.5, 0.6)

        elif fs == 'ext3':
            #colores 0.4, 0.5, 0.6
            libre.add_color_stop_rgb(0, 0, 0.1, 0.2)
            libre.add_color_stop_rgb(0.3, 0.2, 0.3, 0.4)
            libre.add_color_stop_rgb(0.7, 0.4, 0.5, 0.6)

#            usado.add_color_stop_rgb(0, 0.0, 0.05, 0.1)
#            usado.add_color_stop_rgb(0.3, 0.1, 0.2, 0.3)
#            usado.add_color_stop_rgb(0.7, 0.3, 0.4, 0.5)

        elif fs == 'ext4':
            #colores 0.3, 0.4, 0.5
            libre.add_color_stop_rgb(0, 0.0, 0.05, 0.1)
            libre.add_color_stop_rgb(0.3, 0.1, 0.2, 0.3)
            libre.add_color_stop_rgb(0.7, 0.3, 0.4, 0.5)

#            usado.add_color_stop_rgb(0, 0.0, 0.0, 0.05)
#            usado.add_color_stop_rgb(0.3, 0.0, 0.1, 0.2)
#            usado.add_color_stop_rgb(0.7, 0.2, 0.3, 0.4)

        elif fs == 'swap':
            #colores 0.7, 0.4, 0.3
            libre.add_color_stop_rgb(0, 0.3, 0.05, 0.0)
            libre.add_color_stop_rgb(0.3, 0.5, 0.2, 0.1)
            libre.add_color_stop_rgb(0.7, 0.7, 0.4, 0.3)

#            usado.add_color_stop_rgb(0, 0.0, 0.0, 0.05)
#            usado.add_color_stop_rgb(0.3, 0.0, 0.1, 0.2)
#            usado.add_color_stop_rgb(0.7, 0.2, 0.3, 0.4)

        elif fs == 'free':
            #colores 0.7, 0.4, 0.3
            libre.add_color_stop_rgb(0.0, 0.74, 0.74, 0.74)
            libre.add_color_stop_rgb(0.5, 0.88, 0.88, 0.88)
            libre.add_color_stop_rgb(1, 0.95, 0.95, 0.95)

#            usado.add_color_stop_rgb(0, 0.0, 0.0, 0.05)
#            usado.add_color_stop_rgb(0.3, 0.0, 0.1, 0.2)
#            usado.add_color_stop_rgb(0.7, 0.2, 0.3, 0.4)

        if tipo_part == 'extended':
            #colores 0.5, 0.1, 0.1
            libre.add_color_stop_rgb(0, 0.5, 1.0, 1.0)
#            usado.add_color_stop_rgb(0, 0.0, 0.0, 0.05)

        return libre
