#-*- coding: UTF-8 -*-

''' Mensaje de Bienvenida '''
# Autor: William Cabrera, Wil Alvarez
# Fecha: 11/10/2011

import gtk

TITULO = "Bienvenido al asistente de instalación de Canaima GNU/Linux"
MENSAJE = "Este asistente le guiará por los pasos para instalar \
Canaima GNU/Linux en su equipo."

class Bienvenida(gtk.VBox):
    def __init__(self):
        gtk.VBox.__init__(self, False)
        
        title = gtk.Label()
        title.set_use_markup(True)
        title.set_markup('<span size="14000"><b>%s</b></span>' % TITULO)
        
        label = gtk.Label()
        label.set_use_markup(True)
        label.set_line_wrap(True)
        label.set_justify(gtk.JUSTIFY_LEFT)
        label.set_markup(MENSAJE)
        
        self.pack_start(title, False, False, 10)
        self.pack_start(label, True, True)
