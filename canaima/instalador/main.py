#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''Script inicial'''
# Autor: William Cabrera, Wil Alvarez
# Fecha: 11/10/2011

import os
import logging

from optparse import OptionParser

# Imports propios
from canaima.instalador.lib import general
from canaima.instalador.ui.asistente import Asistente

LOG_LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}

'''
from pasos import bienvenida, teclado, metodo, particion_auto, particion_todo, \
    instalacion, usuario, info
import wizard
import os
'''
import gtk
from canaima.instalador.pasos import bienvenida, teclado
from canaima.instalador.wizard import Wizard
ID_SIGUIENTE, ID_ANTERIOR = -1, -1
BANNER = os.path.join(os.path.dirname(__file__), 'data', 'banner-app-top.png')
print BANNER
FRM_MAIN = Wizard(600, 407, "Canaima Instalador", BANNER)
CFG = {}


class Instalador:
    def __init__(self):
        parser = OptionParser()
        parser.add_option('--log-level', dest='log_level',
            help='seleccione el nivel de log deseado. Opciones: %s' % LOG_LEVELS.keys(),
            default='debug')
        
        (options, args) = parser.parse_args()
        
        if options.log_level:
            if LOG_LEVELS.has_key(options.log_level):
                print "Nivel de log: %s" % options.log_level
                logging.basicConfig(level=LOG_LEVELS[options.log_level])
            else:
                print "Nivel de log inválido. 'debug' seleccionado por defecto"
                logging.basicConfig(level=LOG_LEVELS['debug'])
        self.log = logging.getLogger('Instalador')
        
        # Calculamos la RAM una sola vez
        self.ram = general.ram()
        self.mapa_teclado = None
        self.log.debug('RAM disponible: %s' % self.ram)
        self.asistente = Asistente()
        #Bienvenida()
        #Teclado()
        #FRM_MAIN.show()
        #gtk.main()
        
def inicio():
    '''
        Inicia la aplicación
    '''
    gen.ram()
    Bienvenida()
    FRM_MAIN.show()

class Bienvenida():
    '''
        Inicia el paso que muestra el mensaje de bienvenida
    '''
    def __init__(self):
        global ID_SIGUIENTE
        if FRM_MAIN.indice(FRM_MAIN.nombres, 'Bienvenida') == -1:
            FRM_MAIN.agregar('Bienvenida', bienvenida.Main())
        FRM_MAIN.mostrar('Bienvenida')
        desconectar()
        ID_SIGUIENTE = FRM_MAIN.btn_siguiente.connect("clicked", self.siguiente)
        FRM_MAIN.btn_anterior.set_sensitive(False)

    def siguiente(self, widget = None):
        '''
            Función para el evento del boton siguiente
        '''
        Teclado()
    def anterior(self, widget = None):
        '''
            Función para el evento del botón anterior
        '''
        Bienvenida()

class Teclado():
    '''
        Inicia el paso que escoge la distribución del teclado
    '''
    def __init__(self):
        global ID_SIGUIENTE, ID_ANTERIOR, CFG
        if FRM_MAIN.indice(FRM_MAIN.nombres, 'Teclado') == -1:
            FRM_MAIN.agregar('Teclado', teclado.Main())
        FRM_MAIN.mostrar('Teclado')
        desconectar()
        ID_SIGUIENTE = FRM_MAIN.btn_siguiente.connect("clicked", self.siguiente)
        ID_ANTERIOR = FRM_MAIN.btn_anterior.connect("clicked", self.anterior)
        FRM_MAIN.btn_anterior.set_sensitive(True)

    def siguiente(self, widget = None):
        '''
            Función para el evento del botón siguiente
        '''
        frm_teclado = FRM_MAIN.formulario('Teclado')
        CFG['teclado'] = frm_teclado.distribucion
        Metodo()
    def anterior(self, widget = None):
        '''
            Función para el evento del botón anterior
        '''
        Bienvenida()

