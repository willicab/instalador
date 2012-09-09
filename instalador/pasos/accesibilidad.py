#-*- coding: UTF-8 -*-
'''Configuración de la Accesibilidad'''
# Autor: William Cabrera
# Fecha: 14/06/2012

import gtk

class Main(gtk.Fixed):
    def __init__(self):
        gtk.Fixed.__init__(self)

        self.lbl1 = gtk.Label("Opciones de accesibilidad")
        self.lbl1.set_size_request(590, 30)
        self.put(self.lbl1, 0, 0)
        self.lbl1.show()

        self.chkgdm = gtk.CheckButton("Activar accesibilidad en el acceso de usuario.")
        #self.chkgdm.connect("toggled", self.CheckButton_on_changed)
        self.chkgdm.set_size_request(590, 25)
        self.put(self.chkgdm, 0, 40)
        self.chkgdm.show()
