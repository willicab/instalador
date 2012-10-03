# -*- coding: utf-8 -*-
#
# ==============================================================================
# PAQUETE: canaima-instalador
# ARCHIVO: canaimainstalador/translator.py
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

import gtk

from canaimainstalador.clases.common import humanize, TblCol, get_next_row, \
    get_row_index, set_partition, PStatus, get_sector_size
from canaimainstalador.translator import msj
from canaimainstalador.clases.frame_fs import frame_fs

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
        hbox = gtk.HBox()
        hbox.show()
        lbl = gtk.Label('Tamaño')
        lbl.set_alignment(0, 0.5)
        lbl.show()
        hbox.add(lbl)
        adj = gtk.Adjustment(self.fin_part, self.inicio_part, self.fin_part, \
                             1.0, 5.0, 0.0)
        self.escala = gtk.HScale()
        self.escala.set_digits(0)
        self.escala.set_draw_value(False)
        self.escala.set_adjustment(adj)
        self.escala.set_size_request(250, 30)
        self.escala.connect("value-changed", self.escala_on_changed)
        self.escala.show()
        hbox.add(self.escala)

        self.lblsize = gtk.Label(humanize(self.escala.get_value() - \
                                          self.inicio_part))
        self.lblsize.set_alignment(0, 0.5)
        self.lblsize.show()
        hbox.add(self.lblsize)

        fs_container = frame_fs(self, self.lista, self.particion_act)
        self.cmb_tipo = fs_container.cmb_tipo
        self.cmb_fs = fs_container.cmb_fs
        self.cmb_montaje = fs_container.cmb_montaje
        self.entrada = fs_container.entrada

        # Contenedor General
        self.cont = gtk.VBox()
        self.cont.add(hbox)
        self.cont.add(fs_container)
        self.cont.show()
        self.vbox.pack_start(self.cont)

        response = self.run()
        self.procesar_respuesta(response)

    def procesar_respuesta(self, response=None):

        if not response:
            return response

        if response == gtk.RESPONSE_OK:
            tipo = self.cmb_tipo.get_active_text()
            formato = self.cmb_fs.get_active_text()
            montaje = self.cmb_montaje.get_active_text()
            usado = humanize(0)

            if formato == 'swap':
                montaje = ''

            if montaje == 'Escoger manualmente...':
                montaje = self.entrada.get_text().strip()

            # Calculo el tamaño
            inicio = self.inicio_part
            fin = self.escala.get_value()
            tamano = humanize(fin - inicio)
            libre = tamano

            print "---NUEVA----"
            # Primaria
            if tipo == msj.particion.primaria:
                print "Partición primaria"
                self.crear_particion(tipo, formato, montaje, tamano, usado, \
                                     libre, inicio, fin)
                if fin != self.fin_part:
                    print "Que deja espacio libre"
                    inicio = self.escala.get_value()
                    fin = self.fin_part
                    tamano = humanize(fin - inicio)
                    libre = tamano
                    self.crear_particion(tipo, msj.particion.libre, montaje, \
                                         tamano, usado, libre, inicio + self.sector, \
                                         fin)
            # Extendida
            elif tipo == msj.particion.extendida:
                print "Partición Extendida"
                usado = tamano
                libre = humanize(0)
                self.crear_particion(tipo, formato, montaje, tamano, usado, \
                                     libre, inicio, fin)
                print "Crea vacío interno"
                self.crear_particion(msj.particion.logica, msj.particion.libre, \
                                     montaje, tamano, usado, libre, \
                                     inicio + self.sector * 2, fin)
                if fin != self.fin_part:
                    print "Y deja espacio libre"
                    inicio = self.escala.get_value()
                    fin = self.fin_part
                    tamano = humanize(fin - inicio)
                    libre = tamano
                    self.crear_particion(msj.particion.primaria, \
                                         msj.particion.libre, montaje, tamano, \
                                         usado, libre, inicio + self.sector, fin)
            # Lógica
            elif tipo == msj.particion.logica:
                print "Partición Lógica"
                self.crear_particion(tipo, formato, montaje, tamano, usado, \
                                     libre, inicio, fin)
                if fin != self.fin_part:
                    print "Que deja espacio extendido libre"
                    inicio = self.escala.get_value()
                    fin = self.fin_part
                    tamano = humanize(fin - inicio)
                    libre = tamano
                    self.crear_particion(tipo, msj.particion.libre, montaje, \
                                         tamano, usado, libre, inicio + self.sector \
                                         * 2, fin)
            print "------------"

        self.destroy()
        return response

    def crear_particion(self, tipo, formato, montaje, tamano, usado,
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
        # Si NO es espacio libre
        else:
            pop = True
            formatear = True
            if tipo == msj.particion.extendida:
                formato = ''
                montaje = ''

        # Entrada de la particion para la tabla
        particion = [disp, tipo, formato, montaje, tamano, usado, libre, \
                     inicio, fin, formatear, PStatus.NEW]

        # Crea la acción correspondiente que va ejecutarse
        if crear_accion:
            self.acciones.append(['crear', disp, montaje, inicio, fin, \
                                  formato, msj.particion.get_tipo_orig(tipo),
                                  0])

        self.lista = set_partition(self.lista, self.particion_act, particion, \
                                   pop)

    def escala_on_changed(self, widget=None):
        self.lblsize.set_text(humanize(widget.get_value() - self.inicio_part))
