#-*- coding: UTF-8 -*-

import os, gtk

class Main(gtk.Label):
    def __init__(self):
        msg = 'Ha culminado la instalación, puede reiniciar ahora el sistema o \
        seguir probando canaima y reiniciar más tarde.'
        gtk.Label.__init__(self, msg)
