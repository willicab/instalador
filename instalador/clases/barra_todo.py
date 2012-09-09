# -*- coding: utf-8 -*-

import gtk, cairo

import instalador.clases.general as gen
from instalador.config import *

class Main(gtk.DrawingArea):

    def __init__(self, parent):
        super(Main, self).__init__()
        self.set_events(
            gtk.gdk.POINTER_MOTION_MASK | gtk.gdk.POINTER_MOTION_HINT_MASK |
            gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.BUTTON_RELEASE_MASK
            )
        self.connect("expose-event", self.expose)
        self.p = parent

    def expose(self, widget = None, event = None):
        self.forma = self.p.forma
        self.disco = self.p.disco
        self.ini = self.p.ini
        self.fin = self.p.fin
        self.total = self.fin - self.ini
        self.swap = self.p.swap
        self.root1 = gen.hum(gen.part_root1(self.total))
        self.root2 = gen.hum(gen.part_root2(self.total))
        self.usr = gen.hum(gen.part_root1(self.total))

        self.ancho = gen.h2kb(self.get_size_request()[0])
        self.alto = gen.h2kb(self.get_size_request()[1])
        w_swap = ((self.swap * self.ancho) / self.total) - 1
        x_swap = self.ancho - w_swap + 1

        cr = self.window.cairo_create()
        cr.set_source_rgb(1.0, 1.0, 1.0)
        cr.rectangle(0, 0, self.ancho, self.alto)
        cr.fill()
