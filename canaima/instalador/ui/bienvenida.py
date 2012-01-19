#-*- coding: UTF-8 -*-

''' Mensaje de Bienvenida '''
# Autor: William Cabrera, Wil Alvarez
# Fecha: 18/01/2012

import gtk
import pango

TITULO = "Bienvenido al asistente de instalación de Canaima GNU/Linux"
MENSAJE = "Este asistente le guiará por los pasos para instalar \
Canaima GNU/Linux en su equipo."

class Bienvenida(gtk.VBox):
    def __init__(self):
        gtk.VBox.__init__(self, False)
        
        title = gtk.Label()
        title.set_use_markup(True)
        title.set_markup('<span size="12000"><b>%s</b></span>' % TITULO)
        
        label = gtk.Label()
        label.set_use_markup(True)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.set_markup(MENSAJE)
        box = gtk.HBox(False)
        box.pack_start(label, False, False)
        box.set_border_width(30)
        
        self.pack_start(title, False, False, 20)
        self.pack_start(box, True, True)
