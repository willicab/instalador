#-*- coding: UTF-8 -*-
'''Configuración de la distribución del teclado'''
# Autor: William Cabrera
# Fecha: 11/10/2011

import pygtk
pygtk.require('2.0')
import gtk
import os
import getpass
#import clases.distribuciones as distribuciones
from canaima.instalador.clases import distribuciones
import webkit

class Main(gtk.Fixed):
    txt_prueba = gtk.Entry()    # Entrada de prueba
    img_distribucion = gtk.Image()    # Imagen del keymap
    lst_distribuciones = []            # distribuciones disponibles
    distribucion = ''                 # distribucion actual
    def __init__(self):
        gtk.Fixed.__init__(self)
        
        self.lbl1 = gtk.Label("Configuración de la distribución")
        self.lbl1.set_size_request(590, 30)
        self.put(self.lbl1, 0, 0)
        self.lbl1.show()
        
        self.cmb_dist = gtk.combo_box_new_text()
        for l1, l2 in distribuciones.lista_distribuciones.items():
            self.cmb_dist.append_text(l1)
            self.lst_distribuciones.append(l2)
        self.cmb_dist.set_active(0)
        self.change_distribucion()
        self.cmb_dist.connect("changed", self.change_distribucion)
        self.cmb_dist.set_size_request(590, 30)
        self.put(self.cmb_dist, 0,  30)
        self.cmb_dist.show()
        
        self.img_distribucion.set_size_request(590, 150)
        self.put(self.img_distribucion, 0, 70)
        self.img_distribucion.show()
        
        self.lbl1 = gtk.Label("Escriba para probar la configuración")
        self.lbl1.set_size_request(590, 30)
        self.put(self.lbl1, 0, 220)
        self.lbl1.show()
        
        self.txt_prueba.set_size_request(590, 25)
        self.put(self.txt_prueba, 0, 250)
        self.txt_prueba.show()      
        
    def change_distribucion(self, widget=None):
        self.distribucion = self.lst_distribuciones[self.cmb_dist.get_active()]
        cmd = 'gconftool-2 -s /desktop/gnome/peripherals/keyboard/kbd/layouts '
        cmd = cmd + '-t list --list-type=string [{0}]'.format(self.distribucion)
        print cmd
        os.system('{0}'.format(cmd))
        self.txt_prueba.set_activates_default(True)
        path = 'data/distribuciones/' + self.distribucion + '.png'
        self.img_distribucion.set_from_file(path)