#                ini      fin                    fs       tipo
#['/dev/sda1', 1024.0, 27367456.0, 27366432.0, 'ext4', 'primary', 'boot', 3359844.0, 24006588.0, 488386584.0, 1],
        if self.forma == 'particion_1':
            p1 = ['', self.ini, self.fin, 0, 'ext4', 'primary', '', 0, 0, 0, 1]
            self.particiones = [p1,]
        elif self.forma == 'particion_2':
            p1 = ['', self.ini, self.fin, 0, 'ext4', 'primary', '', 0, 0, 0, 1]
            p1 = ['', self.ini, self.fin, 0, 'xfs', 'primary', '', 0, 0, 0, 1]
            self.particiones = [p1,]
        elif self.forma == 'particion_3':
            p1 = ['', self.ini, self.fin, 0, 'ext4', 'primary', '', 0, 0, 0, 1]
            p1 = ['', self.ini, self.fin, 0, 'ext4', 'primary', '', 0, 0, 0, 1]
            p1 = ['', self.ini, self.fin, 0, 'ext4', 'primary', '', 0, 0, 0, 1]
            self.particiones = [p1,]
        elif self.forma == 'particion_4':
            p1 = ['', self.ini, self.fin, 0, 'ext4', 'primary', '', 0, 0, 0, 1]
            p1 = ['', self.ini, self.fin, 0, 'ext4', 'primary', '', 0, 0, 0, 1]
            p1 = ['', self.ini, self.fin, 0, 'ext4', 'primary', '', 0, 0, 0, 1]
            p1 = ['', self.ini, self.fin, 0, 'ext4', 'primary', '', 0, 0, 0, 1]
            self.particiones = [p1,]
        else: pass

        for p in self.particiones:
            ini = gen.h2kb(p[1])
            fin = gen.h2kb(p[2])
            tipo = p[5]
            fs = p[4]

            if tipo == 'logical':
                y1 = 3
                y2 = self.alto - 3
            elif tipo == 'extended' or tipo == 'primary':
                y1 = 0
                y2 = self.alto

            x1 = ((ini * self.ancho) / self.total) + 1
            x2 = ((fin * self.ancho) / self.total) - 2

            if x2 - x1 > 1.5:
                self.draw_rounded(cr, (x1, y1, x2, y2), 5)
                cr.set_source(self.set_color(fs))
                cr.fill()

        linear = cairo.LinearGradient(0, 0, 0, alto)
        linear.add_color_stop_rgb(0, 0.3, 0.05, 0.0)
        linear.add_color_stop_rgb(0.3, 0.5, 0.2, 0.1)
        linear.add_color_stop_rgb(0.7, 0.7, 0.4, 0.3)
        cr.set_source(linear)
        cr.rectangle(x_swap, 0, w_swap, alto)
        cr.fill()
        
        #print self.metodo
        if self.metodo == 'particion_1':
            w_root = ancho - w_swap
            linear = cairo.LinearGradient(0, 0, 0, alto)
            linear.add_color_stop_rgb(0, 0.3, 0.3, 0)
            linear.add_color_stop_rgb(0.3, 0.5, 0.5, 0.2)
            linear.add_color_stop_rgb(0.7, 0.8, 0.8, 0.4)
            cr.set_source(linear)
            cr.rectangle(0, 0, w_root, alto)
            cr.fill()
        elif self.metodo == 'particion_2':
            w_root = ((gen.kb(self.root1) * ancho) / self.total) - 1
            x_root = 0
            w_home = ancho - w_swap - w_root - 1
            x_home = x_root + w_root + 1
            
            linear = cairo.LinearGradient(0, 0, 0, alto)
            linear.add_color_stop_rgb(0, 0.0, 0.05, 0.1)
            linear.add_color_stop_rgb(0.3, 0.1, 0.2, 0.3)
            linear.add_color_stop_rgb(0.7, 0.3, 0.4, 0.5)
            cr.set_source(linear)
            cr.rectangle(x_home, 0, w_home, alto)
            cr.fill()

            linear = cairo.LinearGradient(0, 0, 0, alto)
            linear.add_color_stop_rgb(0, 0.3, 0.3, 0)
            linear.add_color_stop_rgb(0.3, 0.5, 0.5, 0.2)
            linear.add_color_stop_rgb(0.7, 0.8, 0.8, 0.4)
            cr.set_source(linear)
            cr.rectangle(x_root, 0, w_root, alto)
            cr.fill()

        elif self.metodo == 'particion_3':
            w_boot = ((gen.kb(self.boot) * ancho) / self.total) - 1
            x_boot = 0
            w_root = ((gen.kb(self.root2) * ancho) / self.total) - 2
            x_root = x_boot + w_boot + 1
            w_usr  = ((gen.kb(self.usr) * ancho) / self.total) - 2
            x_usr  = x_root + w_root + 1
            w_home = ancho - w_swap - w_root - w_boot - w_usr - 3
            x_home = x_usr + w_usr + 1
            
            linear = cairo.LinearGradient(0, 0, 0, alto)
            linear.add_color_stop_rgb(0, 0.0, 0.0, 0.05)
            linear.add_color_stop_rgb(0.3, 0.0, 0.1, 0.2)
            linear.add_color_stop_rgb(0.7, 0.2, 0.3, 0.4)
            cr.set_source(linear)
            cr.rectangle(x_boot, 0, w_boot, alto)
            cr.fill()

            linear = cairo.LinearGradient(0, 0, 0, alto)
            linear.add_color_stop_rgb(0, 0.3, 0.3, 0)
            linear.add_color_stop_rgb(0.3, 0.5, 0.5, 0.2)
            linear.add_color_stop_rgb(0.7, 0.8, 0.8, 0.4)
            cr.set_source(linear)
            cr.rectangle(x_root, 0, w_root, alto)
            cr.fill()

            linear = cairo.LinearGradient(0, 0, 0, alto)
            linear.add_color_stop_rgb(0, 0.3, 0.3, 0.3)
            linear.add_color_stop_rgb(0.3, 0.5, 0.5, 0.5)
            linear.add_color_stop_rgb(0.7, 0.8, 0.8, 0.8)
            cr.set_source(linear)
            cr.rectangle(x_usr, 0, w_usr, alto)
            cr.fill()

            linear = cairo.LinearGradient(0, 0, 0, alto)
            linear.add_color_stop_rgb(0, 0.0, 0.05, 0.1)
            linear.add_color_stop_rgb(0.3, 0.1, 0.2, 0.3)
            linear.add_color_stop_rgb(0.7, 0.3, 0.4, 0.5)
            cr.set_source(linear)
            cr.rectangle(x_home, 0, w_home, alto)
            cr.fill()

    def cambiar(self, metodo):
        self.metodo = metodo
        self.expose()

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

    def set_color(self, fs):
        libre = cairo.LinearGradient(0, 0, 0, self.alto)

        if fs == 'btrfs':
            self.process_color(libre, '#ff5d2e', '#ff912e')
        elif fs == 'ext2':
            self.process_color(libre, '#2460c8', '#2e7bff')
        elif fs == 'ext3':
            self.process_color(libre, '#1b4794', '#2460c8')
        elif fs == 'ext4':
            self.process_color(libre, '#102b58', '#1b4794')
        elif fs == 'fat16':
            self.process_color(libre, '#00b900', '#00ff00')
        elif fs == 'fat32':
            self.process_color(libre, '#008100', '#00b900')
        elif fs == 'ntfs':
            self.process_color(libre, '#003800', '#008100')
        elif fs == 'hfs+':
            self.process_color(libre, '#382720', '#895f4d')
        elif fs == 'hfs':
            self.process_color(libre, '#895f4d', '#e49e80')
        elif fs == 'jfs':
            self.process_color(libre, '#e49e80', '#ffcfbb')
        elif fs == 'swap':
            self.process_color(libre, '#650000', '#cc0000')
        elif fs == 'reiser4':
            self.process_color(libre, '#45374f', '#806794')
        elif fs == 'reiserfs':
            self.process_color(libre, '#806794', '#b994d5')
        elif fs == 'xfs':
            self.process_color(libre, '#e89900', '#e8d000')
        elif fs == 'free':
            self.process_color(libre, '#ffffff', '#ffffff')
        elif fs == 'extended':
            self.process_color(libre, '#c9c9c9', '#c9c9c9')
        elif fs == 'unknown':
            self.process_color(libre, '#000000', '#000000')

        return libre
