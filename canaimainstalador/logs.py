# -*- coding: UTF-8 -*-
'''
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Ucumari; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA

Created on 27/01/2013

@author: Erick Birbe <erickcion@gmail.com>
'''

import logging
import os

LOG_LEVEL = logging.DEBUG
LOG_DIR = "/var/log"
LOG_FILE = "canaima-instalador.log"
LOG_PATH = os.path.join(LOG_DIR, LOG_FILE)
LOG_FORMAT = '%(asctime)s %(name)s %(levelname)s %(message)s'


def config():

    logging.basicConfig(
            filename=LOG_PATH,
            level=LOG_LEVEL,
            format=LOG_FORMAT)
