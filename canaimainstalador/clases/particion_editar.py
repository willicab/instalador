#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# =============================================================================
# PAQUETE: canaima-instalador
# ARCHIVO: canaimainstalador/clases/particion_editar.py
# COPYRIGHT:
#       (C) 2012 William Abrahan Cabrera Reyes <william@linux.es>
#       (C) 2012 Erick Manuel Birbe Salazar <erickcion@gmail.com>
#       (C) 2012 Luis Alejandro Martínez Faneyth <luis@huntingbears.com.ve>
# LICENCIA: GPL-3
# =============================================================================
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

from canaimainstalador.clases.common import TblCol, get_row_index, PStatus, \
    validate_maximun_fs_size, validate_minimun_fs_size, UserMessage, humanize
from canaimainstalador.clases.frame_fs import frame_fs, MSG_ENTER_MANUAL, \
    MSG_NONE
from canaimainstalador.config import FSMIN, FSMAX
from canaimainstalador.translator import msj, gettext_install
from gi.repository import Gtk


gettext_install()


class Main(Gtk.Dialog):

    def __init__(self, lista, fila_selec, acciones):
        self.lista = lista
        self.particion_act = fila_selec
        self.acciones = acciones
        self.disco = fila_selec[TblCol.DISPOSITIVO]

        Gtk.Window.__init__(self, Gtk.WindowType.TOPLEVEL)
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.set_title(_("Edit existing partition"))
        self.set_resizable(0)

        self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.CANCEL)

        self.fs_box = frame_fs(self, self.lista, self.particion_act)
        self.fill_fields()

        self.vbox.pack_start(self.fs_box, True, True, 0)

        response = self.run()
        self.process_response(response)

    def fill_fields(self):

        # Tipo
        self.fs_box.cmb_tipo.insert_text(0, self.particion_act[TblCol.TIPO])
        self.fs_box.cmb_tipo.set_active(0)
        self.fs_box.cmb_tipo.set_sensitive(False)

        # Filesystem
        self.select_item(self.fs_box.cmb_fs,
                         self.particion_act[TblCol.FORMATO])
        self.fs_box.cmb_fs.connect('changed', self.cmb_fs_changed)

        # Montaje
        montaje = self.particion_act[TblCol.MONTAJE]
        if montaje == '':
            montaje = MSG_NONE
        try:
            self.select_item(self.fs_box.cmb_montaje, montaje)
        except ValueError, e:
            print e
            self.select_item(self.fs_box.cmb_montaje, MSG_ENTER_MANUAL)
            self.fs_box.entrada.set_text(montaje)

        # Formatear
        self.set_format_label(self.particion_act[TblCol.FORMATO])
        self.fs_box.formatear.set_active(self.particion_act[TblCol.FORMATEAR])

    def select_item(self, combo, item):

        # Si la ṕarticion es desconocida selecciona un valor por defecto
        if item == msj.particion.desconocida:
            item = 'ext4'

        for row in combo.get_model():
            index = row.path.get_indices()[0]
            text = row[0]
            if item == text:
                combo.set_active(index)
                return

        raise ValueError("No se ha encontado el item '%s'" % item)

    def process_response(self, response):

        if response == Gtk.ResponseType.OK:
            i = get_row_index(self.lista, self.particion_act)
            tmp = self.lista[i]
            filesystem = self.fs_box.cmb_fs.get_active_text()
            formatear = self.fs_box.formatear.get_active()
            montaje = self.fs_box.cmb_montaje.get_active_text()

            if montaje == MSG_ENTER_MANUAL:
                montaje = self.fs_box.entrada.get_text().strip()
            elif montaje == MSG_NONE:
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
            self.fs_box.formatear.set_label(_("Use this partition"))
        else:
            self.fs_box.formatear.set_label(_("Format this partition"))

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
        tamano = self.particion_act[TblCol.FIN] \
        - self.particion_act[TblCol.INICIO]
        estatus = True

        if not validate_minimun_fs_size(formato, tamano):
            estatus = False
            msg = _("{0} must have a minimum size of {1}.")\
            .format(formato, humanize(FSMIN[formato]))
            UserMessage(msg, 'Información', Gtk.MessageType.INFO, Gtk.ButtonsType.OK)

        if not validate_maximun_fs_size(formato, tamano):
            estatus = False
            msg = _("{0} must have a maximum size of {1}.")\
            .format(formato, humanize(FSMAX[formato]))
            UserMessage(msg, _('Information'), Gtk.MessageType.INFO,
                        Gtk.ButtonsType.OK)

        return estatus
