#-*- coding: UTF-8 -*-
'''Configuración de la distribución del teclado'''
# Autor: William Cabrera
# Fecha: 11/10/2011

import gtk, os
import clases.distribuciones as distribuciones

class Main(gtk.Fixed):
    txt_prueba = gtk.Entry()            # Entrada de prueba
    img_distribucion = gtk.Image()      # Imagen del keymap
    lst_distribuciones = []             # distribuciones disponibles
    distribucion = ''                   # distribucion actual

    def __init__(self):
        gtk.Fixed.__init__(self)
        self.cmb_dist = gtk.combo_box_new_text()

        self.lbl1 = gtk.Label("Escoja una distribución de teclado")
        self.lbl1.set_size_request(690, 20)
        self.put(self.lbl1, 0, 0)

        for l1, l2 in distribuciones.lista_distribuciones.items():
            self.cmb_dist.append_text(l1)
            self.lst_distribuciones.append(l2)

        self.cmb_dist.set_active(0)
        self.cmb_dist.connect("changed", self.change_distribucion)
        self.cmb_dist.set_size_request(690, 30)
        self.put(self.cmb_dist, 0, 25)

        self.img_distribucion.set_size_request(690, 190)
        self.put(self.img_distribucion, 0, 70)

        self.lbl2 = gtk.Label("Presione algunas teclas para probar la distribución de teclado elegida")
        self.lbl2.set_size_request(690, 20)
        self.put(self.lbl2, 0, 265)

        self.txt_prueba.set_size_request(690, 30)
        self.put(self.txt_prueba, 0, 290)

        self.show_all()
        self.change_distribucion()

    def change_distribucion(self, widget=None):
        self.distribucion = self.lst_distribuciones[self.cmb_dist.get_active()]
        cmd = "setxkbmap {0}".format(self.distribucion)
        path = 'data/img/key_' + self.distribucion + '.png'
        os.system('{0}'.format(cmd))
        self.img_distribucion.set_from_file(path)
