#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import gtk

from canaimainstalador.clases.barra_auto import BarraAuto
from canaimainstalador.clases.leyenda import Leyenda
from canaimainstalador.config import *

class PasoPartAuto(gtk.Fixed):
    def __init__(self, CFG):
        gtk.Fixed.__init__(self)
        self.metodo = CFG['metodo']
        self.particiones = CFG['particiones']
        self.current = self.metodo['part'][7]
        self.usado = self.metodo['part'][7]
        self.forma = 'PART:ROOT:HOME:SWAP'
        self.minimo = ESPACIO_TOTAL
        self.nuevas = []
        self.acciones = []
        self.libre = 0

        txt_info = "Seleccione el tamaño que desea usar para la instalación"
        self.lbl1 = gtk.Label(txt_info)
        self.lbl1.set_size_request(690, 20)
        self.lbl1.set_alignment(0, 0)
        self.put(self.lbl1, 0, 0)

        self.barra = BarraAuto(self)
        self.barra.set_size_request(690, 100)
        self.put(self.barra, 0, 60)

        msg_1 = "Instalar todo en una sola partición."
        self.option_1 = gtk.RadioButton(None, msg_1)
        self.option_1.connect("toggled", self.change_option, "PART:ROOT:SWAP")
        self.option_1.set_size_request(350, 20)
        self.put(self.option_1, 0, 170)

        msg_2 = "Separar la partición /home (Recomendado)."
        self.option_2 = gtk.RadioButton(self.option_1, msg_2)
        self.option_2.connect("toggled", self.change_option, "PART:ROOT:HOME:SWAP")
        self.option_2.set_size_request(350, 20)
        self.put(self.option_2, 0, 195)

        msg_3 = "Separar las particiones /home y /boot."
        self.option_3 = gtk.RadioButton(self.option_1, msg_3)
        self.option_3.connect("toggled", self.change_option, "PART:BOOT:ROOT:HOME:SWAP")
        self.option_3.set_size_request(350, 20)
        self.put(self.option_3, 0, 220)

        msg_4 = "Separar las particiones /home, /boot, /var y /usr."
        self.option_4 = gtk.RadioButton(self.option_1, msg_4)
        self.option_4.connect("toggled", self.change_option, "PART:BOOT:ROOT:VAR:USR:HOME:SWAP")
        self.option_4.set_size_request(350, 20)
        self.put(self.option_4, 0, 245)

        self.leyenda = Leyenda(self)
        self.leyenda.set_size_request(270, 150)
        self.put(self.leyenda, 390, 170)

        self.option_2.set_active(True)

        if self.metodo['disco'][4] > 0:
            if self.metodo['disco'][3] == 0:
                # Disponibles: root+swap, root+home+swap
                self.option_3.set_sensitive(False)
                self.option_4.set_sensitive(False)
            elif self.metodo['disco'][3] == 1:
                # Disponibles: root+swap
                self.option_1.set_active(True)
                self.option_2.set_sensitive(False)
                self.option_3.set_sensitive(False)
                self.option_4.set_sensitive(False)

    def change_option(self, widget, forma):
        if widget.get_active() == True:
            self.barra.cambiar(forma)
            self.leyenda.cambiar(forma)
