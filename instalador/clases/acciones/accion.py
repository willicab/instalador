'''
Created on 10/09/2012

@author: Erick Birbe <erickcion@gmail.com>
'''

class accion:

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
