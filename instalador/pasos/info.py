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

import gtk
import pango
from instalador.translator import gettext_install
from instalador.mod_accesible import atk_acc_vd


gettext_install()


class PasoInfo(gtk.Fixed):

    msg_titulo = None
    msg_nombre = None
    msg_usuario = None
    msg_maquina = None
    msg_metodo = None
    msg_tipo = None
    msg_teclado = None
    msg_final = None

    def __init__(self, CFG):
        gtk.Fixed.__init__(self)

        if CFG['oem'] == False:
            msg_nombre = _('- Your full name will be set to "{0}".') \
            .format(CFG['nombre'])
            msg_usuario = _('- An user account named "{0}" will be created.') \
            .format(CFG['usuario'])
            msg_maquina = _('- The machine name "{0}" will be used to \
identify your computer on the local network.').format(CFG['maquina'])
        else:
            msg_nombre = _('- Your full name will be required on the first \
login.')
            msg_usuario = _('- Your username will be required in the first \
login.')
            msg_maquina = _('- The machine name will be required in the first \
login.')

        if CFG['metodo']['tipo'] == 'MANUAL':
            msg_metodo = _('- The installation must follow the directions \
provided in the manual partitioning.')

        elif CFG['metodo']['tipo'] == 'TODO':
            msg_metodo = _('- The installation will use the entire disk  \
"{0}".').format(CFG['metodo']['disco'][0])

        elif CFG['metodo']['tipo'] == 'LIBRE':
            msg_metodo = _('- The installation will use existing free space.')

        elif CFG['metodo']['tipo'] == 'REDIM':
            msg_metodo = _('- The installation will release space resizing an \
existing partition.')

        if CFG['metodo']['tipo'] != 'MANUAL':
            if CFG['forma'] == 'ROOT:SWAP:LIBRE' or \
                CFG['forma'] == 'PART:ROOT:SWAP':
                msg_tipo = _('- The installation will take place in a \
partition for the system and other for swap.')

            elif CFG['forma'] == 'ROOT:HOME:SWAP:LIBRE' or \
                CFG['forma'] == 'PART:ROOT:HOME:SWAP':
                msg_tipo = _('- The installation will take place in several \
partitions: "Root (/)", "/home" and "swap".')

            elif CFG['forma'] == 'BOOT:ROOT:HOME:SWAP:LIBRE' or \
                CFG['forma'] == 'PART:BOOT:ROOT:HOME:SWAP':
                msg_tipo = _('- The installation will take place in several \
partitions: "/boot", "Root (/)", "/home" and "swap".')

            elif CFG['forma'] == 'BOOT:ROOT:VAR:USR:HOME:SWAP:LIBRE' or \
                CFG['forma'] == 'PART:BOOT:ROOT:VAR:USR:HOME:SWAP':
                msg_tipo = _('- The installation will take place in several \
partitions: "/boot", "Root (/)", "/var", "/usr", "/home" y "swap".')

        else:
            msg_tipo = ''

        msg_teclado = _('- "{0}" will be used as keyboard layout.') \
        .format(CFG['keyboard'])

        msg_titulo = _('All ready!')
        msg_final = _('Press "Next" to start installing the system. After \
this step you can not stop the installation, so make sure your data is \
correct.')

        msg_confirm = """
{}
{}
{}
{}
{}
{}

{}
""".format(msg_usuario, msg_nombre, msg_teclado, msg_maquina, \
           msg_metodo, msg_tipo, msg_final)
        # Limpiamos texto de las varaiables vacias.
        msg_confirm.replace("\nNone", "")

        attr = pango.AttrList()
        size = pango.AttrSize(20000, 0, -1)
        attr.insert(size)

        self.lbltitulo = gtk.Label(msg_titulo)
        self.lbltitulo.set_size_request(640, 40)
        self.lbltitulo.set_alignment(0, 0)
        self.lbltitulo.set_attributes(attr)
        self.lbltitulo.set_line_wrap(True)
        self.put(self.lbltitulo, 20, 60)

        self.lblusuario = gtk.Label()
        self.lblusuario.set_markup(msg_confirm)
        self.lblusuario.set_size_request(640, -1)
        self.lblusuario.set_line_wrap(True)
        self.put(self.lblusuario, 20, 100)

        self.set_flags(gtk.CAN_FOCUS)
        atk_acc_vd(self, msg_titulo + ". " + msg_confirm)
