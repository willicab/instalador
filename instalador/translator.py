#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# =============================================================================
# PAQUETE: instalador
# ARCHIVO: instalador/translator.py
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

import gettext
import os

# Busqueda del directorio por defecto para los locales
lc_dir = os.path.join(os.path.dirname(__file__), '..', 'locale')
if os.path.exists(lc_dir):
    GETTEXT_LOCALEDIR = lc_dir
else:
    GETTEXT_LOCALEDIR = '/usr/share/locale'  # Directorio por defecto

GETTEXT_DOMAIN = "instalador"


def gettext_install():
    gettext.install(GETTEXT_DOMAIN, GETTEXT_LOCALEDIR)


gettext_install()


#-----------------------------------------------------------------------------#
MAIN_ROOT_ERROR_MSG = _('The installer must be executed with superuser \
permissions')
MAIN_ROOT_ERROR_TITLE = _('Permission error')
#-----------------------------------------------------------------------------#


class msj:
    '''Clase para administrar los mensajes mostrados al usuario en el \
    particionador manual relacionados a las particiones'''

    class particion:
        'Mensajes relacionados a las particiones'

        libre = _('Free Space')
        primaria = _('Primary')
        extendida = _('Extended')
        logica = _('Logic')
        desconocida = _('Unknown')

        @classmethod
        def get_tipo(self, tipo):
            if tipo == 'free':
                return self.libre
            if tipo == 'primary':
                return self.primaria
            if tipo == 'extended':
                return self.extendida
            if tipo == 'logical':
                return self.logica

            return tipo

        @classmethod
        def get_tipo_orig(self, tipo):
            if tipo == self.libre:
                return 'free'
            if tipo == self.primaria:
                return 'primary'
            if tipo == self.extendida:
                return 'extended'
            if tipo == self.logica:
                return 'logical'
            if tipo == self.desconocida:
                return 'unknown'

            return tipo

        @classmethod
        def get_formato(self, formato):
            if formato == 'free':
                return self.libre
            if formato == 'unknown':
                return self.desconocida
            if formato == 'extended':
                return ''

            return formato

        @classmethod
        def get_dispositivo(self, disp, num):
            if num == -1:
                return ''

            return disp
