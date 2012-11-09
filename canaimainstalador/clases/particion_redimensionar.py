#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ==============================================================================
# PAQUETE: canaima-instalador
# ARCHIVO: canaimainstalador/pasos/particion_redimensionar.py
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
from canaimainstalador.clases.common import humanize, TblCol, floatify, PStatus, \
    get_sector_size, has_next_row, is_free, get_row_index, get_next_row, \
    validate_minimun_fs_size, validate_maximun_fs_size
from canaimainstalador.translator import msj
from copy import copy
from canaimainstalador.config import FSMIN, FSMAX, ESPACIO_USADO_EXTRA

class Main(gtk.Dialog):

    def __init__(self, disco, lista, fila, acciones):
        self.sector = get_sector_size(disco)
        self.lista = lista
        self.acciones = acciones
        self.num_fila_act = get_row_index(lista, fila)
        self.dispositivo = fila[TblCol.DISPOSITIVO]
        self.formato = fila[TblCol.FORMATO]
        self.inicio = fila[TblCol.INICIO]
        self.fin = fila[TblCol.FIN]
        self.usado = floatify(fila[TblCol.USADO])

        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        gtk.Window.set_position(self, gtk.WIN_POS_CENTER_ALWAYS)

        self.set_title("Redimensionar Partición")
        self.set_size_request(400, 200)
        self.set_resizable(0)

        self.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        self.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        self.set_response_sensitive(gtk.RESPONSE_OK, False)
        self.set_default_response(gtk.RESPONSE_CANCEL)

        self.escala = gtk.HScale()
        self.escala.set_draw_value(False)
        adj = gtk.Adjustment(self.fin,
                            self.inicio,
                            self.get_maximum_size(),
                            1.0,
                            1024.0,
                            0.0)
        adj.connect("value-changed", self.escala_value_changed)
        self.escala.set_adjustment(adj)
        self.escala.show()

        self.lbl_dispositivo = gtk.Label("Partición '%s'" % self.dispositivo)
        self.lbl_dispositivo.show()

        self.lbl_tamano = gtk.Label('Tamaño')
        self.lbl_tamano_num = gtk.Label(humanize(self.get_new_partition_size()))
        self.vb_tamano = gtk.VBox()
        self.vb_tamano.add(self.lbl_tamano)
        self.vb_tamano.add(self.lbl_tamano_num)
        self.vb_tamano.show_all()

        self.lbl_usado = gtk.Label('Usado')
        self.lbl_usado_num = gtk.Label(humanize(self.usado))
        self.vb_usado = gtk.VBox()
        self.vb_usado.add(self.lbl_usado)
        self.vb_usado.add(self.lbl_usado_num)
        self.vb_usado.show_all()

        self.lbl_libre = gtk.Label('Libre')
        self.lbl_libre_num = gtk.Label(humanize(self.get_free_space()))
        self.vb_libre = gtk.VBox()
        self.vb_libre.add(self.lbl_libre)
        self.vb_libre.add(self.lbl_libre_num)
        self.vb_libre.show_all()

        self.lbl_sin_particion = gtk.Label('Sin Particionar')
        self.lbl_sin_particion_num = gtk.Label(humanize(self.get_unasigned_space()))
        self.vb_sin_particion = gtk.VBox()
        self.vb_sin_particion.add(self.lbl_sin_particion)
        self.vb_sin_particion.add(self.lbl_sin_particion_num)
        self.vb_sin_particion.show_all()

        self.hb_leyenda = gtk.HBox()
        self.hb_leyenda.add(self.vb_tamano)
        self.hb_leyenda.add(self.vb_usado)
        self.hb_leyenda.add(self.vb_libre)
        self.hb_leyenda.add(self.vb_sin_particion)
        self.hb_leyenda.show_all()

        self.cont = gtk.VBox()
        self.cont.add(self.lbl_dispositivo)
        self.cont.add(self.hb_leyenda)
        self.cont.add(self.escala)
        self.cont.show()

        self.vbox.pack_start(self.cont)

        self.process_response(self.run())

    def get_new_partition_size(self):
        'Retorna el tamaño de la nueva partición'
        return self.escala.get_value() - self.inicio

    def get_used_space(self):
        'El tamaño minimo al que se puede redimensionar la partición'
        return self.inicio + self.usado + ESPACIO_USADO_EXTRA

    def get_maximum_size(self):
        'El tamaño maximo al que se puede redimensionar la partición'
        return self.fin + self.get_next_available_space()

    def get_free_space(self):
        'Retorna el espacio libre de la partición'
        return self.escala.get_value() - self.get_used_space()

    def get_unasigned_space(self):
        'Retorna el espacio sin particionar que va quedando al redimensionar'
        return self.get_maximum_size() - self.escala.get_value()

    def get_next_free_partition(self):
        '''Retorna la fila siguiente si existe y se trata de un espacio libre,
        sino retorna None'''
        if has_next_row(self.lista, self.num_fila_act):
            actual_row = self.lista[self.num_fila_act]
            next_row = get_next_row(self.lista, None, self.num_fila_act)
            # Si la particion es del mismo tipo (Extendida o Primaria)
            # Y se trata de un espacio libre
            if actual_row[TblCol.TIPO] == next_row[TblCol.TIPO] \
            and is_free(next_row):
                return next_row
        return None

    def get_next_available_space(self):
        '''Retona la cantidad de espacio sin particionar que hay luego de la
        particion'''
        next_row = self.get_next_free_partition()
        if next_row != None:
            return next_row[TblCol.FIN] - next_row[TblCol.INICIO]
        else:
            return 0

    def escala_value_changed(self, adjustment):
        'Acciones a tomar cuando se mueve el valor de la escala'

        # No reducir menos del espacio minimo
        tamano = adjustment.value - self.inicio
        if not validate_minimun_fs_size(self.formato, tamano):
            adjustment.set_value(self.inicio + FSMIN[self.formato])
        elif not validate_maximun_fs_size(self.formato, tamano):
            adjustment.set_value(self.inicio + FSMAX[self.formato])
        # No reducir menos del espacio usado
        elif adjustment.value <= self.get_used_space():
            adjustment.set_value(self.get_used_space())

        # Activa el boton de aceptar sólo si se ha modificado el valor
        if adjustment.value == self.fin:
            self.set_response_sensitive(gtk.RESPONSE_OK, False)
        else:
            self.set_response_sensitive(gtk.RESPONSE_OK, True)

        # Actualizar los textos con los valores
        self.lbl_tamano_num.set_text(humanize(self.get_new_partition_size()))
        self.lbl_libre_num.set_text(humanize(self.get_free_space()))
        self.lbl_sin_particion_num.set_text(humanize(self.get_unasigned_space()))

    def process_response(self, response=None):

        if not response:
            return response

        part_actual = self.lista[self.num_fila_act]
        original = copy(part_actual)
        part_sig = self.get_next_free_partition()

        if response == gtk.RESPONSE_OK:

            part_actual[TblCol.FIN] = self.escala.get_value()
            part_actual[TblCol.TAMANO] = humanize(self.get_new_partition_size())
            part_actual[TblCol.LIBRE] = humanize(self.get_free_space())
            part_actual[TblCol.ESTADO] = PStatus.REDIM

            # Si dejamos espacio libre
            if part_actual[TblCol.FIN] < self.get_maximum_size():
                # Si hay particion libre siguiente, solo modificamos algunos
                # valores
                if part_sig:
                    part_sig[TblCol.INICIO] = part_actual[TblCol.FIN] + self.sector
                    tamano = humanize(
                                part_sig[TblCol.FIN] - part_sig[TblCol.INICIO])
                    part_sig[TblCol.TAMANO] = tamano
                    part_sig[TblCol.LIBRE] = tamano
                    part_sig[TblCol.ESTADO] = PStatus.FREED
                    self.lista[self.num_fila_act + 1] = part_sig
                # Si no hay particion siguiente, tenemos que crear toda la fila
                else:
                    part_sig = list(range(len(part_actual)))
                    part_sig[TblCol.DISPOSITIVO] = ''
                    part_sig[TblCol.TIPO] = part_actual[TblCol.TIPO]
                    part_sig[TblCol.FORMATO] = msj.particion.libre
                    part_sig[TblCol.MONTAJE] = ''
                    part_sig[TblCol.TAMANO] = humanize(self.get_unasigned_space())
                    part_sig[TblCol.USADO] = humanize(0)
                    part_sig[TblCol.LIBRE] = humanize(self.get_unasigned_space())
                    part_sig[TblCol.INICIO] = part_actual[TblCol.FIN] + self.sector
                    part_sig[TblCol.FIN] = self.get_maximum_size()
                    part_sig[TblCol.FORMATEAR] = False
                    part_sig[TblCol.ESTADO] = PStatus.FREED
                    tmp = []
                    for i in range(len(self.lista)):
                        if i == self.num_fila_act:
                            tmp.append(part_actual)
                            tmp.append(part_sig)
                        else:
                            tmp.append(self.lista[i])
                    self.lista = tmp

            # Sino dejamos espacio libre
            elif part_sig:
                self.lista.remove(part_sig)

            self.acciones.append([
              'redimensionar',
              part_actual[TblCol.DISPOSITIVO],
              part_actual[TblCol.MONTAJE],
              part_actual[TblCol.INICIO],
              original[TblCol.FIN], # Fin original
              part_actual[TblCol.FORMATO],
              msj.particion.get_tipo_orig(part_actual[TblCol.TIPO]),
              part_actual[TblCol.FIN], # Nuevo Fin
            ])
        self.destroy()
        return response
