#-*- coding: UTF-8 -*-

import os
import gtk

class Main(gtk.Label):
    def __init__(self):
        msg = 'Ha culminado la instalación, puede reiniciar ahora el sistema\n'
        msg = msg + 'o seguir probando canaima y reiniciar más tarde.'
        gtk.Label.__init__(self, msg)
