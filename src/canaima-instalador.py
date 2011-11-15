#!/usr/bin/env python
#-*- coding: UTF-8 -*-
'''Script para probar la clase'''
# Autor: William Cabrera
# Fecha: 11/10/2011

import pygtk
pygtk.require('2.0')
import gtk
import Image
from pasos import bienvenida, teclado, metodo, particion_auto, accion
import wizard
import commands
import clases.particiones
import mensaje
import threading

gtk.gdk.threads_init()

id_siguiente, id_anterior = -1, -1
banner = 'data/banner-app-top.png'
frm1 = wizard.Wizard(600, 407, "Canaima Instalador", banner, "Instalar")
pasos = {}
cfg = {}
m = mensaje.Main('Canaima Instalador', 'Espere mientras se crean las particiones')

def Test():
    Bienvenida()
    frm1.show()
    frm1.btn_aplicar.connect("clicked", go)

class Bienvenida():
    def __init__(self):
        global id_siguiente
        if frm1.indice(frm1.nombres, 'Bienvenida') == -1:
            frm1.agregar('Bienvenida', bienvenida.Main())
        frm1.mostrar('Bienvenida')
        desconectar()
        id_siguiente = frm1.btn_siguiente.connect("clicked", self.siguiente)
        frm1.btn_anterior.set_sensitive(False)
        
    def siguiente(self, widget=None): Teclado()

class Teclado():
    def __init__(self):
        global id_siguiente, id_anterior
        if frm1.indice(frm1.nombres, 'Teclado') == -1:
            frm1.agregar('Teclado', teclado.Main())
        frm1.mostrar('Teclado')
        desconectar()
        id_siguiente = frm1.btn_siguiente.connect("clicked", self.siguiente)
        id_anterior = frm1.btn_anterior.connect("clicked", self.anterior)
        frm1.btn_anterior.set_sensitive(True)
        
    def siguiente(self, widget=None): Metodo()
    def anterior(self, widget=None): Bienvenida()
    
class Metodo():
    def __init__(self):
        global id_siguiente, id_anterior
        if frm1.indice(frm1.nombres, 'Metodo') == -1:
            frm1.agregar('Metodo', metodo.Main())
        frm1.mostrar('Metodo')
        desconectar()
        id_siguiente = frm1.btn_siguiente.connect("clicked", self.siguiente)
        id_anterior = frm1.btn_anterior.connect("clicked", self.anterior)
        
    def siguiente(self, widget=None):
        frm_metodo = frm1.pasos[frm1.indice(frm1.nombres, 'Metodo')]
        print frm_metodo.metodo
        if frm_metodo.metodo == 'manual': 
            pass
        elif frm_metodo.metodo == 'todo': 
            pass
        else:
            p = Part_auto(frm_metodo.metodo)
            frm1.pasos[frm1.indice(frm1.nombres, 'ParticionAuto')].\
                img_particion()
    def anterior(self, widget=None): Teclado()

class Part_auto():
    def __init__(self, particion):
        global id_siguiente, id_anterior
        if frm1.indice(frm1.nombres, 'ParticionAuto') == -1:
            frm1.agregar('ParticionAuto', particion_auto.Main(particion))
        frm1.mostrar('ParticionAuto')
        desconectar()
        id_siguiente = frm1.btn_siguiente.connect("clicked", self.siguiente)
        id_anterior = frm1.btn_anterior.connect("clicked", self.anterior)
        
    def siguiente(self, widget=None):
        pass
        #m.start()
        #thread = threading.Thread(target=particion_automatica, args=())
        #thread.start()
        #print 'Listo'
    def anterior(self, widget=None): Metodo()

def desconectar():
    global id_siguiente, id_anterior
    if id_siguiente != -1:
        frm1.btn_siguiente.disconnect(id_siguiente)
        id_siguiente = -1
    if id_anterior != -1:
        frm1.btn_anterior.disconnect(id_anterior)
        id_anterior = -1

def go(self, widget=None):
    cfg['layout'] = p1.layout
    cfg['disco'] = p2.disco
    cfg['metodo'] = p2.metodo
    accion.ejecutar(cfg)
    frm1.close()

def particion_automatica():

    cfg = frm1.pasos[frm1.nombres.index('ParticionAuto')].cfg
    print 'Configuración: ', cfg
    cmd = 'umount {0}'.format(cfg['particion'])
    print cmd
    m.accion('Desmontando dispositivo')
    print commands.getstatusoutput(cmd)
    cmd = 'echo y | ntfsresize -P --force {0} -s {1}k'.format(cfg['particion'], cfg['desde'])
    print cmd
    m.accion('redimensionando partición')
    print commands.getstatusoutput(cmd)
    cmd = 'parted -s {0} rm {1}'.format(cfg['disco'], cfg['num'])
    m.accion('Creando nuevas particiones')
    print cmd
    print commands.getstatusoutput(cmd)
    cmd = 'parted -s {0} mkpart primary NTFS {1}k {2}k'.format(cfg['disco'], cfg['ini'], (cfg['desde'] + cfg['ini']))
    print cmd
    print commands.getstatusoutput(cmd)
    cmd = 'parted -s {0} mkpart primary {1}k {2}k'.format(cfg['disco'], cfg['ext4']['ini'], (cfg['ext4']['fin']))
    print cmd
    print commands.getstatusoutput(cmd)
    cmd = 'parted -s {0} mkpart primary {1}k {2}k'.format(cfg['disco'], cfg['swap']['ini'], (cfg['swap']['fin']))
    print cmd
    print commands.getstatusoutput(cmd)
    #return
    part = clases.particiones.Main()
    p = part.lista_particiones(cfg['disco'])
    #print p
    for s in p:
        print s[1][:-2], cfg['ext4']['ini'], cfg['swap']['ini']
        print s[1][:-2].replace(',', '.')
        print int(float(s[1][:-2].replace(',', '.')))
        l = [s[1][:-2], \
            str(int(float(s[1][:-2].replace(',', '.'))) + 1), \
            str(int(float(s[1][:-2].replace(',', '.'))) - 1)]
        if str(cfg['ext4']['ini']) in l:
            cmd = 'mkfs.ext4 {0}'.format(s[0])
            print cmd
            m.accion('Formateando partición {0} a ext4'.format(s[0]))
            print commands.getstatusoutput(cmd)
        if str(cfg['swap']['ini']) in l:
            cmd = 'mkswap {0}'.format(s[0])
            print cmd
            m.accion('Formateando partición {0} como swap'.format(s[0]))
            print commands.getstatusoutput(cmd)
    m.close()

def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    Test()
    main()
