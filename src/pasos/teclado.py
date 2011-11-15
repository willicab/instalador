#-*- coding: UTF-8 -*-
'''Configuración de la distribución del teclado'''
# Autor: William Cabrera
# Fecha: 11/10/2011

import pygtk
pygtk.require('2.0')
import gtk
import os
import getpass
import layouts

class Main(gtk.Fixed):
    txt_prueba = gtk.Entry()    # Entrada de prueba
    img_layout = gtk.Image()    # Imagen del keymap
    lst_layouts = []            # layouts disponibles
    layout = ''                 # layout actual
    def __init__(self):
        gtk.Fixed.__init__(self)
        
        self.lbl1 = gtk.Label("Configuración de la distribución")
        self.lbl1.set_size_request(590, 30)
        self.lbl1.set_justify(gtk.JUSTIFY_CENTER)
        self.put(self.lbl1, 0, 0)
        self.lbl1.show()
        
        self.cmb_dist = gtk.combo_box_new_text()
        for l1, l2 in layouts.list_layouts.items():
            self.cmb_dist.append_text(l1)
            self.lst_layouts.append(l2)
        self.cmb_dist.set_active(0)
        self.change_layout()
        self.cmb_dist.connect("changed", self.change_layout)
        self.cmb_dist.set_size_request(590, 30)
        self.put(self.cmb_dist, 0,  30)
        self.cmb_dist.show()
        
        self.img_layout.set_size_request(590, 150)
        self.put(self.img_layout, 0, 70)
        self.img_layout.show()
        
        self.lbl1 = gtk.Label("Escriba para probar la configuración")
        self.lbl1.set_size_request(590, 30)
        self.lbl1.set_justify(gtk.JUSTIFY_CENTER)
        self.put(self.lbl1, 0, 220)
        self.lbl1.show()
        
        self.txt_prueba.set_size_request(590, 25)
        self.put(self.txt_prueba, 0, 250)
        self.txt_prueba.show()

    def change_layout(self, widget=None):
        self.layout = self.lst_layouts[self.cmb_dist.get_active()]
        cmd = 'gconftool-2 -s \
            /desktop/gnome/peripherals/keyboard/kbd/layouts -t list \
            --list-type=string [{0}]'
        cmd = cmd.format(self.layout)
        os.system(cmd)
        self.txt_prueba.set_activates_default(True)
        path = 'data/layouts/' + self.layout + '.png'
        self.img_layout.set_from_file(path)










