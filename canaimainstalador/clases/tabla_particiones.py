#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ==============================================================================
# PAQUETE: canaima-instalador
# ARCHIVO: canaimainstalador/clases/tabla_particiones.py
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

from canaimainstalador.clases.common import TblCol

class TablaParticiones (gtk.TreeView):

    liststore = None
    columnas = {}
    ultima_fila_seleccionada = None

    def __init__(self):

        # Tipos de valores a mostrar en la tabla
        self.liststore = gtk.ListStore(str, str, str, str, str, str, str, float, \
                                       float, bool, str)

        gtk.TreeView.__init__(self, model=self.liststore)
        self.set_headers_clickable(False)
        #self.connect("row-activated", self._accion_doble_click)
        self.connect("cursor-changed", self._accion_seleccionar)

        self.armar_tabla()

    def set_seleccionar(self, callback):
        'Determina la funcion que se ejecutará al hacer click'
        self.seleccionar = callback

    def _accion_seleccionar(self, treeview):
        '''Hace el llamado a la funcion indicada en set_seleccionar, pasandole
        los parametros correspondientes'''
        fila = self.get_fila_seleccionada()
        if fila != self.ultima_fila_seleccionada:
            self.ultima_fila_seleccionada = fila
        self.seleccionar(fila)

    def set_doble_click(self, callback):
        self.doble_click = callback

    def _accion_doble_click(self, treeview, path, column):
        modelo = treeview.get_model()
        fila = modelo.get(modelo.get_iter(path),

                          TblCol.DISPOSITIVO,
                          TblCol.TIPO,
                          TblCol.FORMATO,
                          TblCol.MONTAJE,
                          TblCol.TAMANO,
                          TblCol.USADO,
                          TblCol.LIBRE,
                          TblCol.INICIO,
                          TblCol.FIN,
                          TblCol.FORMATEAR,
                          TblCol.ESTADO)

        self.doble_click(fila)

    def get_fila_seleccionada(self):
        '''Obtiene la fila que esta seleccionada al momento de su llamado, si no
        hay filas seleccionadas retornará None'''

        obj_seleccion = self.get_selection().get_selected()
        modelo = obj_seleccion[0]
        iterador = obj_seleccion[1]

        if iterador != None:
            return modelo.get(iterador,
                              TblCol.DISPOSITIVO,
                              TblCol.TIPO,
                              TblCol.FORMATO,
                              TblCol.MONTAJE,
                              TblCol.TAMANO,
                              TblCol.USADO,
                              TblCol.LIBRE,
                              TblCol.INICIO,
                              TblCol.FIN,
                              TblCol.FORMATEAR,
                              TblCol.ESTADO)
        else:
            return None

    def armar_tabla(self):
        'Crea la tabla'

        # Columnas
        self.nueva_columna_texto("Dispositivo", TblCol.DISPOSITIVO)
        self.nueva_columna_texto("Tipo", TblCol.TIPO)
        self.nueva_columna_texto("Formato", TblCol.FORMATO)
        self.nueva_columna_texto("Montaje", TblCol.MONTAJE)
        self.nueva_columna_texto("Tamaño", TblCol.TAMANO)
        self.nueva_columna_texto("Usado", TblCol.USADO)
        self.nueva_columna_texto("Libre", TblCol.LIBRE)
        self.nueva_columna_texto("Inicio", TblCol.INICIO)
        self.nueva_columna_texto("Fin", TblCol.FIN)
        self.nueva_columna_check("Formatear", TblCol.FORMATEAR)
        self.nueva_columna_texto("Estado", TblCol.ESTADO)

        # Ocultar las columnas que no se desean mostrar
        self.columnas[TblCol.INICIO].set_visible(False)
        self.columnas[TblCol.FIN].set_visible(False)
        self.columnas[TblCol.ESTADO].set_visible(False)

    def nueva_columna_color(self, title, index):
        'Crea nueva columna de color en el TreeView'

        celda = gtk.CellRendererText()

        self.columnas[index] = gtk.TreeViewColumn(title, celda, text=index)
        self.columnas[index].set_reorderable(False)
        self.columnas[index].set_min_width(40)
        self.columnas[index].set_cell_data_func(celda, self.colorear_celda)

        self.insert_column(self.columnas[index], index)

    def nueva_columna_texto(self, title, index):
        'Crea nueva columna de texto en el TreeView'

        celda = gtk.CellRendererText()
        celda.set_property('cell-background-gdk', gtk.gdk.color_parse("#FFF"))

        self.columnas[index] = gtk.TreeViewColumn(title, celda, text=index)
        self.columnas[index].set_resizable(True)
        self.columnas[index].set_reorderable(False)

        #columna.connect("clicked", self.on_column_clicked, index)
        self.insert_column(self.columnas[index], index)

    def nueva_columna_check(self, title, index):
        'Crea nueva columna de seleccion en el TreeView'

        celda = gtk.CellRendererToggle()

        self.columnas[index] = gtk.TreeViewColumn(title, celda, active=index)
        self.columnas[index].set_resizable(False)
        self.columnas[index].set_reorderable(False)

        self.insert_column(self.columnas[index], index)

    def colorear_celda(self, columna, celda, modelo, iterad):
        color = modelo.get_value(iterad, 0)
        celda.set_property('background', color)
        celda.set_property('text', None)

    def agregar_fila(self, lista):
        'Agrega los datos a las filas'
        self.liststore.append([lista[TblCol.DISPOSITIVO],
                               lista[TblCol.TIPO],
                               lista[TblCol.FORMATO],
                               lista[TblCol.MONTAJE],
                               lista[TblCol.TAMANO],
                               lista[TblCol.USADO],
                               lista[TblCol.LIBRE],
                               lista[TblCol.INICIO],
                               lista[TblCol.FIN],
                               lista[TblCol.FORMATEAR],
                               lista[TblCol.ESTADO],
                              ])
