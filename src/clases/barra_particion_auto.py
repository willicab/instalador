#!/usr/bin/python
# -*- coding: utf-8 -*-

# ZetCode PyGTK tutorial 
#
# This example creates a burning
# custom widget
#
# author: Jan Bodnar
# website: zetcode.com 
# last edited: April 2011


import gtk
import cairo
import clases.general as gen

class Burning(gtk.DrawingArea):
    def __init__(self, parent, total, usado, minimo, particion):
        self.par = parent
        self.total = float(total)
        self.usado = float(usado)
        self.minimo = float(minimo)
        self.particion = particion
        super(Burning, self).__init__()
        
        #self.num = ( "75", "150", "225", "300", 
        #    "375", "450", "525", "600", "675" )
 
        #self.set_size_request(-1, height)
        self.connect("expose-event", self.expose)
    
    def expose(self, widget, event):
        cr = widget.window.cairo_create()
        cr.set_line_width(0.8)

        cr.select_font_face("Courier", 
            cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(11)

        width = self.allocation.width
        height = self.allocation.height
     
        self.cur_width = self.par.get_cur_value()

        step = round(width / 10.0)

        till = (width / self.total) * self.cur_width
        minimo = (self.minimo * width) / self.total
        usado =  (self.usado * width) / self.total
        
        
        # Seleccionado para instalación
        cr.set_source_rgb(0, 1, 0)
        cr.rectangle(till, 0, width - till, height)
        cr.save()
        cr.clip()
        cr.paint()
        cr.restore()
        # Seleccionado para instalación
        cr.set_source_rgb(1, 1, 0)
        cr.rectangle(usado, 0, till - usado, height)
        cr.save()
        cr.clip()
        cr.paint()
        cr.restore()
        # Dibuja espacio usado
        cr.set_source_rgb(0.8, 0.8, 0)
        cr.rectangle(0, 0, usado, height)
        cr.save()
        cr.clip()
        cr.paint()
        cr.restore()
        # Dibuja espacio minimo
        cr.set_source_rgb(0, 0.8, 0)
        cr.rectangle(width - minimo, 0, minimo, height)
        cr.save()
        cr.clip()
        cr.paint()
        cr.restore()

        cr.set_source_rgb(0, 0, 0)

        nombre = 'Particion {0}'.format(self.particion)
        (x, y, ancho, alto, dx, dy) = cr.text_extents(nombre)
        cr.move_to((till / 2) - (ancho / 2), 40 - alto)
        cr.text_path(nombre)
        cr.stroke()
        
        valor = gen.hum(self.cur_width)
        (x, y, ancho, alto, dx, dy) = cr.text_extents(valor)
        cr.move_to((till / 2) - (ancho / 2), 40 + alto)
        cr.text_path(valor)
        cr.stroke()

        #(x, y, ancho, alto, dx, dy) = cr.text_extents('Mínimo')
        #cr.move_to(((width) - (minimo / 2)) - (ancho / 2), 40 + (alto / 2))
        #cr.text_path('Mínimo')
        #cr.stroke()

        nombre = 'Espacio a Ocupar por Canaima'
        (x, y, ancho, alto, dx, dy) = cr.text_extents(nombre)
        cr.move_to( ((till + width) / 2) - (ancho / 2), 40 - alto)
        cr.text_path(nombre)
        cr.stroke()

        valor = gen.hum(self.total - self.cur_width)
        (x, y, ancho, alto, dx, dy) = cr.text_extents(valor)
        cr.move_to( ((till + width) / 2) - (ancho / 2), 40 + alto)
        #cr.move_to((till / 2) - (ancho / 2), 40 + alto)
        cr.text_path(valor)
        cr.stroke()

        #cr.set_source_rgb(0.35, 0.31, 0.24)
        #for i in range(1, len(self.num) + 1):
        #    cr.move_to(i*step, 0)
        #    cr.line_to(i*step, 5)
        #    cr.stroke()
        #    
        #    (x, y, width, height, dx, dy) = cr.text_extents(self.num[i-1])
        #    cr.move_to(i*step-width/2, 15)
        #    cr.text_path(self.num[i-1])
        #    cr.stroke()
       
 
class PyApp(gtk.Window): 

    def __init__(self):
        super(PyApp, self).__init__()
        
        self.set_title("Burning")
        self.set_size_request(350, 200)        
        self.set_position(gtk.WIN_POS_CENTER)
        self.connect("destroy", gtk.main_quit)

        self.cur_value = 0
       
        vbox = gtk.VBox(False, 2)
        
        scale = gtk.HScale()
        scale.set_range(0, 750)
        scale.set_digits(0)
        scale.set_size_request(160, 40)
        scale.set_value(self.cur_value)
        scale.connect("value-changed", self.on_changed)
                
        fix = gtk.Fixed()
        fix.put(scale, 50, 50)
        
        vbox.pack_start(fix)
        
        self.burning = Burning(self)
        vbox.pack_start(self.burning, False, False, 0)

        self.add(vbox)
        self.show_all()
        
        
    def on_changed(self, widget):
        self.cur_value = widget.get_value()
        self.burning.queue_draw()
    
    
    def get_cur_value(self):
        return self.cur_value
    

#PyApp()
#gtk.main()

