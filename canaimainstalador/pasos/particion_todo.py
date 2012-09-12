#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import gtk

from canaimainstalador.clases.barra_todo import BarraTodo
from canaimainstalador.clases.leyenda import Leyenda

class PasoPartTodo(gtk.Fixed):

    render = []
    forma = 'ROOT:HOME:SWAP'

    def __init__(self, CFG):
        gtk.Fixed.__init__(self)
        self.disco = CFG['disco']
        self.ini = CFG['ini']
        self.fin = CFG['fin']

        txt_info = "Seleccione tipo de instalación que desea realizar"
        self.lbl1 = gtk.Label(txt_info)
        self.lbl1.set_size_request(690, 20)
        self.lbl1.set_justify(gtk.JUSTIFY_CENTER)
        self.put(self.lbl1, 0, 0)

        self.barra = BarraTodo(self)
        self.barra.set_size_request(690, 100)
        self.put(self.barra, 0, 30)

        # Opciones
        msg_1 = "Instalar todo en una sola partición."
        self.option_1 = gtk.RadioButton(None, msg_1)
        self.option_1.connect("toggled", self.change_option, "ROOT:SWAP")
        self.option_1.set_size_request(350, 20)
        self.put(self.option_1, 0, 140)

        msg_2 = "Separar la partición /home (Recomendado)."
        self.option_2 = gtk.RadioButton(self.option_1, msg_2)
        self.option_2.set_active(True)
        self.option_2.connect("toggled", self.change_option, "ROOT:HOME:SWAP")
        self.option_2.set_size_request(350, 20)
        self.put(self.option_2, 0, 165)

        msg_3 = "Separar las particiones /home y /boot."
        self.option_3 = gtk.RadioButton(self.option_1, msg_3)
        self.option_3.connect("toggled", self.change_option, "BOOT:ROOT:HOME:SWAP")
        self.option_3.set_size_request(350, 20)
        self.put(self.option_3, 0, 190)

        msg_4 = "Separar las particiones /home, /boot, /var y /usr."
        self.option_4 = gtk.RadioButton(self.option_1, msg_4)
        self.option_4.connect("toggled", self.change_option, "BOOT:ROOT:VAR:USR:HOME:SWAP")
        self.option_4.set_size_request(350, 20)
        self.put(self.option_4, 0, 215)

        msg_5 = "Particionar manualmente."
        self.option_5 = gtk.RadioButton(self.option_1, msg_5)
        self.option_5.connect("toggled", self.change_option, "MANUAL")
        self.option_5.set_size_request(350, 20)
        self.put(self.option_5, 0, 240)

        self.leyenda = Leyenda(self)
        self.leyenda.set_size_request(270, 150)
        self.put(self.leyenda, 390, 140)

    def change_option(self, widget, data):
        if widget.get_active() == True:
            self.forma = data
            self.barra.cambiar(self.forma)
            self.leyenda.cambiar(self.forma)

