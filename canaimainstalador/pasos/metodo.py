#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# =============================================================================
# PAQUETE: canaima-instalador
# ARCHIVO: canaimainstalador/pasos/metodo.py
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

from canaimainstalador.clases.barra_particiones import BarraParticiones
from canaimainstalador.clases.common import humanize, UserMessage
from canaimainstalador.clases.particiones import Particiones
from canaimainstalador.config import ESPACIO_TOTAL, CFG, FSPROGS
from canaimainstalador.translator import gettext_install
from gi.repository import Gtk
from canaimainstalador.mod_accesible import atk_acc, atk_label


gettext_install()


class PasoMetodo(Gtk.Fixed):
    def __init__(self, CFG):
        Gtk.Fixed.__init__(self)

        self.metodos = []
        self.minimo = ESPACIO_TOTAL
        self.part = Particiones()
        self.discos = self.part.lista_discos()
        print 'Se han encontrado los siguientes discos: {0}' \
        .format(self.discos)

        self.lbl1 = Gtk.Label(_("Select the disk where you want to install \
Canaima:"))
        self.lbl1.set_size_request(690, 20)
        self.lbl1.set_alignment(0, 0)
        self.put(self.lbl1, 0, 0)

        self.cmb_discos = Gtk.ComboBoxText()
        self.cmb_discos.set_size_request(690, 30)
        self.put(self.cmb_discos, 0, 25)
        atk_acc(self.cmb_discos, self.lbl1)
        self.cmb_discos.connect('changed', self.seleccionar_disco)

        for d in self.discos:
            self.cmb_discos.append_text(d)

        self.barra_part = BarraParticiones(self)
        self.barra_part.set_size_request(690, 100)
        self.put(self.barra_part, 0, 60)

        self.lbl2 = Gtk.Label(_("Slelect the installation method:"))
        self.lbl2.set_size_request(690, 20)
        self.lbl2.set_alignment(0, 0)
        self.put(self.lbl2, 0, 165)

        self.cmb_metodo = Gtk.ComboBoxText()
        self.cmb_metodo.set_size_request(690, 30)
        self.cmb_metodo.connect('changed', self.establecer_metodo)
        self.put(self.cmb_metodo, 0, 190)

        self.lbl4 = Gtk.Label()
        self.lbl4.set_size_request(690, 90)
        self.lbl4.set_alignment(0, 0)
        self.lbl4.set_line_wrap(True)
        atk_label(self.lbl4)
        self.put(self.lbl4, 0, 225)

        atk_acc(self.cmb_metodo, self.lbl2)

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
                    message=_("""Disk  "{0}" needs a partition table to \
continue the installation. Do you want to create a partition table now?

If you press Cancel you can not use that disk to install Canaima.""")\
                    .format(self.disco),
                    title=_("Partition table not found."),
                    mtype=Gtk.MessageType.INFO, buttons=Gtk.ButtonsType.OK_CANCEL,
                    c_1=Gtk.ResponseType.OK, f_1=self.part.nueva_tabla_particiones,
                    p_1=(self.disco, 'msdos'), c_2=Gtk.ResponseType.OK,
                    f_2=self.seleccionar_disco, p_2=()
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

            disco_array = [self.disco, mini, mfin, primarias, extendidas,
                           logicas]

            if self.total >= self.minimo:
                for p in self.particiones:
                    part = p[0]
                    tam = p[3]
                    fs = p[4]
                    tipo = p[5]
                    libre = p[8]

                    if fs != 'free' and libre >= self.minimo:
                        if fs in FSPROGS:
                            if tipo == 'logical' and FSPROGS[fs][1][0] != '':
                                if logicas < 10:
                                    self.metodos.append({
                                        'tipo': 'REDIM',
                                        'msg': _("Install resizing {0} to \
free up space ({1} free)").format(part, humanize(libre)),
                                        'part': p,
                                        'disco': disco_array
                                    })

                            elif tipo == 'primary' and FSPROGS[fs][1][0] != '':
                                if (extendidas < 1 and primarias < 4) \
                                or (extendidas > 0 and primarias < 2):
                                    self.metodos.append({
                                        'tipo': 'REDIM',
                                        'msg': _("Install resizing {0} to \
free up space ({1} free)").format(part, humanize(libre)),
                                        'part': p,
                                        'disco': disco_array
                                    })

                    if fs == 'free' and tam >= self.minimo:
                        if tipo == 'logical':
                            if logicas < 10:
                                self.metodos.append({
                                    'tipo': 'LIBRE',
                                    'msg': _("Install using available free \
space ({0})").format(humanize(tam)),
                                    'part': p,
                                    'disco': disco_array
                                })

                        elif tipo == 'primary':
                            if (extendidas < 1 and primarias < 4) \
                            or (extendidas > 0 and primarias < 2):
                                self.metodos.append({
                                    'tipo': 'LIBRE',
                                    'msg': _("Install using available free \
space ({0})").format(humanize(tam)),
                                    'part': p,
                                    'disco': disco_array
                                })

                self.metodos.append({
                    'tipo': 'TODO',
                    'msg': _("Install using the entire disk ({0})") \
                    .format(humanize(self.total)),
                    'part': disco_array,
                    'disco': disco_array
                })

                self.metodos.append({
                    'tipo': 'MANUAL',
                    'msg': _("Install editing partitions manually")\
                    .format(humanize(tam)),
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

            for k in sorted(self.metodos, key=lambda ordn: ordn['tipo'],
                            reverse=True):
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
            msg = _("By choosing this option, Canaima will occupy all of your \
hard drive. Note that all data present will be erased. You can take this time \
to make a backup before proceeding with the installation.")
        elif self.metodo['tipo'] == 'LIBRE':
            msg = _("By choosing this option, Canaima will be installed in \
the free space of {0} that is in you hard disk, preserving the other data and \
systems that are in the other portions of the disc.") \
            .format(humanize(self.metodo['part'][2] - self.metodo['part'][1]))
        elif self.metodo['tipo'] == 'REDIM':
            msg = _("This option will use the free space present in the \
partition {0} to install Canaima. The partition will be resized to free up \
space, preserving the data and/or systems present.") \
            .format(self.metodo['part'][0])
        elif self.metodo['tipo'] == 'MANUAL':
            msg = _("If you choose this option will open the partition \
editor, allowing you to adjust the partitions according to your convenience. \
We do not recommend you use this option unless you know what you are doing.")
        elif self.metodo['tipo'] == 'NONE':

            msg = _("Canaima needs at least {0} to be installed. Select other \
disk with more available space.").format(humanize(ESPACIO_TOTAL))
        else:
            pass

        self.lbl4.set_text(msg)
