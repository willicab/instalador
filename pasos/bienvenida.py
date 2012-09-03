#-*- coding: UTF-8 -*-
'''Mensaje de Bienvenida'''
# Autor: William Cabrera
# Fecha: 11/10/2011

import gtk

class Main(gtk.Label):
    msg = "Bienvenido al asistente de instalación de Canaima GNU/Linux.\n\n" \
        "Este asistente le guiará por los pasos para instalar\n"\
        "Canaima GNU/Linux en tu equipo."
    def __init__(self):
        gtk.Label.__init__(self, self.msg)
        #self.set_justify(gtk.JUSTIFY_CENTER)

