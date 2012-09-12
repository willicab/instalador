#-*- coding: UTF-8 -*-
'''Configuración de la Accesibilidad'''
# Autor: William Cabrera
# Fecha: 14/06/2012

import gtk

class PasoAccesibilidad(gtk.Fixed):
    def __init__(self, CFG):
        gtk.Fixed.__init__(self)

        self.lbl1 = gtk.Label("Opciones de Accesibilidad")
        self.lbl1.set_size_request(590, 30)
        self.put(self.lbl1, 0, 0)

        self.chkgdm = gtk.CheckButton("Activar accesibilidad en la pantalla de acceso de usuario (GDM).")
        self.chkgdm.set_size_request(590, 25)
        self.put(self.chkgdm, 0, 40)
