#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import gtk

from canaimainstalador.clases.common import floatify, humanize
from canaimainstalador.clases.barra_auto import BarraAuto
from canaimainstalador.clases.leyenda import Leyenda
from canaimainstalador.config import *

class PasoPartAuto(gtk.Fixed):

    render = []
    forma = 'ROOT:HOME:SWAP'

    def __init__(self, CFG):
        gtk.Fixed.__init__(self)
        self.disco = CFG['disco']
        self.particion = CFG['particion']
        self.particiones = CFG['particiones']

        for x in self.particiones:
            if x[0] == self.particion:
                self.num = x[10]
                self.fs = x[4]
                self.usado = x[7]
                self.ini = x[1]
                self.fin = x[2]

        self.total = self.fin - self.ini
        self.libre = self.total - self.usado
        self.minimo = ESPACIO_TOTAL
        self.current = self.usado + ((self.total - self.minimo - self.usado) / 2)

        txt_info = "Seleccione el tamaño que desea usar para la instalación"
        self.lbl1 = gtk.Label(txt_info)
        self.lbl1.set_size_request(690, 20)
        self.lbl1.set_justify(gtk.JUSTIFY_CENTER)
        self.put(self.lbl1, 0, 0)

        self.barra = BarraAuto(self)
        self.barra.set_size_request(690, 100)
        self.put(self.barra, 0, 30)

        # Etiqueta Información Espacio Usado
        msg = 'Espacio Usado en la partición'
        self.lbl_usado = gtk.Label('{0} ({1})'.format(msg, humanize(self.usado)))
        self.lbl_usado.set_size_request(590, 20)
        self.lbl_usado.set_alignment(0, 0)
        self.put(self.lbl_usado, 22, 90)

        # Etiqueta Información Espacio Libre
        self.lbl_otra = gtk.Label('')
        self.lbl_otra.set_size_request(590, 20)
        self.lbl_otra.set_alignment(0, 0)
        self.put(self.lbl_otra, 22, 115)

        # Etiqueta Información Instalación canaima
        self.lbl_canaima = gtk.Label('')
        self.lbl_canaima.set_size_request(590, 20)
        self.lbl_canaima.set_alignment(0, 0)
        self.put(self.lbl_canaima, 22, 140)

        # Etiqueta Información Espacio mínimo
        msg = 'Espacio mínimo requerido para instalar Canaima GNU/Linux'
        self.lbl_minimo = gtk.Label('{0} ({1})'.format(msg, humanize(self.minimo)))
        self.lbl_minimo.set_size_request(590, 20)
        self.lbl_minimo.set_alignment(0, 0)
        self.put(self.lbl_minimo, 22, 165)
        self.lbl_minimo.show()

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

#        if self.swap != False:
#            # Etiqueta Información Swap
#            msg = 'Se usará la partición Swap Existente'
#            self.lbl_usado = gtk.Label('{0}'.format(msg))
#            self.lbl_usado.set_size_request(590, 20)
#            self.lbl_usado.set_alignment(1, 0)
#            self.put(self.lbl_usado, 0, 265)
#            self.lbl_usado.show()

    def change_option(self, widget, data):
        if widget.get_active() == True:
            self.forma = data
            self.barra.cambiar(self.forma)
            self.leyenda.cambiar(self.forma)

    def on_changed(self, widget=None):
        self.cur_value = int(self.barra.cur) #widget.get_value()
        if self.barra != None : self.barra.queue_draw()
        #print 'Changed: ', self.cur_value, gen.hum(self.cur_value)

    def get_cur_value(self):
        return self.cur_value

    def hay_swap(self):
        for p in self.particiones:
            if p[5].find('swap') != -1 : return True
        return False
