#!/usr/bin/env python
#-*- coding: UTF-8 -*-
'''Script inicial'''
# Autor: William Cabrera
# Fecha: 11/10/2011

import os, gtk, sys

from instalador.main import Bienvenida, Wizard
from instalador.constructor import UserMessage
from instalador.translator import MAIN_ROOT_ERROR_MSG, MAIN_ROOT_ERROR_TITLE
from instalador.config import CFG, BANNER

if __name__ == "__main__":
    if os.geteuid() != 0:
        dialog = UserMessage(
            message=MAIN_ROOT_ERROR_MSG, title=MAIN_ROOT_ERROR_TITLE,
            mtype=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK,
            c_1=gtk.RESPONSE_OK, f_1=sys.exit, p_1=(1,)
            )
    else:
        CFG['w'] = Wizard(700, 450, "Canaima Instalador", BANNER)
        b = Bienvenida(CFG)
        a = b.init(CFG)

        gtk.main()
        sys.exit()