class Metodo():
    '''
        Inicia el paso que escoge el método de particionado
    '''
    def __init__(self):
        global ID_SIGUIENTE, ID_ANTERIOR, CFG
        if FRM_MAIN.indice(FRM_MAIN.nombres, 'Metodo') == -1:
            FRM_MAIN.agregar('Metodo', metodo.Main(FRM_MAIN))
        FRM_MAIN.mostrar('Metodo')
        desconectar()
        ID_SIGUIENTE = FRM_MAIN.btn_siguiente.connect("clicked", self.siguiente)
        ID_ANTERIOR = FRM_MAIN.btn_anterior.connect("clicked", self.anterior)

    def siguiente(self, widget = None):
        '''
            Funcion para el evento del botón siguiente
        '''
        frm_metodo = FRM_MAIN.formulario('Metodo')
        CFG['metodo'] = frm_metodo.metodo
        if frm_metodo.metodo == 'manual':
            pass # Aun no desarrollado
        elif frm_metodo.metodo == 'todo':
            CFG['disco'] = frm_metodo.disco
            PartTodo(CFG['disco'], 0, 0)
        elif frm_metodo.metodo[0:5] == 'vacio':
            CFG['metodo'] = frm_metodo.metodo[0:5]
            CFG['disco'] = frm_metodo.disco
            CFG['inicio'] = frm_metodo.ini
            CFG['fin'] = frm_metodo.fin
            PartTodo(CFG['disco'], CFG['inicio'], CFG['fin'])
        else:
            CFG['particion'] = frm_metodo.metodo
            PartAuto(frm_metodo.metodo)
    def anterior(self, widget = None):
        '''
            Función para el evento del botón anterior
        '''
        Teclado()

class PartAuto():
    '''
        Inicia el paso que redimensiona la partición
    '''
    def __init__(self, particion):
        global ID_SIGUIENTE, ID_ANTERIOR, CFG
        if FRM_MAIN.indice(FRM_MAIN.nombres, 'ParticionAuto') == -1:
            FRM_MAIN.agregar('ParticionAuto', particion_auto.Main(particion))
        FRM_MAIN.mostrar('ParticionAuto')
        desconectar()
        ID_SIGUIENTE = FRM_MAIN.btn_siguiente.connect("clicked", self.siguiente)
        ID_ANTERIOR = FRM_MAIN.btn_anterior.connect("clicked", self.anterior)

    def siguiente(self, widget = None):
        '''
            Función para el evento del botón siguiente
        '''
        frm_part_auto = FRM_MAIN.formulario('ParticionAuto')
        CFG['particion'] = frm_part_auto.particion
        CFG['inicio'] = frm_part_auto.ini
        CFG['fin'] = frm_part_auto.fin
        CFG['nuevo_fin'] = frm_part_auto.cur_value
        CFG['tipo'] = frm_part_auto.metodo
        CFG['swap'] = frm_part_auto.swap
        CFG['fs'] = frm_part_auto.fs
        Usuario()
        #Info()
    def anterior(self, widget = None):
        '''
            Función para el evento del botón anterior
        '''
        Metodo()

class PartTodo():
    '''
        Inicia el paso que particiona el disco
    '''
    def __init__(self, disco, ini, fin):
        global ID_SIGUIENTE, ID_ANTERIOR, CFG
        self.disco = disco
        if FRM_MAIN.indice(FRM_MAIN.nombres, 'PartTodo') == -1:
            FRM_MAIN.agregar('PartTodo', particion_todo.Main(disco, ini, fin))
        FRM_MAIN.mostrar('PartTodo')
        desconectar()
        ID_SIGUIENTE = FRM_MAIN.btn_siguiente.connect("clicked", self.siguiente)
        ID_ANTERIOR = FRM_MAIN.btn_anterior.connect("clicked", self.anterior)
        FRM_MAIN.formulario('PartTodo').iniciar(disco, ini, fin)
    def siguiente(self, widget = None):
        '''
            Función para el evento del botón siguiente
        '''
        frm_part_todo = FRM_MAIN.formulario('PartTodo')
        CFG['inicio'] = frm_part_todo.ini
        CFG['fin'] = frm_part_todo.fin
        CFG['tipo'] = frm_part_todo.metodo
        Usuario()
        #Info()
    def anterior(self, widget = None):
        '''
            Función para el evento del botón anterior
        '''
        Metodo()

