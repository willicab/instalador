#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import gtk

from canaimainstalador.clases.barra_todo import BarraTodo
from canaimainstalador.clases.leyenda import Leyenda
from canaimainstalador.config import *

class PasoPartTodo(gtk.Fixed):

    render = []
    forma = 'ROOT:HOME:SWAP:LIBRE'

    def __init__(self, CFG):
        gtk.Fixed.__init__(self)
        self.metodo = CFG['metodo']
        self.particiones = CFG['particiones']
        self.ini = CFG['ini']
        self.fin = CFG['fin']
        self.total = self.fin - self.ini
        self.current = self.total
        self.minimo = ESPACIO_TOTAL
        self.acciones = []
        self.libre = 0

        txt_info = "Seleccione el tamaño que desea usar para la instalación"
        self.lbl1 = gtk.Label(txt_info)
        self.lbl1.set_size_request(690, 20)
        self.lbl1.set_alignment(0, 0)
        self.put(self.lbl1, 0, 0)

        self.barra = BarraTodo(self)
        self.barra.set_size_request(690, 100)
        self.put(self.barra, 0, 60)

        msg_1 = "Instalar todo en una sola partición."
        self.option_1 = gtk.RadioButton(None, msg_1)
        self.option_1.connect("toggled", self.change_option, "ROOT:SWAP:LIBRE")
        self.option_1.set_size_request(350, 20)
        self.put(self.option_1, 0, 170)

        msg_2 = "Separar la partición /home (Recomendado)."
        self.option_2 = gtk.RadioButton(self.option_1, msg_2)
        self.option_2.set_active(True)
        self.option_2.connect("toggled", self.change_option, "ROOT:HOME:SWAP:LIBRE")
        self.option_2.set_size_request(350, 20)
        self.put(self.option_2, 0, 195)

        msg_3 = "Separar las particiones /home y /boot."
        self.option_3 = gtk.RadioButton(self.option_1, msg_3)
        self.option_3.connect("toggled", self.change_option, "BOOT:ROOT:HOME:SWAP:LIBRE")
        self.option_3.set_size_request(350, 20)
        self.put(self.option_3, 0, 220)

        msg_4 = "Separar las particiones /home, /boot, /var y /usr."
        self.option_4 = gtk.RadioButton(self.option_1, msg_4)
        self.option_4.connect("toggled", self.change_option, "BOOT:ROOT:VAR:USR:HOME:SWAP:LIBRE")
        self.option_4.set_size_request(350, 20)
        self.put(self.option_4, 0, 245)

        self.leyenda = Leyenda(self)
        self.leyenda.set_size_request(270, 150)
        self.put(self.leyenda, 390, 170)

    def change_option(self, widget, data):
        if widget.get_active() == True:
            self.forma = data
            self.barra.cambiar(self.forma)
            self.leyenda.cambiar(self.forma)

