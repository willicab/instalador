# -*- coding: utf-8 -*-

import gtk, cairo, gobject

import instalador.clases.general as gen

class Main(gtk.DrawingArea):
    #usado = ''
    #particion = ''
    def __init__(self, parent, metodo):
        super(Main, self).__init__()
        self.set_events(gtk.gdk.POINTER_MOTION_MASK |
                      gtk.gdk.POINTER_MOTION_HINT_MASK |
                      gtk.gdk.BUTTON_PRESS_MASK |
                	  gtk.gdk.BUTTON_RELEASE_MASK )
        self.par = parent
        self.metodo = metodo
        self.connect("expose-event", self.expose)
    
    def cambiar(self, metodo):
        self.metodo = metodo
        self.expose()
    
    def expose(self, widget=None, event=None):
        self.window.clear()
        cr = self.window.cairo_create()
        cr.set_line_width(0.8)

        #cr.select_font_face('Verdana', 
        #    cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(12)

        #establece ancho y alto
        ancho = self.get_size_request()[0]
        alto = self.get_size_request()[1]
        
        # Swap
        linear = cairo.LinearGradient(0, 0, 0, 20)
        linear.add_color_stop_rgb(0, 0.3, 0.05, 0.0)
        linear.add_color_stop_rgb(0.3, 0.5, 0.2, 0.1)
        linear.add_color_stop_rgb(0.7, 0.7, 0.4, 0.3)
        cr.set_source(linear)
        cr.rectangle(0, 0, 20, 20)
        cr.fill()
                
        # Root
        linear = cairo.LinearGradient(0, 0, 0, 20)
        linear.add_color_stop_rgb(0, 0.3, 0.3, 0)
        linear.add_color_stop_rgb(0.3, 0.5, 0.5, 0.2)
        linear.add_color_stop_rgb(0.7, 0.8, 0.8, 0.4)
        cr.set_source(linear)
        cr.rectangle(0, 25, 20, 20)
        cr.fill()

        if self.metodo == 'particion_2' or self.metodo == 'particion_3' :
            # Home
            linear = cairo.LinearGradient(0, 0, 0, 20)
            linear.add_color_stop_rgb(0, 0.0, 0.05, 0.1)
            linear.add_color_stop_rgb(0.3, 0.1, 0.2, 0.3)
            linear.add_color_stop_rgb(0.7, 0.3, 0.4, 0.5)
            cr.set_source(linear)
            cr.rectangle(0, 50, 20, 20)
            cr.fill()

        if self.metodo == 'particion_3':
            # Usr
            linear = cairo.LinearGradient(0, 0, 0, 20)
            linear.add_color_stop_rgb(0, 0.3, 0.3, 0.3)
            linear.add_color_stop_rgb(0.3, 0.5, 0.5, 0.5)
            linear.add_color_stop_rgb(0.7, 0.8, 0.8, 0.8)
            cr.set_source(linear)
            cr.rectangle(0, 75, 20, 20)
            cr.fill()

            # Boot
            linear = cairo.LinearGradient(0, 0, 0, 20)
            linear.add_color_stop_rgb(0, 0.0, 0.0, 0.05)
            linear.add_color_stop_rgb(0.3, 0.0, 0.1, 0.2)
            linear.add_color_stop_rgb(0.7, 0.2, 0.3, 0.4)
            cr.set_source(linear)
            cr.rectangle(0, 100, 20, 20)
            cr.fill()

