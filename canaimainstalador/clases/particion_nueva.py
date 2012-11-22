#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ==============================================================================
# PAQUETE: canaima-instalador
# ARCHIVO: canaimainstalador/clases/particion_nueva.py
# COPYRIGHT:
#       (C) 2012 William Abrahan Cabrera Reyes <william@linux.es>
#       (C) 2012 Erick Manuel Birbe Salazar <erickcion@gmail.com>
#       (C) 2012 Luis Alejandro Martínez Faneyth <luis@huntingbears.com.ve>
# LICENCIA: GPL-3
# ==============================================================================
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# COPYING file for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# CODE IS POETRY

import gtk

from canaimainstalador.clases.common import humanize, TblCol, get_next_row, \
    get_row_index, set_partition, PStatus, get_sector_size, \
    validate_minimun_fs_size, validate_maximun_fs_size, UserMessage
from canaimainstalador.translator import msj
from canaimainstalador.clases.frame_fs import frame_fs
from canaimainstalador.config import FSMIN, FSMAX

class Main(gtk.Dialog):

    inicio_part = 0
    fin_part = 0

    def __init__(self, padre):
        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        gtk.Window.set_position(self, gtk.WIN_POS_CENTER_ALWAYS)
        self.disco = padre.disco
        self.sector = get_sector_size(self.disco)
        self.lista = padre.lista
        self.acciones = padre.acciones
        self.particion_act = padre.fila_selec
        # Toma el inicio_part y fin_part de la particion seleccionada
        self.inicio_part = self.particion_act[TblCol.INICIO]
        self.fin_part = self.particion_act[TblCol.FIN]
        self.num_fila_act = get_row_index(self.lista, self.particion_act)
        self.particion_sig = get_next_row(self.lista, self.particion_act,
                                          self.num_fila_act)

        self.set_title("Nueva Partición")
        self.set_resizable(0)

        self.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        self.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        self.set_default_response(gtk.RESPONSE_CANCEL)

        #Tamaño de la partición
        lbl_tamano = gtk.Label('Tamaño:')
        lbl_tamano.set_alignment(0, 0.5)
        lbl_tamano.show()
        adj = gtk.Adjustment(self.fin_part, self.inicio_part, self.fin_part, \
                             1.0, 1024.0, 0.0)
        self.escala = gtk.HScale()
        self.escala.set_digits(0)
        self.escala.set_draw_value(False)
        self.escala.set_adjustment(adj)
        self.escala.set_size_request(450, -1)
        self.escala.connect("value-changed", self.escala_on_changed)
        self.escala.show()

        self.lblsize = gtk.Label(humanize(self.escala.get_value() - \
                                          self.inicio_part))
        self.lblsize.show()

        hbox = gtk.VBox()
        hbox.show()
        hbox.pack_start(self.escala)
        hbox.pack_start(self.lblsize)

        fs_container = frame_fs(self, self.lista, self.particion_act)
        self.cmb_tipo = fs_container.cmb_tipo

        self.cmb_fs = fs_container.cmb_fs
        self.cmb_fs.connect('changed', self.cmb_fs_changed)

        self.cmb_montaje = fs_container.cmb_montaje
        self.entrada = fs_container.entrada
        fs_container.formatear.set_active(True)
        fs_container.formatear.set_sensitive(False)

        # Contenedor General
        self.cont = gtk.VBox()
        self.cont.pack_start(lbl_tamano)
        self.cont.pack_start(hbox, padding=15)
        self.cont.pack_start(fs_container)
        self.cont.show()
        self.vbox.pack_start(self.cont)

        response = self.run()
        self.process_response(response)

    def process_response(self, response=None):

        if not response:
            return response

        if response == gtk.RESPONSE_OK:
            tipo = self.cmb_tipo.get_active_text()
            formato = self.cmb_fs.get_active_text()
            montaje = self.cmb_montaje.get_active_text()
            usado = humanize(0)

            # Calculo el tamaño
            inicio = self.inicio_part
            fin = self.escala.get_value()
            tamano = humanize(fin - inicio)
            libre = tamano

            if formato == 'swap':
                montaje = 'swap'

            if montaje == 'Escoger manualmente...':
                montaje = self.entrada.get_text().strip()

            print "---NUEVA----"
            # Primaria
            if tipo == msj.particion.primaria:
                print "Partición primaria"
                self.add_partition_to_list(tipo, formato, montaje, tamano, \
                    usado, libre, inicio + self.sector, fin)
                if fin != self.fin_part:
                    print "Que deja espacio libre"
                    inicio = self.escala.get_value()
                    fin = self.fin_part
                    tamano = humanize(fin - inicio)
                    libre = tamano
                    self.add_partition_to_list(tipo, msj.particion.libre, \
                        montaje, tamano, usado, libre, inicio , \
                        fin)
            # Extendida
            elif tipo == msj.particion.extendida:
                print "Partición Extendida"
                usado = tamano
                libre = humanize(0)
                self.add_partition_to_list(tipo, formato, montaje, tamano, \
                    usado, libre, inicio + self.sector, fin)
                print "Crea vacío interno"
                self.add_partition_to_list(msj.particion.logica, \
                    msj.particion.libre, montaje, tamano, usado, libre, \
                    inicio + 1, fin) # agregamos +1 al inicio para que la lista no se desordene
                if fin != self.fin_part:
                    print "Y deja espacio libre"
                    inicio = self.escala.get_value()
                    fin = self.fin_part
                    tamano = humanize(fin - inicio)
                    libre = tamano
                    self.add_partition_to_list(msj.particion.primaria, \
                        msj.particion.libre, montaje, tamano, usado, libre, \
                        inicio , fin)
            # Lógica
            elif tipo == msj.particion.logica:
                print "Partición Lógica"
                self.add_partition_to_list(tipo, formato, montaje, tamano, \
                    usado, libre, inicio + self.sector * 4, fin)
                if fin != self.fin_part:
                    print "Que deja espacio extendido libre"
                    inicio = self.escala.get_value()
                    fin = self.fin_part
                    tamano = humanize(fin - inicio)
                    libre = tamano
                    self.add_partition_to_list(tipo, msj.particion.libre, \
                        montaje, tamano, usado, libre, \
                        inicio , fin)
            print "------------"

        self.destroy()
        return response

    def add_partition_to_list(self, tipo, formato, montaje, tamano, usado,
                        libre, inicio, fin):
        disp = self.disco
        crear_accion = True
        formatear = False
        # Si es espacio libre
        if formato == msj.particion.libre:
            crear_accion = False
            pop = False
            disp = ''
            montaje = ''
            usado = humanize(0)
            libre = tamano
        # Si NO es espacio libre
        else:
            pop = True
            formatear = True
            if tipo == msj.particion.extendida:
                formato = ''
                montaje = ''

        if montaje == 'Ninguno': montaje = ''

        # Entrada de la particion para la tabla
        particion = [disp, tipo, formato, montaje, tamano, usado, libre, \
            inicio, fin, formatear, PStatus.NEW]

        # Crea la acción correspondiente que va ejecutarse
        if crear_accion:
            self.acciones.append(['crear', disp, montaje, inicio, fin, formato,
                msj.particion.get_tipo_orig(tipo), 0])

        self.lista = set_partition(self.lista, self.particion_act, particion, \
            pop)

    def escala_on_changed(self, widget=None):
        formato = self.cmb_fs.get_active_text()
        tamano = widget.get_value() - self.inicio_part

        # Impide que se sobrepasen los maximos y minimos
        if not validate_minimun_fs_size(formato, tamano):
            widget.set_value(self.inicio_part + FSMIN[formato])
        elif not validate_maximun_fs_size(formato, tamano):
            widget.set_value(self.inicio_part + FSMAX[formato])

        if self.cmb_fs:
            self.lblsize.set_text(humanize(widget.get_value() - self.inicio_part))

    def cmb_fs_changed(self, widget):
        self.validate_fs_size()

    def validate_fs_size(self):
        formato = self.cmb_fs.get_active_text()
        tamano = self.particion_act[TblCol.FIN] - self.particion_act[TblCol.INICIO]
        estatus = True

        if not validate_minimun_fs_size(formato, tamano):
            estatus = False
            msg = "%s debe tener un tamaño mínimo de %s." % (formato, humanize(FSMIN[formato]))
            UserMessage(msg, 'Información', gtk.MESSAGE_INFO, gtk.BUTTONS_OK)
            self.escala.set_value(self.inicio_part + FSMIN[formato])

        if not validate_maximun_fs_size(formato, tamano):
            estatus = False
            msg = "%s debe tener un tamaño máximo de %s." % (formato, humanize(FSMAX[formato]))
            UserMessage(msg, 'Información', gtk.MESSAGE_INFO, gtk.BUTTONS_OK)
            self.escala.set_value(self.inicio_part + FSMAX[formato])

        return estatus
