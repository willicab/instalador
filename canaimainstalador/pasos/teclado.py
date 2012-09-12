#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''Configuración de la distribución del teclado'''
# Autor: William Cabrera
# Fecha: 11/10/2011

import gtk, os

from canaimainstalador.config import TECLADOS

class PasoTeclado(gtk.Fixed):
    def __init__(self, CFG):
        gtk.Fixed.__init__(self)

        self.lst_distribuciones = []             # distribuciones disponibles
        self.distribucion = ''                   # distribucion actual

        self.lbl1 = gtk.Label("Escoja una distribución de teclado")
        self.lbl1.set_size_request(690, 20)
        self.put(self.lbl1, 0, 0)

        self.cmb_dist = gtk.combo_box_new_text()
        for l1, l2 in TECLADOS.items():
            self.cmb_dist.append_text(l1)
            self.lst_distribuciones.append(l2)

        self.cmb_dist.set_active(0)
        self.cmb_dist.connect("changed", self.change_distribucion)
        self.cmb_dist.set_size_request(690, 30)
        self.put(self.cmb_dist, 0, 25)
        
        self.img_distribucion = gtk.Image()
        self.img_distribucion.set_size_request(690, 190)
        self.put(self.img_distribucion, 0, 70)

        self.lbl2 = gtk.Label("Presione algunas teclas para probar la distribución de teclado elegida")
        self.lbl2.set_size_request(690, 20)
        self.put(self.lbl2, 0, 265)

        self.txt_prueba = gtk.Entry()
        self.txt_prueba.set_size_request(690, 30)
        self.put(self.txt_prueba, 0, 290)

        self.change_distribucion()

    def change_distribucion(self, widget=None):
        self.distribucion = self.lst_distribuciones[self.cmb_dist.get_active()]
        path = 'canaimainstalador/data/img/key_' + self.distribucion + '.png'
        os.system("setxkbmap {0}".format(self.distribucion))
        self.img_distribucion.set_from_file(path)
