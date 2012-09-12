#-*- coding: UTF-8 -*-
'''Mensaje de Bienvenida'''
# Autor: William Cabrera
# Fecha: 11/10/2011

import gtk

class PasoBienvenida(gtk.Fixed):
    msg = "Bienvenido al asistente de instalación de Canaima GNU/Linux.\n\nEste asistente le guiará por los pasos para instalar\nCanaima GNU/Linux en tu equipo."

    def __init__(self, CFG):
        gtk.Fixed.__init__(self)
        self.lbl1 = gtk.Label(self.msg)
        self.lbl1.set_size_request(690, 400)
        self.put(self.lbl1, 0, 0)

