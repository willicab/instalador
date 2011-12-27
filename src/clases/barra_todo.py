# -*- coding: utf-8 -*-

import gtk
import cairo
import clases.general as gen

class Main(gtk.DrawingArea):
#    root1_min = '2.5GB'
#    root1_max = '18GB'
#    root2_min = '512MB'
#    root2_max = '3GB'
#    usr_min = '2GB'
#    usr_max = '15GB'
    boot = '128MB'
#    _min = '5GB'
#    root1 = '2GB'
#    root2 = '307.2MB'
#    usr = '1843.2MB'
#    boot = '256MB'
    def __init__(self, cfg):
        super(Main, self).__init__()
        self.set_events(gtk.gdk.POINTER_MOTION_MASK |
                      gtk.gdk.POINTER_MOTION_HINT_MASK |
                      gtk.gdk.BUTTON_PRESS_MASK |
                	  gtk.gdk.BUTTON_RELEASE_MASK )
        self.connect("expose-event", self.expose)
        self.disco = cfg[0]
        self.ini = int(float(cfg[1]))
        self.fin = int(float(cfg[2]))
        self.swap = int(float(cfg[3]))
        self.metodo = cfg[4]
        self.total = int(self.fin - self.ini)
        self.root1 = gen.part_root1(self.total)
        self.root2 = gen.part_root1(self.total)
        self.usr = gen.part_root1(self.total)
#        self.root1 = ((self.total) * gen.kb(self.root1_min)) / gen.kb(self._min)
#        if self.root1 < gen.kb(self.root1_min): 
#            self.root1 = gen.kb(self.root1_min)
#        if self.root1 > gen.kb(self.root1_max): 
#            self.root1 = gen.kb(self.root1_max)

#        self.root2 = ((self.total) * gen.kb(self.root1_min)) / gen.kb(self._min)
#        if self.root2 < gen.kb(self.root2_min): 
#            self.root2 = gen.kb(self.root2_min)
#        if self.root2 > gen.kb(self.root2_max): 
#            self.root2 = gen.kb(self.root2_max)

#        self.usr = ((self.total) * gen.kb(self.usr_min)) / gen.kb(self._min)
#        if self.usr < gen.kb(self.usr_min): 
#            self.usr = gen.kb(self.usr_min)
#        if self.usr > gen.kb(self.usr_max): 
#            self.usr = gen.kb(self.usr_max)
    
    def cambiar(self, metodo):
        self.metodo = metodo
        self.expose()
        
    def expose(self, widget = None, event = None):
        cr = self.window.cairo_create()
        cr.set_line_width(0.8)

        cr.select_font_face("Courier", 
            cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(11)
        
        ancho = self.get_size_request()[0]
        alto = self.get_size_request()[1]
        
        w_swap = ((self.swap * ancho) / self.total) - 1
        x_swap = ancho - w_swap + 1
        
        cr.set_source_rgb(1.0, 1.0, 1.0)
        cr.rectangle(0, 0, ancho, alto)
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
            linear.add_color_stop_rgb(0, 0.3, 0.3, 0)
            linear.add_color_stop_rgb(0.3, 0.5, 0.5, 0.2)
            linear.add_color_stop_rgb(0.7, 0.8, 0.8, 0.4)
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

