#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# =============================================================================
# PAQUETE: canaima-instalador
# ARCHIVO: canaimainstalador/clases/leyenda.py
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

from canaimainstalador.clases.common import humanize
from canaimainstalador.translator import gettext_install
import gtk


gettext_install()

MSG_ROOT_SPC = _("Espacio principal (/):")
MSG_SWAP_SPC = _("Espacio de intercambio (swap):")
MSG_USER_SPC = _("Espacio de usuarios (/home):")
MSG_APP_SPC = _("Espacio de aplicaciones (/usr):")
MSG_BOOT_SPC = _("Espacio de arranque (/boot):")
MSG_VAR_SPC = _("Espacio de variables (/var):")
MSG_FREE_SPC = _("Espacio Libre:")
MSG_RESIZE_SPC = _("Partición redimensionada:")


class Leyenda(gtk.Fixed):
    def __init__(self, parent):
        gtk.Fixed.__init__(self)
        self.p = parent

        label = ''
        self.lbl_1 = gtk.Label(label)
        self.lbl_1.set_size_request(300, 20)
        self.lbl_1.set_alignment(0, 0)
        self.put(self.lbl_1, 0, 0)

        self.lbl_2 = gtk.Label(label)
        self.lbl_2.set_size_request(300, 20)
        self.lbl_2.set_alignment(0, 0)
        self.put(self.lbl_2, 0, 20)

        self.lbl_3 = gtk.Label(label)
        self.lbl_3.set_size_request(300, 20)
        self.lbl_3.set_alignment(0, 0)
        self.put(self.lbl_3, 0, 40)

        self.lbl_4 = gtk.Label(label)
        self.lbl_4.set_size_request(300, 20)
        self.lbl_4.set_alignment(0, 0)
        self.put(self.lbl_4, 0, 60)

        self.lbl_5 = gtk.Label(label)
        self.lbl_5.set_size_request(300, 20)
        self.lbl_5.set_alignment(0, 0)
        self.put(self.lbl_5, 0, 80)

        self.lbl_6 = gtk.Label(label)
        self.lbl_6.set_size_request(300, 20)
        self.lbl_6.set_alignment(0, 0)
        self.put(self.lbl_6, 0, 100)

        self.lbl_7 = gtk.Label(label)
        self.lbl_7.set_size_request(300, 20)
        self.lbl_7.set_alignment(0, 0)
        self.put(self.lbl_7, 0, 120)

        self.show_all()

    def cambiar(self, forma):
        self.forma = forma
        self.p.forma = forma
        self.expose()

    def expose(self, widget=None, event=None):
        self.forma = self.p.forma
        self.nuevas = self.p.nuevas
        self.lbl_1.set_text('')
        self.lbl_2.set_text('')
        self.lbl_3.set_text('')
        self.lbl_4.set_text('')
        self.lbl_5.set_text('')
        self.lbl_6.set_text('')
        self.lbl_7.set_text('')

        j = 1
        for i in self.nuevas:
            part = i[0]
            size = humanize(i[2] - i[1])

            if part == 'ROOT':
                exec "self.lbl_" + str(j) + ".set_text('" + MSG_ROOT_SPC \
                + " '+size)"
            elif part == 'SWAP':
                exec "self.lbl_" + str(j) + ".set_text('" + MSG_SWAP_SPC \
                + " '+size)"
            elif part == 'HOME':
                exec "self.lbl_" + str(j) + ".set_text('" + MSG_USER_SPC \
                + " '+size)"
            elif part == 'USR':
                exec "self.lbl_" + str(j) + ".set_text('" + MSG_APP_SPC \
                + " '+size)"
            elif part == 'BOOT':
                exec "self.lbl_" + str(j) + ".set_text('" + MSG_BOOT_SPC \
                + " '+size)"
            elif part == 'VAR':
                exec "self.lbl_" + str(j) + ".set_text('" + MSG_VAR_SPC \
                + " '+size)"
            elif part == 'LIBRE':
                exec "self.lbl_" + str(j) + ".set_text('" + MSG_FREE_SPC \
                + " '+size)"
            elif part == 'PART':
                exec "self.lbl_" + str(j) + ".set_text('" + MSG_RESIZE_SPC \
                + " '+size)"

            j += 1

