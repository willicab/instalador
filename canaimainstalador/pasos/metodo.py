#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ==============================================================================
# PAQUETE: canaima-instalador
# ARCHIVO: canaimainstalador/pasos/metodo.py
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

# Módulos globales
import gtk

# Módulos locales
from canaimainstalador.clases.particiones import Particiones
from canaimainstalador.clases.common import humanize, UserMessage
from canaimainstalador.clases.barra_particiones import BarraParticiones
from canaimainstalador.config import ESPACIO_TOTAL, CFG, FSPROGS

class PasoMetodo(gtk.Fixed):
    def __init__(self, CFG):
        gtk.Fixed.__init__(self)

        self.metodos = []
        self.minimo = ESPACIO_TOTAL
        self.part = Particiones()
        self.discos = self.part.lista_discos()
        print 'Se han encontrado los siguientes discos: {0}'.format(self.discos)

        self.lbl1 = gtk.Label('Seleccione el disco donde desea instalar el sistema:')
        self.lbl1.set_size_request(690, 20)
        self.lbl1.set_alignment(0, 0)
        self.put(self.lbl1, 0, 0)

        self.cmb_discos = gtk.combo_box_new_text()
        self.cmb_discos.set_size_request(690, 30)
        self.put(self.cmb_discos, 0, 25)
        self.cmb_discos.connect('changed', self.seleccionar_disco)

        for d in self.discos:
            self.cmb_discos.append_text(d)

        self.barra_part = BarraParticiones(self)
        self.barra_part.set_size_request(690, 100)
        self.put(self.barra_part, 0, 60)

        self.lbl2 = gtk.Label('Seleccione el método de instalación:')
        self.lbl2.set_size_request(690, 20)
        self.lbl2.set_alignment(0, 0)
        self.put(self.lbl2, 0, 165)

        self.cmb_metodo = gtk.combo_box_new_text()
        self.cmb_metodo.set_size_request(690, 30)
        self.put(self.cmb_metodo, 0, 190)
        self.cmb_metodo.connect('changed', self.establecer_metodo)

        self.lbl4 = gtk.Label()
        self.lbl4.set_size_request(690, 90)
        self.lbl4.set_alignment(0, 0)
        self.lbl4.set_line_wrap(True)
        self.put(self.lbl4, 0, 225)

        self.cmb_discos.set_active(0)

    def seleccionar_disco(self, widget=None):
        primarias = 0
        extendidas = 0
        logicas = 0
        self.metodos = []

        try:
            self.barra_part.expose()
        except:
            pass
        self.cmb_metodo.get_model().clear()
        self.cmb_metodo.set_sensitive(False)
        CFG['w'].siguiente.set_sensitive(False)
        self.lbl4.set_text('')

        self.disco = self.cmb_discos.get_active_text()
        print '{0} seleccionado'.format(self.disco)
        self.particiones = self.part.lista_particiones(self.disco)

        if len(self.particiones) == 0:
            UserMessage(
                    message='El disco {0} necesita una tabla de particiones para poder continuar con la instalación. ¿Desea crear una tabla de particiones ahora?.\n\nSi presiona cancelar no podrá utilizar este disco para instalar Canaima.'.format(self.disco),
                    title='Tabla de particiones no encontrada'.format(self.disco),
                    mtype=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK_CANCEL,
                    c_1=gtk.RESPONSE_OK, f_1=self.part.nueva_tabla_particiones, p_1=(self.disco, 'msdos'),
                    c_2=gtk.RESPONSE_OK, f_2=self.seleccionar_disco, p_2=()
                    )
        else:
            try:
                self.barra_part.expose()
            except:
                pass

            self.total = self.particiones[0][9]
            CFG['w'].siguiente.set_sensitive(True)
            self.cmb_metodo.set_sensitive(True)

            mini = self.particiones[0][1]
            mfin = self.particiones[0][9]
            for t in self.particiones:
                if mini > t[1]:
                    mini = t[1]

                if mfin < t[2]:
                    mfin = t[2]

                if t[5] == 'primary' and t[4] != 'free':
                    primarias += 1
                elif t[5] == 'logical' and t[4] != 'free':
                    logicas += 1
                elif t[5] == 'extended':
                    extendidas += 1

            disco_array = [self.disco, mini, mfin, primarias, extendidas, logicas]

            if self.total > self.minimo:
                for p in self.particiones:
                    part = p[0]
                    tam = p[3]
                    fs = p[4]
                    tipo = p[5]
                    libre = p[8]

                    if fs != 'free' and libre >= self.minimo:
                        if tipo == 'logical' and FSPROGS[fs][1] != '':
                            if logicas < 10:
                                self.metodos.append({
                                    'tipo': 'REDIM',
                                    'msg': 'Instalar redimensionando {0} para liberar espacio ({1} libres)'.format(part, humanize(libre)),
                                    'part': p,
                                    'disco': disco_array
                                })

                        elif tipo == 'primary' and FSPROGS[fs][1] != '':
                            if (extendidas < 1 and primarias < 4) or (extendidas > 0 and primarias < 2):
                                self.metodos.append({
                                    'tipo': 'REDIM',
                                    'msg': 'Instalar redimensionando {0} para liberar espacio ({1} libres)'.format(part, humanize(libre)),
                                    'part': p,
                                    'disco': disco_array
                                })

                    if fs == 'free' and tam >= self.minimo:
                        if tipo == 'logical':
                            if logicas < 10:
                                self.metodos.append({
                                    'tipo': 'LIBRE',
                                    'msg': 'Instalar usando espacio libre disponible ({0})'.format(humanize(tam)),
                                    'part': p,
                                    'disco': disco_array
                                })

                        elif tipo == 'primary':
                            if (extendidas < 1 and primarias < 4) or (extendidas > 0 and primarias < 2):
                                self.metodos.append({
                                    'tipo': 'LIBRE',
                                    'msg': 'Instalar usando espacio libre disponible ({0})'.format(humanize(tam)),
                                    'part': p,
                                    'disco': disco_array
                                })

                self.metodos.append({
                    'tipo': 'TODO',
                    'msg': 'Instalar usando todo el disco ({0})'.format(humanize(self.total)),
                    'part': disco_array,
                    'disco': disco_array
                })

                self.metodos.append({
                    'tipo': 'MANUAL',
                    'msg': 'Instalar editando particiones manualmente'.format(humanize(tam)),
                    'part': disco_array,
                    'disco': disco_array
                })

            else:
                self.metodos.append({
                    'tipo': 'NONE',
                    'msg': 'El tamaño del disco no es suficiente'
                })

                CFG['w'].siguiente.set_sensitive(False)
                self.cmb_metodo.set_sensitive(False)

            for k in sorted(self.metodos, key=lambda ordn: ordn['tipo'], reverse=True):
                self.cmb_metodo.append_text(k['msg'])

            self.cmb_metodo.set_active(0)

    def establecer_metodo(self, widget=None):
        '''
            Crea una lista de los metodos de instalación disponibles para la
            partición
        '''
        for d in self.metodos:
            if d['msg'] == self.cmb_metodo.get_active_text():
                self.metodo = d

        if self.metodo['tipo'] == 'TODO':
            msg = 'Al escoger esta opción el nuevo Sistema Operativo ocupará la totalidad de su disco duro. Tenga en cuenta que se borrarán todos los datos y/o sistemas presentes. Puede aprovechar este momento para realizar un respaldo antes de proseguir con la instalación.'
        elif self.metodo['tipo'] == 'LIBRE':
            msg = 'Esta opción le permitirá instalar el Sistema Operativo en el espacio libre de {0} que se encuentra en su disco duro, conservando los demás datos y/o sistemas que se encuentren en las demás porciones del disco.'.format(humanize(self.metodo['part'][2] - self.metodo['part'][1]))
        elif self.metodo['tipo'] == 'REDIM':
            msg = 'Esta opción permitirá utilizar el espacio libre presente en la partición {0} para instalar el Sistema Operativo. Se redimensionará la partición para liberar el espacio, manteniendo los datos y/o sistemas presentes'.format(self.metodo['part'][0])
        elif self.metodo['tipo'] == 'MANUAL':
            msg = 'Si escoge esta opción se abrirá el editor de particiones, que le permitirá ajustar las particiones según más le convenga. No le recomendamos que utilice esta opción a menos que sepa lo que está haciendo.'
        elif self.metodo['tipo'] == 'NONE':
            msg = 'El sistema operativo necesita al menos 6GB libres para poder instalar. Seleccione otro disco duro.'
        else:
            pass

        self.lbl4.set_text(msg)

