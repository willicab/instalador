'''
-*- coding: UTF-8 -*-
Created on 10/09/2012

@author: Erick Birbe <erickcion@gmail.com>
'''

ELIMINAR = 0
NUEVA = 1

class accion:
    'Clase general para las acciones'
    tipo_accion = None
    disco = None
    tipo = None
    formato = None
    inicio = None
    fin = None

    def __init__(self, tipo_accion, disco, tipo, formato, inicio, fin):
        '''
        Constructor
        '''
        self.tipo_accion = tipo_accion
        self.disco = disco
        self.tipo = tipo
        self.formato = formato
        self.inicio = inicio
        self.fin = fin
