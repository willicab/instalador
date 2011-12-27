#!/usr/bin/env python
#-*- coding: UTF-8 -*-
'''Script para probar la clase'''
# Autor: William Cabrera
# Fecha: 11/10/2011

import pygtk
pygtk.require('2.0')
import gtk
#import Image
from pasos import bienvenida, teclado, metodo, particion_auto, particion_todo, \
    instalacion, usuario, info
import wizard
#import commands
#import clases.particiones
import clases.general as gen
#import mensaje
#import threading
import os

gtk.gdk.threads_init()

id_siguiente, id_anterior = -1, -1
banner = 'data/banner-app-top.png'
frmMain = wizard.Wizard(600, 407, "Canaima Instalador", banner, "Instalar")
pasos = {}
cfg = {}

def Test():
    gen.ram()
    Bienvenida()
    frmMain.show()

class Bienvenida():
    def __init__(self):
        global id_siguiente
        if frmMain.indice(frmMain.nombres, 'Bienvenida') == -1:
            frmMain.agregar('Bienvenida', bienvenida.Main())
        frmMain.mostrar('Bienvenida')
        desconectar()
        id_siguiente = frmMain.btn_siguiente.connect("clicked", self.siguiente)
        frmMain.btn_anterior.set_sensitive(False)
        
    def siguiente(self, widget=None): Teclado()

class Teclado():
    def __init__(self):
        global id_siguiente, id_anterior, cfg
        if frmMain.indice(frmMain.nombres, 'Teclado') == -1:
            frmMain.agregar('Teclado', teclado.Main())
        frmMain.mostrar('Teclado')
        desconectar()
        id_siguiente = frmMain.btn_siguiente.connect("clicked", self.siguiente)
        id_anterior = frmMain.btn_anterior.connect("clicked", self.anterior)
        frmMain.btn_anterior.set_sensitive(True)
        
    def siguiente(self, widget=None): 
        frmTeclado = frmMain.formulario('Teclado')
        cfg['teclado'] = frmTeclado.distribucion
        Metodo()
    def anterior(self, widget=None): Bienvenida()
    
class Metodo():
    def __init__(self):
        global id_siguiente, id_anterior, cfg
        if frmMain.indice(frmMain.nombres, 'Metodo') == -1:
            frmMain.agregar('Metodo', metodo.Main(frmMain))
        frmMain.mostrar('Metodo')
        desconectar()
        id_siguiente = frmMain.btn_siguiente.connect("clicked", self.siguiente)
        id_anterior = frmMain.btn_anterior.connect("clicked", self.anterior)
        
    def siguiente(self, widget=None):
        frmMetodo = frmMain.formulario('Metodo')
        cfg['metodo'] = frmMetodo.metodo
        if frmMetodo.metodo == 'manual': pass # Aun no desarrollado
        elif frmMetodo.metodo == 'todo': 
            cfg['disco'] = frmMetodo.disco
            PartTodo(cfg['disco'])
            pass
        else:
            cfg['particion'] = frmMetodo.metodo
            PartAuto(frmMetodo.metodo)
    def anterior(self, widget=None): Teclado()

class PartAuto():
    def __init__(self, particion):
        global id_siguiente, id_anterior, cfg
        if frmMain.indice(frmMain.nombres, 'ParticionAuto') == -1:
            frmMain.agregar('ParticionAuto', particion_auto.Main(particion))
        frmMain.mostrar('ParticionAuto')
        desconectar()
        id_siguiente = frmMain.btn_siguiente.connect("clicked", self.siguiente)
        id_anterior = frmMain.btn_anterior.connect("clicked", self.anterior)
        
    def siguiente(self, widget=None):
        frmPartAuto = frmMain.formulario('ParticionAuto')
        cfg['particion'] = frmPartAuto.particion
        cfg['inicio'] = frmPartAuto.ini
        cfg['fin'] = frmPartAuto.fin
        cfg['nuevo_fin'] = frmPartAuto.cur_value
        cfg['tipo'] = frmPartAuto.metodo
        cfg['swap'] = frmPartAuto.swap
        cfg['fs'] = frmPartAuto.fs
        Usuario()
        #Info()
    def anterior(self, widget=None): Metodo()

