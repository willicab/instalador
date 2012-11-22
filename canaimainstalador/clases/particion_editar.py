#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ==============================================================================
# PAQUETE: canaima-instalador
# ARCHIVO: canaimainstalador/clases/particion_editar.py
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

from canaimainstalador.clases.common import TblCol, get_row_index, PStatus, \
    validate_maximun_fs_size, validate_minimun_fs_size, UserMessage, humanize
from canaimainstalador.clases.frame_fs import frame_fs
from canaimainstalador.translator import msj
from canaimainstalador.config import FSMIN, FSMAX

txt_manual = 'Escoger manualmente...'
txt_ninguno = 'Ninguno'

class Main(gtk.Dialog):

    def __init__(self, lista, fila_selec, acciones):
        self.lista = lista
        self.particion_act = fila_selec
        self.acciones = acciones
        self.disco = fila_selec[TblCol.DISPOSITIVO]

        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        self.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.set_title("Editar partición existente")
        self.set_resizable(0)

        self.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        self.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        self.set_default_response(gtk.RESPONSE_CANCEL)

        self.fs_box = frame_fs(self, self.lista, self.particion_act)
        self.fill_fields()

        self.vbox.pack_start(self.fs_box)

        response = self.run()
        self.process_response(response)

    def fill_fields(self):

        # Tipo
        self.fs_box.cmb_tipo.insert_text(0, self.particion_act[TblCol.TIPO])
        self.fs_box.cmb_tipo.set_active(0)
        self.fs_box.cmb_tipo.set_sensitive(False)

        # Filesystem
        self.select_item(self.fs_box.cmb_fs, self.particion_act[TblCol.FORMATO])
        self.fs_box.cmb_fs.connect('changed', self.cmb_fs_changed)

        # Montaje
        montaje = self.particion_act[TblCol.MONTAJE]
        if montaje == '': montaje = txt_ninguno
        try:
            self.select_item(self.fs_box.cmb_montaje, montaje)
        except ValueError, e:
            print e
            self.select_item(self.fs_box.cmb_montaje, txt_manual)
            self.fs_box.entrada.set_text(montaje)

        # Formatear
        self.set_format_label(self.particion_act[TblCol.FORMATO])
        self.fs_box.formatear.set_active(self.particion_act[TblCol.FORMATEAR])

    def select_item(self, combo, item):

        # Si la ṕarticion es desconocida selecciona un valor por defecto
        if item == msj.particion.desconocida:
            item = 'ext4'

        for row in combo.get_model():
            index = row.path[0]
            text = row[0]
            if item == text:
                combo.set_active(index)
                return

        raise ValueError("No se ha encontado el item '%s'" % item)

    def process_response(self, response):

        if response == gtk.RESPONSE_OK:
            i = get_row_index(self.lista, self.particion_act)
            tmp = self.lista[i]
            filesystem = self.fs_box.cmb_fs.get_active_text()
            formatear = self.fs_box.formatear.get_active()
            montaje = self.fs_box.cmb_montaje.get_active_text()

            if montaje == txt_manual:
                montaje = self.fs_box.entrada.get_text().strip()
            elif montaje == txt_ninguno:
                montaje = ''

            tmp[TblCol.FORMATO] = filesystem
            tmp[TblCol.MONTAJE] = montaje
            tmp[TblCol.FORMATEAR] = formatear

            if tmp != list(self.particion_act):

                tmp[TblCol.ESTADO] = PStatus.USED
                self.lista[i] = tmp

                disco = tmp[TblCol.DISPOSITIVO]
                montaje = tmp[TblCol.MONTAJE]
                inicio = tmp[TblCol.INICIO]
                fin = tmp[TblCol.FIN]
                formato = tmp[TblCol.FORMATO]
                tipo = tmp[TblCol.TIPO]

                if formatear:
                    accion = 'formatear'
                else:
                    accion = 'usar'

                self.acciones.append([accion, disco, montaje, inicio, fin, \
                    formato, msj.particion.get_tipo_orig(tipo), 0])

        self.destroy()

    def set_format_label(self, fs):
        if fs == 'swap' and self.particion_act[TblCol.FORMATO] == 'swap':
            self.fs_box.formatear.set_label("Usar esta partición")
        else:
            self.fs_box.formatear.set_label("Formatear esta partición")

    def cmb_fs_changed(self, widget):

        selec = widget.get_active_text()
        self.set_format_label(selec)

        if not self.validate_fs_size():
            self.fs_box.cmb_fs.set_active(3)

        actual = self.particion_act[TblCol.FORMATO]
        formatear = self.particion_act[TblCol.FORMATEAR]

        # Si el filesystem seleccionado es el mismo que tiene la particion
        # se coloca el estado original que trae de la variable formatear
        # sino hay que formatear obligatoramente y no se debe editar ese campo
        if selec == actual:
            self.fs_box.formatear.set_active(formatear)
            self.fs_box.formatear.set_sensitive(True)
        else:
            self.fs_box.formatear.set_active(True)
            self.fs_box.formatear.set_sensitive(False)

    def validate_fs_size(self):
        formato = self.fs_box.cmb_fs.get_active_text()
        tamano = self.particion_act[TblCol.FIN] - self.particion_act[TblCol.INICIO]
        estatus = True

        if not validate_minimun_fs_size(formato, tamano):
            estatus = False
            msg = "%s debe tener un tamaño mínimo de %s." % (formato, humanize(FSMIN[formato]))
            UserMessage(msg, 'Información', gtk.MESSAGE_INFO, gtk.BUTTONS_OK)

        if not validate_maximun_fs_size(formato, tamano):
            estatus = False
            msg = "%s debe tener un tamaño máximo de %s." % (formato, humanize(FSMAX[formato]))
            UserMessage(msg, 'Información', gtk.MESSAGE_INFO, gtk.BUTTONS_OK)

        return estatus

