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
    
    def expose(self, widget, event):
        #self.window.clear()
        cr = self.window.cairo_create()
        cr.set_line_width(0.8)

        #cr.select_font_face('Verdana', 
        #    cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(12)

        #establece ancho y alto
        ancho = self.get_size_request()[0]
        alto = self.get_size_request()[1]
        
        # Espacio usado
        cr.set_source_rgb(0.8, 0.8, 0.4)
        cr.rectangle(0, 0, 20, 20)
        cr.fill()
        
        # Espacio disponible
        cr.set_source_rgb(1.0, 1.0, 0.7)
        cr.rectangle(0, 25, 20, 20)
        cr.fill()

        # Espacio disponible
        cr.set_source_rgb(0.7, 1.0, 0.7)
        cr.rectangle(0, 50, 20, 20)
        cr.fill()

        # Espacio disponible
        cr.set_source_rgb(0.4, 0.8, 0.4)
        cr.rectangle(0, 75, 20, 20)
        cr.fill()