class PartTodo():
    def __init__(self, disco):
        global id_siguiente, id_anterior, cfg
        self.disco = disco
        if frmMain.indice(frmMain.nombres, 'ParticionTodo') == -1:
            frmMain.agregar('ParticionTodo', particion_todo.Main(disco))
        frmMain.mostrar('ParticionTodo')
        desconectar()
        id_siguiente = frmMain.btn_siguiente.connect("clicked", self.siguiente)
        id_anterior = frmMain.btn_anterior.connect("clicked", self.anterior)
    def siguiente(self, widget=None):
        frmPartTodo = frmMain.formulario('ParticionTodo')
        cfg['inicio'] = frmPartTodo.ini
        cfg['fin'] = frmPartTodo.fin
        cfg['tipo'] = frmPartTodo.metodo
        Usuario()
        #Info()
    def anterior(self, widget=None): Metodo()

class Usuario():
    def __init__(self):
        global id_siguiente, id_anterior, cfg
        if frmMain.indice(frmMain.nombres, 'UsuarioRoot') == -1:
            frmMain.agregar('UsuarioRoot', usuario.Main())
        frmMain.mostrar('UsuarioRoot')
        desconectar()
        id_siguiente = frmMain.btn_siguiente.connect("clicked", self.siguiente)
        id_anterior = frmMain.btn_anterior.connect("clicked", self.anterior)
    def siguiente(self, widget=None):
        frmUsuarioRoot = frmMain.formulario('UsuarioRoot')
        cfg['passroot'] = frmUsuarioRoot.txt_passroot.get_text()
        cfg['passroot2'] = frmUsuarioRoot.txt_passroot2.get_text()
        cfg['nombre'] = frmUsuarioRoot.txt_nombre.get_text()
        cfg['usuario'] = frmUsuarioRoot.txt_usuario.get_text()
        cfg['passuser'] = frmUsuarioRoot.txt_passuser.get_text()
        cfg['passuser2'] = frmUsuarioRoot.txt_passuser2.get_text()
        cfg['maquina'] = frmUsuarioRoot.txt_maquina.get_text()
        if cfg['passroot'].strip() == '':
            self.msg_error("Debe escribir una contraseña para root")
            return
        elif cfg['passroot'] != cfg['passroot2']:
            self.msg_error("Las contraseñas de root no coinciden")
            return
        if cfg['nombre'].strip() == '':
            self.msg_error("Debe escribir un nombre")
            return
        if cfg['usuario'].strip() == '':
            self.msg_error("Debe escribir un nombre de usuario")
            return
        if cfg['passuser'].strip() == '':
            self.msg_error("Debe escribir una contraseña para el usuario")
            return
        elif cfg['passuser'] != cfg['passuser2']:
            self.msg_error("Las contraseñas del usuario no coinciden")
            return
        Info()
    def anterior(self, widget=None):
        if cfg['metodo'] == 'todo':
            PartTodo(cfg['disco'])
        else:
            PartAuto(cfg['particion'])
            
    def msg_error(self, mensaje):
        dialog = gtk.MessageDialog(frmMain,
             gtk.DIALOG_MODAL,
             gtk.MESSAGE_ERROR,
             gtk.BUTTONS_OK,
             mensaje)
        response = dialog.run()
        dialog.destroy()
    
class Info():
    def __init__(self):
        global id_siguiente, id_anterior, cfg
        if frmMain.indice(frmMain.nombres, 'info') == -1:
            frmMain.agregar('info', info.Main(cfg))
        frmMain.mostrar('info')
        desconectar()
        id_siguiente = frmMain.btn_siguiente.connect("clicked", self.siguiente)
        id_anterior = frmMain.btn_anterior.connect("clicked", self.anterior)
    def siguiente(self, widget=None): Instalacion()
    def anterior(self, widget=None): Usuario()

class Instalacion():
    def __init__(self):
        global id_siguiente, id_anterior, cfg
        if frmMain.indice(frmMain.nombres, 'Instalacion') == -1:
            frmMain.agregar('Instalacion', instalacion.Main(cfg, frmMain))
        frmMain.mostrar('Instalacion')
        desconectar()
        id_siguiente = frmMain.btn_siguiente.connect("clicked", self.siguiente)
        id_anterior = frmMain.btn_anterior.connect("clicked", self.anterior)
    def siguiente(self, widget=None): frmMain.close()
    def anterior(self, widget=None): os.system('reboot')
        
def desconectar():
    global id_siguiente, id_anterior
    if id_siguiente != -1:
        frmMain.btn_siguiente.disconnect(id_siguiente)
        id_siguiente = -1
    if id_anterior != -1:
        frmMain.btn_anterior.disconnect(id_anterior)
        id_anterior = -1

def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    Test()
    main()
