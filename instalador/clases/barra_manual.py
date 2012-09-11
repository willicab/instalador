# -*- coding: utf-8 -*-

import gtk, cairo, gobject

import instalador.clases.general as gen

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
        #self.particiones = self.par.particiones
        #self.total = gen.h2kb(self.par.total)
        
        cr.set_source_rgb(1.0, 1.0, 1.0)
        cr.rectangle(0, 0, self.ancho, self.alto)
        cr.fill()
