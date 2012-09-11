#-*- coding: UTF-8 -*-
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

Created on 11/09/2012

@author: Erick Birbe <erickcion@gmail.com>
'''
from instalador.clases.acciones import NUEVA, accion

class nueva(accion):
    def __init__(self, disco, tipo, formato, inicio, fin):

        accion.__init__(NUEVA, disco, tipo, formato, inicio, fin)
