#-*- coding: UTF-8 -*-
'''Clase que instalará el sistema'''
# Autor: William Cabrera
# Fecha: 11/10/2011

def ejecutar(cfg):
    for i in cfg:
        #print 'Layout: ' + cfg['layout']
        print '{0}: {1}'.format(i, cfg[i])
