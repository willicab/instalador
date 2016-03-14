#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# =============================================================================
# PAQUETE: instalador
# ARCHIVO: instalador/config.py
# COPYRIGHT:
#       (C) 2012 William Abrahan Cabrera Reyes <william@linux.es>
#       (C) 2012 Erick Manuel Birbe Salazar <erickcion@gmail.com>
#       (C) 2012 Luis Alejandro Martínez Faneyth <luis@huntingbears.com.ve>
# LICENCIA: GPL-2
# =============================================================================
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from instalador.clases.barra_todo import BarraTodo
from instalador.clases.leyenda import Leyenda
from instalador.config import ESPACIO_TOTAL
from instalador.translator import gettext_install
import gtk
from instalador.mod_accesible import atk_label


gettext_install()


class PasoPartTodo(gtk.Fixed):
    def __init__(self, CFG):
        gtk.Fixed.__init__(self)
        self.metodo = CFG['metodo']
        self.particiones = CFG['particiones']
        self.forma = 'ROOT:SWAP:LIBRE'
        self.minimo = ESPACIO_TOTAL
        self.nuevas = []
        self.acciones = []
        self.libre = 0

        txt_info = _("Select the partition layout to use. Use the selector to \
indicate the size you want to use for installation of Canaima.")
        self.lbl1 = gtk.Label(txt_info)
        self.lbl1.set_size_request(690, 35)
        self.lbl1.set_alignment(0, 0)
        self.lbl1.set_line_wrap(True)
        atk_label(self.lbl1)
        self.put(self.lbl1, 0, 0)

        tip_msg = _("Select this button to use the minimum disk \
space for the Canaima installation")
        self.tam_min = gtk.Button()
        self.tam_min.set_label(_("Minimum"))
        self.tam_min.set_size_request(80, 25)
        self.tam_min.connect('clicked', self.set_min)
        self.tam_min.set_tooltip_text(tip_msg)
        self.put(self.tam_min, 525, 40)

        tip_msg = _("Select this button to use the maximum disk \
space for the Canaima installation")
        self.tam_max = gtk.Button()
        self.tam_max.set_label(_('Maximum'))
        self.tam_max.set_size_request(80, 25)
        self.tam_max.connect('clicked', self.set_max)
        self.tam_max.set_tooltip_text(tip_msg)
        self.put(self.tam_max, 610, 40)

        self.barra = BarraTodo(self)
        self.barra.set_size_request(690, 100)
        self.put(self.barra, 0, 70)

        msg_1 = _("Install everything in a single partition. (recommended)")
        self.option_1 = gtk.RadioButton(None, msg_1)
        self.option_1.connect("toggled", self.change_option, "ROOT:SWAP:LIBRE")
        self.option_1.set_size_request(350, 20)
        self.put(self.option_1, 0, 185)

        msg_2 = _("Separate /home partition.")
        self.option_2 = gtk.RadioButton(self.option_1, msg_2)
        self.option_2.connect("toggled", self.change_option,
                              "ROOT:HOME:SWAP:LIBRE")
        self.option_2.set_size_request(350, 20)
        self.put(self.option_2, 0, 210)

        msg_3 = _("Separate /home and /boot.")
        self.option_3 = gtk.RadioButton(self.option_1, msg_3)
        self.option_3.connect("toggled", self.change_option,
                              "BOOT:ROOT:HOME:SWAP:LIBRE")
        self.option_3.set_size_request(350, 20)
        self.put(self.option_3, 0, 235)

        msg_4 = _("Separate /home, /boot, /var and /usr.")
        self.option_4 = gtk.RadioButton(self.option_1, msg_4)
        self.option_4.connect("toggled", self.change_option,
                              "BOOT:ROOT:VAR:USR:HOME:SWAP:LIBRE")
        self.option_4.set_size_request(350, 20)
        self.put(self.option_4, 0, 260)

        self.leyenda = Leyenda(self)
        self.leyenda.set_size_request(300, 150)
        self.put(self.leyenda, 390, 185)

        self.option_1.toggled()

        if self.metodo['tipo'] != 'TODO' and self.metodo['disco'][4] > 0:
            if self.metodo['part'][5] == 'primary':
                if self.metodo['disco'][3] == 0:
                    # Disponibles: root+swap, root+home+swap
                    self.option_3.set_sensitive(False)
                    self.option_4.set_sensitive(False)
                elif self.metodo['disco'][3] == 1:
                    # Disponibles: root+swap
                    self.option_2.set_sensitive(False)
                    self.option_3.set_sensitive(False)
                    self.option_4.set_sensitive(False)
            elif self.metodo['part'][5] == 'logical':
                if self.metodo['disco'][5] == 7:
                    # Disponibles: root+swap, root+home+swap,
                    # boot+root+home+swap
                    self.option_4.set_sensitive(False)
                elif self.metodo['disco'][5] == 6:
                    # Disponibles: root+swap, root+home+swap,
                    # boot+root+home+swap
                    self.option_4.set_sensitive(False)
                elif self.metodo['disco'][5] == 8:
                    # Disponibles: root+swap, root+home+swap
                    self.option_3.set_sensitive(False)
                    self.option_4.set_sensitive(False)
                elif self.metodo['disco'][5] == 9:
                    # Disponibles: root+swap
                    self.option_2.set_sensitive(False)
                    self.option_3.set_sensitive(False)
                    self.option_4.set_sensitive(False)

    def set_min(self, widget):
        self.libre = self.barra.total - self.minimo
        self.barra.expose()
        self.leyenda.expose()

    def set_max(self, widget):
        self.libre = 0
        self.barra.expose()
        self.leyenda.expose()

    def change_option(self, widget, forma):
        self.forma = forma
        self.barra.expose()
        self.leyenda.expose()