class Usuario():
    '''
        Inicia el paso que crea el usuario del sistema
    '''
    def __init__(self):
        global ID_SIGUIENTE, ID_ANTERIOR, CFG
        if FRM_MAIN.indice(FRM_MAIN.nombres, 'UsuarioRoot') == -1:
            FRM_MAIN.agregar('UsuarioRoot', usuario.Main())
        FRM_MAIN.mostrar('UsuarioRoot')
        desconectar()
        ID_SIGUIENTE = FRM_MAIN.btn_siguiente.connect("clicked", self.siguiente)
        ID_ANTERIOR = FRM_MAIN.btn_anterior.connect("clicked", self.anterior)
    def siguiente(self, widget = None):
        '''
            Función para el evento del botón siguiente
        '''
        frm_usuario_root = FRM_MAIN.formulario('UsuarioRoot')
        CFG['passroot'] = frm_usuario_root.txt_passroot.get_text()
        CFG['passroot2'] = frm_usuario_root.txt_passroot2.get_text()
        CFG['nombre'] = frm_usuario_root.txt_nombre.get_text()
        CFG['usuario'] = frm_usuario_root.txt_usuario.get_text()
        CFG['passuser'] = frm_usuario_root.txt_passuser.get_text()
        CFG['passuser2'] = frm_usuario_root.txt_passuser2.get_text()
        CFG['maquina'] = frm_usuario_root.txt_maquina.get_text()
        if CFG['passroot'].strip() == '':
            self.msg_error("Debe escribir una contraseña para root")
            return
        elif CFG['passroot'] != CFG['passroot2']:
            self.msg_error("Las contraseñas de root no coinciden")
            return
        if CFG['nombre'].strip() == '':
            self.msg_error("Debe escribir un nombre")
            return
        if CFG['usuario'].strip() == '':
            self.msg_error("Debe escribir un nombre de usuario")
            return
        if CFG['passuser'].strip() == '':
            self.msg_error("Debe escribir una contraseña para el usuario")
            return
        elif CFG['passuser'] != CFG['passuser2']:
            self.msg_error("Las contraseñas del usuario no coinciden")
            return
        Info()
    def anterior(self, widget = None):
        '''
            Función para el evento del botón anterior
        '''
        if CFG['metodo'] == 'todo' or CFG['metodo'] == 'vacio':
            PartTodo(CFG['disco'], CFG['inicio'], CFG['fin'])
        else:
            PartAuto(CFG['particion'])

    def msg_error(self, mensaje):
        '''
            Función que muestra el mensaje de error
        '''
        dialog = gtk.MessageDialog(FRM_MAIN,
             gtk.DIALOG_MODAL,
             gtk.MESSAGE_ERROR,
             gtk.BUTTONS_OK,
             mensaje)
        response = dialog.run()
        dialog.destroy()

class Info():
    '''
        Inicia el paso que muestr la información general de la instalación
    '''
    def __init__(self):
        global ID_SIGUIENTE, ID_ANTERIOR, CFG
        if FRM_MAIN.indice(FRM_MAIN.nombres, 'info') == -1:
            FRM_MAIN.agregar('info', info.Main(CFG))
        FRM_MAIN.mostrar('info')
        desconectar()
        ID_SIGUIENTE = FRM_MAIN.btn_siguiente.connect("clicked", self.siguiente)
        ID_ANTERIOR = FRM_MAIN.btn_anterior.connect("clicked", self.anterior)
    def siguiente(self, widget = None):
        '''
            Función para el evento del botón siguiente
        '''
        Instalacion()
    def anterior(self, widget = None):
        '''
            Función para el evento del botón anterior
        '''
        Usuario()

class Instalacion():
    '''
        Inicia el paso que realiza la instalación del sistema
    '''
    def __init__(self):
        global ID_SIGUIENTE, ID_ANTERIOR, CFG
        if FRM_MAIN.indice(FRM_MAIN.nombres, 'Instalacion') == -1:
            FRM_MAIN.agregar('Instalacion', instalacion.Main(CFG, FRM_MAIN))
        FRM_MAIN.mostrar('Instalacion')
        desconectar()
        ID_SIGUIENTE = FRM_MAIN.btn_siguiente.connect("clicked", self.siguiente)
        ID_ANTERIOR = FRM_MAIN.btn_anterior.connect("clicked", self.anterior)
    def siguiente(self, widget = None):
        '''
            Función para el evento del botón cerrar
        '''
        FRM_MAIN.close()
    def anterior(self, widget = None):
        '''
            Función para el evento del botón reiniciar
        '''
        os.system('reboot')

def desconectar():
    '''
        desconecta los eventos de los controles btn_sigiente y btn_anterior
    '''
    global ID_SIGUIENTE, ID_ANTERIOR
    if ID_SIGUIENTE != -1:
        FRM_MAIN.btn_siguiente.disconnect(ID_SIGUIENTE)
        ID_SIGUIENTE = -1
    if ID_ANTERIOR != -1:
        FRM_MAIN.btn_anterior.disconnect(ID_ANTERIOR)
        ID_ANTERIOR = -1

def main():
    '''
        Inicia la parte gráfica
    '''
    gtk.main()
    return 0

if __name__ == "__main__":
    instalador = Instalador()
