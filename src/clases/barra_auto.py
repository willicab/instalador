# -*- coding: utf-8 -*-

import gtk
import cairo
import clases.general as gen
import gobject

class Barra(gtk.DrawingArea):
    pos = []
    presionado = False
    cur = 0
    w = 0
    h = 0
    def __init__(self, parent, total, usado, libre, minimo, particion, swap = False):
        super(Barra, self).__init__()
        self.total = total
        self.usado = usado
        self.minimo = minimo
        self.libre = libre
        self.particion = particion
        self.par = parent
        self.cur = ((total - minimo) - usado) / 2
        self.par.cur_value = self.cur
        #self.par.on_changed()
        self.set_events(gtk.gdk.POINTER_MOTION_MASK |
                      gtk.gdk.POINTER_MOTION_HINT_MASK |
                      gtk.gdk.BUTTON_PRESS_MASK |
                	  gtk.gdk.BUTTON_RELEASE_MASK )
        self.connect("expose-event", self.expose)
        self.connect("button-press-event", self.press)
        self.connect("button-release-event", self.release)
        self.connect("motion-notify-event", self.draw_cursor)

    def press(self, widget, event):
        if event.x >= self.pos[0] and event.x <= self.pos[2] and \
            event.y >= self.pos[1] and event.y <= self.pos[3]:
            self.presionado = True
        
    def release(self, widget, event):
        self.presionado = False
    
    def draw_cursor(self, widget, event):
        if event.x >= self.pos[0] and event.x <= self.pos[2] and \
            event.y >= self.pos[1] and event.y <= self.pos[3]:
            cursor = gtk.gdk.Cursor(gtk.gdk.HAND2)    #esto crea un cursor que mostrara un lápiz
            self.window.set_cursor(cursor)           #se lo asignamos a nuestro dibujable
        else:
            cursor = gtk.gdk.Cursor(gtk.gdk.LEFT_PTR)    #esto crea un cursor que mostrara un lápiz
            self.window.set_cursor(cursor)           #se lo asignamos a nuestro dibujable            
        if self.presionado == True:
            #print 'posicion:', event.x, event.y
            x = (event.x * self.total) / self.w
            if x >= self.total - self.minimo: x = self.total - self.minimo
            if x <= self.usado + self.libre : x = self.usado + self.libre
            #if gen.hum(x)[-2:] == 'GB':
            #    self.cur = (float(gen.hum(x)[:-2]) * 1024) * 1024
            #elif gen.hum(x)[-2:] == 'MB':
            #    self.cur = (float(gen.hum(x)[:-2]) * 1024)
            self.cur = x
            #print 'Draw: ', self.cur,  gen.hum(self.cur)
            self.expose(self, event)
            self.par.on_changed()

    def expose(self, widget, event):
        #self.window.clear()
        #self.par.on_changed()
        cr = widget.window.cairo_create()
        cr.set_line_width(0.8)

        cr.select_font_face("Courier", 
            cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(11)

        #establece ancho y alto
        self.w = self.get_size_request()[0]
        self.h = self.get_size_request()[1]
        ancho = self.w
        alto = self.h # - 16

        #establece posicion actual     
        #self.cur = self.par.get_cur_value()
        
        w_usado = (int(self.usado) * ancho) / int(self.total)
        x_minimo = ((int(self.total) - int(self.minimo)) * ancho) / int(self.total)
        w_minimo = (int(self.minimo) * ancho) / int(self.total)
        x_particion = (self.cur * ancho) / int(self.total)
        w_particion = ancho - x_particion - w_minimo
        w_libre = x_particion - w_usado 
        x1_barra = x_particion - 5
        y1_barra = 10
        x2_barra = x_particion + 5
        y2_barra = alto - 10
        w_barra = 10
        h_barra = alto - 20
        self.pos = [x1_barra, y1_barra, x2_barra, y2_barra]
        
        # Espacio usado
        linear = cairo.LinearGradient(0, 0, 0, alto)
        linear.add_color_stop_rgb(0, 0.3, 0.3, 0)
        linear.add_color_stop_rgb(0.3, 0.5, 0.5, 0.2)
        linear.add_color_stop_rgb(0.7, 0.8, 0.8, 0.4)
        cr.set_source(linear)
        #cr.set_source_rgb(0.8, 0.8, 0.4)
        cr.rectangle(0, 0, w_usado, alto)
        cr.fill()

        # Espacio libre
        linear = cairo.LinearGradient(0, 0, 0, alto)
        linear.add_color_stop_rgb(0, 0.5, 0.5, 0)
        linear.add_color_stop_rgb(0.3, 0.7, 0.7, 0.3)
        linear.add_color_stop_rgb(0.7, 1.0, 1.0, 0.7)
        cr.set_source(linear)
        #cr.set_source_rgb(1.0, 1.0, 0.8)
        cr.rectangle(w_usado, 0, w_libre, alto)
        cr.fill()

        # Espacio Mínimo
        linear = cairo.LinearGradient(0, 0, 0, alto)
        linear.add_color_stop_rgb(0, 0, 0.3, 0)
        linear.add_color_stop_rgb(0.3, 0.2, 0.4, 0.2)
        linear.add_color_stop_rgb(0.7, 0.4, 0.8, 0.4)
        cr.set_source(linear)
        cr.rectangle(x_minimo, 0, w_minimo, alto)
        cr.fill()

        #Espacio a particionar
        linear = cairo.LinearGradient(0, 0, 0, alto)
        linear.add_color_stop_rgb(0, 0, 0.5, 0)
        linear.add_color_stop_rgb(0.3, 0.3, 0.7, 0.3)
        linear.add_color_stop_rgb(0.7, 0.7, 1.0, 0.7)
        cr.set_source(linear)
        #cr.set_source_rgb(0.8, 1.0, 0.8)
        cr.rectangle(x_particion, 0, w_particion, alto)
        cr.fill()

        canaima = gen.hum(self.total - self.cur)
        otra = gen.hum(self.cur)
        msg = 'Espacio que se usará para instalar Canaima GNU/Linux'
        self.par.lbl_canaima.set_text('{1} ({0})'.format(canaima, msg))
        msg = 'Espacio que quedará despues de redimensionar la particion'
        self.par.lbl_otra.set_text('{2} {0} ({1})'.format(self.particion, otra, msg))

        cr.set_source_rgb(0, 0, 0)
        area = (x1_barra, x2_barra, y1_barra, y2_barra)
        self.draw_rounded(cr, area, 3)
        for i in range(y1_barra + 3, y2_barra - 2, 3):
            cr.move_to(x1_barra + 1, i)
            cr.rel_line_to(8, 0)
            cr.stroke()
        
    def draw_rounded(self, cr, area, radius):
        """ draws rectangles with rounded (circular arc) corners """
        from math import pi
        a,b,c,d=area
        cr.arc(a + radius, c + radius, radius, 2*(pi/2), 3*(pi/2))
        cr.arc(b - radius, c + radius, radius, 3*(pi/2), 4*(pi/2))
        cr.arc(b - radius, d - radius, radius, 0*(pi/2), 1*(pi/2))  # ;o)
        cr.arc(a + radius, d - radius, radius, 1*(pi/2), 2*(pi/2))
        cr.close_path()
        cr.stroke()
        for i in range(c + 2, c - 2, 3):
            cr.move_to(a + 1, i)
            cr.rel_line_to(8, 0)
            cr.stroke()
            
        
