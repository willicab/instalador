#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ==============================================================================
# PAQUETE: canaima-instalador
# ARCHIVO: canaimainstalador/pasos/info.py
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

import gtk, pango

class PasoInfo(gtk.Fixed):
    def __init__(self, CFG):
        gtk.Fixed.__init__(self)

        if CFG['oem'] == False:
            msg_nombre = '● Su nombre completo será configurado como "{0}".'.format(CFG['nombre'])
            msg_usuario = '● Se creará una cuenta de usuario con nombre "{0}".'.format(CFG['usuario'])
            msg_maquina = '● Se utilizará "{0}" para identificar a su equipo en la red local.'.format(CFG['maquina'])
        else:
            msg_nombre = '● Su nombre completo será requerido en el primer inicio de sesión (modo OEM).'
            msg_usuario = '● Su nombre de usuario será requerido en el primer inicio de sesión (modo OEM).'
            msg_maquina = '● El nombre de máquina será requerido en el primer inicio de sesión (modo OEM).'

        if CFG['metodo']['tipo'] == 'MANUAL':
            msg_metodo = '● La instalación se realizará según las indicaciones provistas en el particionador manual.'

        elif CFG['metodo']['tipo'] == 'TODO':
            msg_metodo = '● La instalación utilizará todo el disco "{0}".'.format(CFG['metodo']['disco'][0])

        elif CFG['metodo']['tipo'] == 'LIBRE':
            msg_metodo = '● La instalación utilizará un espacio libre existente.'

        elif CFG['metodo']['tipo'] == 'REDIM':
            msg_metodo = '● La instalación liberará espacio redimesionando una partición existente.'

        if CFG['metodo']['tipo'] != 'MANUAL':
            if CFG['forma'] == 'ROOT:SWAP:LIBRE' or \
                CFG['forma'] == 'PART:ROOT:SWAP':
                msg_tipo = '● La instalación se realizará en una partición para el sistema y otra para la swap.'

            elif CFG['forma'] == 'ROOT:HOME:SWAP:LIBRE' or \
                CFG['forma'] == 'PART:ROOT:HOME:SWAP':
                msg_tipo = '● La instalación se realizará en varias particiones: raíz, home y swap.'

            elif CFG['forma'] == 'BOOT:ROOT:HOME:SWAP:LIBRE' or \
                CFG['forma'] == 'PART:BOOT:ROOT:HOME:SWAP':
                msg_tipo = '● La instalación se realizará en varias particiones: boot, raíz, home y swap.'

            elif CFG['forma'] == 'BOOT:ROOT:VAR:USR:HOME:SWAP:LIBRE' or \
                CFG['forma'] == 'PART:BOOT:ROOT:VAR:USR:HOME:SWAP':
                msg_tipo = '● La instalación se realizará en varias particiones: boot, raíz, var, usr, home y swap.'

        else:
            msg_tipo = ''

        msg_teclado = '● Se utilizará "{0}" como distribución de teclado.'.format(CFG['teclado'])
        msg_final = 'Presione el botón "Adelante" para iniciar la instalación del sistema. Después de este paso no podrá detener la instalación, así que asegúrese de que sus datos son correctos.'
        msg_titulo = '¡Todo listo!'

        attr = pango.AttrList()
        size = pango.AttrSize(20000, 0, -1)
        attr.insert(size)

        self.lbltitulo = gtk.Label(msg_titulo)
        self.lbltitulo.set_size_request(640, 40)
        self.lbltitulo.set_alignment(0, 0)
        self.lbltitulo.set_attributes(attr)
        self.lbltitulo.set_line_wrap(True)
        self.put(self.lbltitulo, 50, 90)

        self.lblusuario = gtk.Label(msg_usuario)
        self.lblusuario.set_size_request(640, 20)
        self.lblusuario.set_alignment(0, 0)
        self.lblusuario.set_line_wrap(True)
        self.put(self.lblusuario, 50, 130)

        self.lblnombre = gtk.Label(msg_nombre)
        self.lblnombre.set_size_request(640, 20)
        self.lblnombre.set_alignment(0, 0)
        self.lblnombre.set_line_wrap(True)
        self.put(self.lblnombre, 50, 150)

        self.lblteclado = gtk.Label(msg_teclado)
        self.lblteclado.set_size_request(640, 20)
        self.lblteclado.set_alignment(0, 0)
        self.lblteclado.set_line_wrap(True)
        self.put(self.lblteclado, 50, 170)

        self.lblmaquina = gtk.Label(msg_maquina)
        self.lblmaquina.set_size_request(640, 20)
        self.lblmaquina.set_alignment(0, 0)
        self.lblmaquina.set_line_wrap(True)
        self.put(self.lblmaquina, 50, 190)

        self.lblmetodo = gtk.Label(msg_metodo)
        self.lblmetodo.set_size_request(640, 20)
        self.lblmetodo.set_alignment(0, 0)
        self.lblmetodo.set_line_wrap(True)
        self.put(self.lblmetodo, 50, 210)

        self.lbltipo = gtk.Label(msg_tipo)
        self.lbltipo.set_size_request(640, 20)
        self.lbltipo.set_alignment(0, 0)
        self.lbltipo.set_line_wrap(True)
        self.put(self.lbltipo, 50, 230)

        self.lblmsg = gtk.Label(msg_final)
        self.lblmsg.set_size_request(640, 50)
        self.lblmsg.set_alignment(0, 0)
        self.lblmsg.set_line_wrap(True)
        self.put(self.lblmsg, 50, 280)

