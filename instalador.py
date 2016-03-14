#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# =============================================================================
# PAQUETE: instalador
# ARCHIVO: instalador.py
# COPYRIGHT:
#       (C) 2012 William Abrahan Cabrera Reyes <william@linux.es>
#       (C) 2012 Erick Manuel Birbe Salazar <erickcion@gmail.com>
#       (C) 2012 Luis Alejandro Martínez Faneyth <luis@huntingbears.com.ve>
# LICENCIA: GPL-3
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

from instalador.clases.common import UserMessage
from instalador.config import CFG, BANNER_IMAGE
from instalador.main import Bienvenida, Wizard
from instalador.translator import MAIN_ROOT_ERROR_MSG, \
    MAIN_ROOT_ERROR_TITLE, gettext_install
import gtk
import os
import sys


gettext_install()

if __name__ == "__main__":
    if os.geteuid() != 0:
        dialog = UserMessage(
            message=MAIN_ROOT_ERROR_MSG, title=MAIN_ROOT_ERROR_TITLE,
            mtype=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK,
            c_1=gtk.RESPONSE_OK, f_1=sys.exit, p_1=(1,)
            )
    else:
        CFG['w'] = Wizard(700, 470, _('Canaima Installation'), BANNER_IMAGE)
        b = Bienvenida(CFG)
        a = b.init(CFG)

        gtk.main()
        sys.exit()

