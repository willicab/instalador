#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ==============================================================================
# PAQUETE: canaima-instalador
# ARCHIVO: canaimainstalador/clases/particion_eliminar.py
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
from copy import copy

from canaimainstalador.clases.common import get_row_index, TblCol, has_next_row, \
    is_primary, is_logic, humanize, PStatus, is_free, UserMessage
from canaimainstalador.translator import msj

class Main():

    def __init__(self, lista, fila_selec, acciones):
        self.lista = lista
        self.fila_selec = fila_selec
        self.acciones = acciones
        self.disco = fila_selec[TblCol.DISPOSITIVO]

        if is_primary(self.fila_selec, False) or is_logic(self.fila_selec):
            self.delete_partition(self.fila_selec)
        else:
            is_clean = True
            for partition in self.lista:
                if is_logic(partition) and not is_free(partition):
                    message = "Debe borrar primero las particiones lógicas."
                    UserMessage(message, 'ERROR', gtk.MESSAGE_ERROR, gtk.BUTTONS_OK)
                    is_clean = False
                    break;
            if is_clean:
                i = get_row_index(self.lista, self.fila_selec)
                free = self.lista[i + 1]
                self.delete_partition(self.fila_selec)
                free[TblCol.TIPO] = msj.particion.primaria
                self.delete_partition(free)

    def delete_partition(self, part):
        'Ejecuta el proceso de eliminar la particion de la lista'
        i = get_row_index(self.lista, part)
        particion = self.lista[i]
        inicio = particion[TblCol.INICIO]
        fin = particion[TblCol.FIN]
        del_sig = del_ant = False

        # Si tiene una fila anterior
        if i > 0:
            p_anterior = self.lista[i - 1]
            if self.is_summable(p_anterior, particion):
                del_ant = True
                inicio = p_anterior[TblCol.INICIO]
        # si tiene una fila siguiente
        if has_next_row(self.lista, i):
            p_siguiente = self.lista[i + 1]
            if self.is_summable(p_siguiente, particion):
                del_sig = True
                fin = p_siguiente[TblCol.FIN]

        tamano = fin - inicio

        temp = copy(particion)
        temp[TblCol.DISPOSITIVO] = ''
        # Validar de que tipo quedará la particion libre
        if is_primary(temp):
            temp[TblCol.TIPO] = msj.particion.primaria
        elif is_logic(temp):
            temp[TblCol.TIPO] = msj.particion.logica
        temp[TblCol.FORMATO] = msj.particion.libre
        temp[TblCol.MONTAJE] = ''
        temp[TblCol.TAMANO] = humanize(tamano)
        temp[TblCol.USADO] = humanize(0)
        temp[TblCol.LIBRE] = humanize(tamano)
        temp[TblCol.INICIO] = inicio
        temp[TblCol.FIN] = fin
        temp[TblCol.FORMATEAR] = False
        temp[TblCol.ESTADO] = PStatus.FREED

        # Sustituimos con los nuevos valores
        self.lista[i] = temp
        # Borramos los esṕacios vacios contiguos si existieren
        if del_sig:
            del self.lista[i + 1]
        if del_ant:
            del self.lista[i - 1]

        # Si lo que se estaeliminando no es un espacio libre
        if not is_free(particion):
            # Agregamos la accion correspondiente
            self.acciones.append(['borrar',
                                  self.disco,
                                  None,
                                  particion[TblCol.INICIO],
                                  particion[TblCol.FIN],
                                  particion[TblCol.FORMATO],
                                  msj.particion.get_tipo_orig(particion[TblCol.TIPO]),
                                  0])

    def is_summable(self, otra, actual):
        '''Indica si se puede sumar el tamaño de las particiones si se trata \
        del mismo tipo (primaria o lógica)'''
        # Si la particion es libre
        if otra[TblCol.FORMATO] == msj.particion.libre:
            # Si ambas son primarias
            # o ambas son logicas
            if (is_primary(actual) and is_primary(otra)) \
            or (is_logic(actual) and is_logic(otra)):
                return True
        return False
