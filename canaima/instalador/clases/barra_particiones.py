# -*- coding: utf-8 -*-

import gtk
import cairo
import clases.general as gen
import gobject

class Main(gtk.DrawingArea):
    #usado = ''
    #particion = ''
    def __init__(self, parent):
        super(Main, self).__init__()
        self.par = parent
        self.set_events(gtk.gdk.POINTER_MOTION_MASK |
                      gtk.gdk.POINTER_MOTION_HINT_MASK |
                      gtk.gdk.BUTTON_PRESS_MASK |
                	  gtk.gdk.BUTTON_RELEASE_MASK )
        self.connect("expose-event", self.expose)
    
    def expose(self, widget=None, event=None):
        #self.window.clear()
        cr = self.window.cairo_create()
        cr.set_line_width(0.8)

        #cr.select_font_face('Verdana', 
        #    cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(12)

        #establece ancho y alto
        self.ancho = self.get_size_request()[0]
        self.alto = self.get_size_request()[1]
        self.particiones = self.par.particiones
        self.total = gen.h2kb(self.par.total)
        
        cr.set_source_rgb(1.0, 1.0, 1.0)
        cr.rectangle(0, 0, self.ancho, self.alto)
        cr.fill()
        
        for p in self.particiones:
            w = ((float(gen.kb(p[3])) * float(self.ancho)) / float(self.total)) - 2
            h = self.alto if p[4] != 'logical' else self.alto - 8
            x = ((float(gen.kb(p[1])) * float(self.ancho)) / float(self.total)) + 1
            y = 0  if p[4] != 'logical' else 4
            #print p[0], p[4], p[5], w, h, x, y, self.ancho, gen.kb(self.total)
            linear = self.color_fs(p[5], p[4])
            cr.set_source(linear[0])
            #cr.set_source_rgb(0.8, 0.8, 0.4)
            cr.rectangle(x, y, w, h)
            cr.fill()
    def set_particion(self, particiones, total):
        self.particion = particion
        self.total = gen.h2kb(total)
        
    def color_fs(self, fs, tipo_part):
        libre = None
        usado = None
        if fs == 'ntfs':
            libre = cairo.LinearGradient(0, 0, 0, self.alto)
            libre.add_color_stop_rgb(0, 0.5, 0.5, 0)
            libre.add_color_stop_rgb(0.3, 0.7, 0.7, 0.3)
            libre.add_color_stop_rgb(0.7, 1.0, 1.0, 0.7)
            
            usado = cairo.LinearGradient(0, 0, 0, self.alto)
            usado.add_color_stop_rgb(0, 0.3, 0.3, 0)
            usado.add_color_stop_rgb(0.3, 0.5, 0.5, 0.2)
            usado.add_color_stop_rgb(0.7, 0.8, 0.8, 0.4)
        elif fs == 'ext2':
            #colores 0.6, 0.7, 0.8
            libre = cairo.LinearGradient(0, 0, 0, self.alto)
            libre.add_color_stop_rgb(0, 0.2, 0.3, 0.4)
            libre.add_color_stop_rgb(0.3, 0.4, 0.5, 0.6)
            libre.add_color_stop_rgb(0.7, 0.6, 0.7, 0.8)
            
            usado = cairo.LinearGradient(0, 0, 0, self.alto)
            usado.add_color_stop_rgb(0, 0, 0.1, 0.2)
            usado.add_color_stop_rgb(0.3, 0.2, 0.3, 0.4)
            usado.add_color_stop_rgb(0.7, 0.4, 0.5, 0.6)
        elif fs == 'ext3':
            #colores 0.4, 0.5, 0.6
            libre = cairo.LinearGradient(0, 0, 0, self.alto)
            libre.add_color_stop_rgb(0, 0, 0.1, 0.2)
            libre.add_color_stop_rgb(0.3, 0.2, 0.3, 0.4)
            libre.add_color_stop_rgb(0.7, 0.4, 0.5, 0.6)
            
            usado = cairo.LinearGradient(0, 0, 0, self.alto)
            usado.add_color_stop_rgb(0, 0.0, 0.05, 0.1)
            usado.add_color_stop_rgb(0.3, 0.1, 0.2, 0.3)
            usado.add_color_stop_rgb(0.7, 0.3, 0.4, 0.5)
        elif fs == 'ext4':
            #colores 0.3, 0.4, 0.5
            libre = cairo.LinearGradient(0, 0, 0, self.alto)
            libre.add_color_stop_rgb(0, 0.0, 0.05, 0.1)
            libre.add_color_stop_rgb(0.3, 0.1, 0.2, 0.3)
            libre.add_color_stop_rgb(0.7, 0.3, 0.4, 0.5)
            
            usado = cairo.LinearGradient(0, 0, 0, self.alto)
            usado.add_color_stop_rgb(0, 0.0, 0.0, 0.05)
            usado.add_color_stop_rgb(0.3, 0.0, 0.1, 0.2)
            usado.add_color_stop_rgb(0.7, 0.2, 0.3, 0.4)
        elif fs == 'linux-swap(v1)':
            #colores 0.7, 0.4, 0.3
            libre = cairo.LinearGradient(0, 0, 0, self.alto)
            libre.add_color_stop_rgb(0, 0.3, 0.05, 0.0)
            libre.add_color_stop_rgb(0.3, 0.5, 0.2, 0.1)
            libre.add_color_stop_rgb(0.7, 0.7, 0.4, 0.3)
            
            usado = cairo.LinearGradient(0, 0, 0, self.alto)
            usado.add_color_stop_rgb(0, 0.0, 0.0, 0.05)
            usado.add_color_stop_rgb(0.3, 0.0, 0.1, 0.2)
            usado.add_color_stop_rgb(0.7, 0.2, 0.3, 0.4)
        elif tipo_part == 'extended':
            #colores 0.5, 0.1, 0.1
            libre = cairo.LinearGradient(0, 0, 0, self.alto)
            libre.add_color_stop_rgb(0, 0.5, 1.0, 1.0)
            
            usado = cairo.LinearGradient(0, 0, 0, self.alto)
            usado.add_color_stop_rgb(0, 0.0, 0.0, 0.05)
        elif fs == 'Free Space':
            #colores 0.7, 0.4, 0.3
            libre = cairo.LinearGradient(0, 0, 0, self.alto)
            libre.add_color_stop_rgb(0.7, 0, 0, 0)
            
            usado = cairo.LinearGradient(0, 0, 0, self.alto)
            usado.add_color_stop_rgb(0, 0.0, 0.0, 0.05)
            usado.add_color_stop_rgb(0.3, 0.0, 0.1, 0.2)
            usado.add_color_stop_rgb(0.7, 0.2, 0.3, 0.4)
        else: 
            libre = cairo.LinearGradient(0, 0, 0, self.alto)
            libre.add_color_stop_rgb(0, 0.5, 0.5, 5)
            libre.add_color_stop_rgb(0.3, 0.7, 0.7, 0.7)
            libre.add_color_stop_rgb(0.7, 1.0, 1.0, 1.0)
            
            usado = cairo.LinearGradient(0, 0, 0, self.alto)
            usado.add_color_stop_rgb(0, 0.3, 0.3, 0.3)
            usado.add_color_stop_rgb(0.3, 0.5, 0.5, 0.5)
            usado.add_color_stop_rgb(0.7, 0.8, 0.8, 0.8)
        return [libre, usado]
