#-*- coding: UTF-8 -*-
'''
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Ucumari; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA

Created on 24/09/2012

@author: Erick Birbe <erickcion@gmail.com>
'''
import gtk
from canaimainstalador.clases.common import TblCol, get_row_index
from canaimainstalador.clases.frame_fs import frame_fs

txt_manual = 'Escoger manualmente...'
txt_ninguno = 'Ninguno'

class Main(gtk.Dialog):

    def __init__(self, lista, fila_selec, acciones):
        self.lista = lista
        self.fila_selec = fila_selec
        self.acciones = acciones
        self.disco = fila_selec[TblCol.DISPOSITIVO]

        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        self.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.set_title("Usar partición existente")
        self.set_resizable(0)

        self.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        self.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        self.set_default_response(gtk.RESPONSE_CANCEL)

        self.fs_box = frame_fs(self, self.lista, self.fila_selec)
        self.llenar_campos()

        self.vbox.pack_start(self.fs_box)

        response = self.run()
        self.procesar_respuesta(response)

    def llenar_campos(self):

        # Tipo
        self.fs_box.cmb_tipo.insert_text(0, self.fila_selec[TblCol.TIPO])
        self.fs_box.cmb_tipo.set_active(0)
        self.fs_box.cmb_tipo.set_sensitive(False)

        # Filesystem
        self.select_item(self.fs_box.cmb_fs, self.fila_selec[TblCol.FORMATO])
        self.fs_box.cmb_fs.set_sensitive(False)

        # Montaje
        montaje = self.fila_selec[TblCol.MONTAJE]
        if montaje == '':
            montaje = txt_ninguno
        try:
            self.select_item(self.fs_box.cmb_montaje, montaje)
        except ValueError, e:
            print e
            self.select_item(self.fs_box.cmb_montaje, txt_manual)
            self.fs_box.entrada.set_text(montaje)

        # Formatear
        self.fs_box.formatear.set_active(self.fila_selec[TblCol.FORMATEAR])

    def select_item(self, combo, item):
        for row in combo.get_model():
            index = row.path[0]
            text = row[0]
            if item == text:
                combo.set_active(index)
                return
        raise ValueError("No se ha encontado el item '%s'" % item)

    def procesar_respuesta(self, response):

        if response == gtk.RESPONSE_OK:
            i = get_row_index(self.lista, self.fila_selec)
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

            if tmp != self.fila_selec:
                self.lista[i] = tmp
                disco = tmp[TblCol.DISPOSITIVO]
                montaje = tmp[TblCol.MONTAJE]
                inicio = tmp[TblCol.INICIO]
                fin = tmp[TblCol.FIN]
                formato = tmp[TblCol.FORMATO]
                tipo = tmp[TblCol.TIPO]
                self.acciones.append(['usar', disco, montaje, inicio, fin, \
                                      formato, tipo])

        self.destroy()


