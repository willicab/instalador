#!/usr/bin/env python
#-*- coding: UTF-8 -*-
'''Script inicial'''
# Autor: William Cabrera
# Fecha: 11/10/2011

# Módulos globales
import gtk, os, sys, re

# Módulos locales
from pasos import bienvenida, teclado, metodo, particion_auto, particion_todo
from pasos import particion_manual, instalacion, usuario, accesibilidad, info
from clases.wizard import Wizard
from clases.constructor import UserMessage
from clases.translator import MAIN_ROOT_ERROR_MSG, MAIN_ROOT_ERROR_TITLE

CFG = {'next':-1, 'prev':-1}
BANNER = 'data/img/banner.png'

def aconnect(button, function, bid, params):
    '''
        desconecta los eventos de los controles btn_sigiente y btn_anterior
    '''
    if bid != -1:
        button.disconnect(bid)
        bid = -1

    button.connect_object('clicked', function, params)

class Bienvenida():
    '''
        Inicia el paso que muestra el mensaje de bienvenida
    '''
    def __init__(self, CFG):

        if WIZ.indice(WIZ.nombres, 'Bienvenida') == -1:
            a = WIZ.agregar('Bienvenida', bienvenida.Main())

        m = WIZ.mostrar('Bienvenida')
        c = aconnect(WIZ.siguiente, self.siguiente, CFG['next'], CFG)
        s = WIZ.anterior.set_sensitive(False)

    def siguiente(self, CFG):
        '''
            Función para el evento del botón siguiente
        '''
        s = Teclado(CFG)

class Teclado():
    '''
        Inicia el paso que escoge la distribución del teclado
    '''
    def __init__(self, CFG):

        if WIZ.indice(WIZ.nombres, 'Teclado') == -1:
            a = WIZ.agregar('Teclado', teclado.Main())

        m = WIZ.mostrar('Teclado')
        c = aconnect(WIZ.siguiente, self.siguiente, CFG['next'], CFG)
        c = aconnect(WIZ.anterior, self.anterior, CFG['prev'], CFG)
        s = WIZ.anterior.set_sensitive(True)

    def siguiente(self, CFG):
        '''
            Función para el evento del botón siguiente
        '''
        CFG['teclado'] = WIZ.formulario('Teclado').distribucion
        print 'Distribución de teclado seleccionada: {0}'.format(CFG['teclado'])
        print 'CFG: {0}\n'.format(CFG)
        s = Metodo(CFG)

    def anterior(self, CFG):
        '''
            Función para el evento del botón anterior
        '''
        s = Bienvenida(CFG)

class Metodo():
    '''
        Inicia el paso que escoge el método de particionado
    '''
    def __init__(self, CFG):

        if WIZ.indice(WIZ.nombres, 'Metodo') == -1:
            a = WIZ.agregar('Metodo', metodo.Main(WIZ))

        m = WIZ.mostrar('Metodo')
        c = aconnect(WIZ.siguiente, self.siguiente, CFG['next'], CFG)
        c = aconnect(WIZ.anterior, self.anterior, CFG['prev'], CFG)

    def siguiente(self, CFG):
        '''
            Funcion para el evento del botón siguiente
        '''
        CFG['metodo'] = WIZ.formulario('Metodo').metodo
        print 'El metodo de instalación escogido es: {0}'.format(CFG['metodo'])

        if CFG['metodo'].split(':')[0] == 'MANUAL':
            CFG['disco'] = WIZ.formulario('Metodo').disco
            CFG['inicio'] = WIZ.formulario('Metodo').ini
            CFG['fin'] = WIZ.formulario('Metodo').fin
            #TODO: Todavía no se por qué hago esto pero ahí va:
            CFG['nuevo_fin'] = 1049

            print 'CFG: {0}\n'.format(CFG)
            PartManual(CFG)

        elif CFG['metodo'].split(':')[0] == 'TODO':
            CFG['disco'] = WIZ.formulario('Metodo').disco
            CFG['ini'] = WIZ.formulario('Metodo').ini
            CFG['fin'] = WIZ.formulario('Metodo').fin
            print 'CFG: {0}\n'.format(CFG)
            PartTodo(CFG)

        elif CFG['metodo'].split(':')[0] == 'LIBRE':
            CFG['disco'] = WIZ.formulario('Metodo').disco
            CFG['ini'] = WIZ.formulario('Metodo').ini
            CFG['fin'] = WIZ.formulario('Metodo').fin
            print 'CFG: {0}\n'.format(CFG)
            PartTodo(CFG)

        elif CFG['metodo'].split(':')[0] == 'REDIM':
            CFG['particion'] = CFG['metodo'].split(':')[0]
            print 'CFG: {0}\n'.format(CFG)
            PartAuto(CFG)

        else:
            pass

    def anterior(self, CFG):
        '''
            Función para el evento del botón anterior
        '''
        Teclado(CFG)

class PartAuto():
    '''
        Inicia el paso que redimensiona la partición
    '''
    def __init__(self, CFG):

        if WIZ.indice(WIZ.nombres, 'ParticionAuto') == -1:
            a = WIZ.agregar('ParticionAuto', particion_auto.Main(particion))

        frm_part_auto = WIZ.formulario('ParticionAuto')
        frm_part_auto.inicio(particion)
        WIZ.mostrar('ParticionAuto')

        c = aconnect(WIZ.siguiente, self.siguiente, CFG['next'], CFG)
        c = aconnect(WIZ.anterior, self.anterior, CFG['prev'], CFG)

    def siguiente(self, widget=None):
        '''
            Función para el evento del botón siguiente
        '''
        frm_part_auto = WIZ.formulario('ParticionAuto')
        CFG['particion'] = frm_part_auto.particion
        CFG['inicio'] = frm_part_auto.ini
        CFG['fin'] = frm_part_auto.fin
        CFG['nuevo_fin'] = frm_part_auto.cur_value
        CFG['tipo'] = frm_part_auto.metodo
        CFG['swap'] = frm_part_auto.swap
        CFG['fs'] = frm_part_auto.fs

        if CFG['tipo'] == 'particion_4':
            data = [CFG]
            PartManual(data)
        else:
            Usuario()

    def anterior(self, widget=None):
        '''
            Función para el evento del botón anterior
        '''
        Metodo()

class PartTodo():
    '''
        Inicia el paso que particiona el disco
    '''
    def __init__(self, CFG):

        self.disco = CFG['disco']
        self.ini = CFG['ini']
        self.fin = CFG['fin']

        if WIZ.indice(WIZ.nombres, 'PartTodo') == -1:
            a = WIZ.agregar('PartTodo',
                particion_todo.Main(self.disco, self.ini, self.fin)
                )

        m = WIZ.mostrar('PartTodo')
        c = aconnect(WIZ.siguiente, self.siguiente, CFG['next'], CFG)
        c = aconnect(WIZ.anterior, self.anterior, CFG['prev'], CFG)

    def siguiente(self, CFG):
        '''
            Función para el evento del botón siguiente
        '''
        CFG['ini'] = WIZ.formulario('PartTodo').ini
        CFG['fin'] = WIZ.formulario('PartTodo').fin
        CFG['tipo'] = WIZ.formulario('PartTodo').metodo

        if CFG['tipo'] == 'particion_4':
            PartManual(CFG)
        else:
            Usuario(CFG)

    def anterior(self, CFG):
        '''
            Función para el evento del botón anterior
        '''
        Metodo(CFG)

class PartManual():
    '''
        Inicia el paso que particiona el disco de forma manual
    '''
    def __init__(self, data):
        if WIZ.indice(WIZ.nombres, 'PartManual') == -1:
            WIZ.agregar('PartManual', particion_manual.Main(data))
        WIZ.mostrar('PartManual')

        c = aconnect(WIZ.siguiente, self.siguiente, CFG['next'], CFG)
        c = aconnect(WIZ.anterior, self.anterior, CFG['prev'], CFG)

    def siguiente(self, widget=None):
        '''
            Función para el evento del botón siguiente
        '''
        frm_part_manual = WIZ.formulario('PartManual')
        CFG['lista_manual'] = frm_part_manual.lista
        CFG['disco'] = frm_part_manual.disco
        if frm_part_manual.raiz == False:
            self.msg_error("Debe existir una partición raiz (/)")
            return
        Usuario(CFG)

    def anterior(self, widget=None):
        '''
            Función para el evento del botón anterior
        '''
        Metodo(CFG)

    def msg_error(self, mensaje):
        '''
            Función que muestra el mensaje de error
        '''
        dialog = gtk.MessageDialog(WIZ,
             gtk.DIALOG_MODAL,
             gtk.MESSAGE_ERROR,
             gtk.BUTTONS_OK,
             mensaje)
        response = dialog.run()
        dialog.destroy()

class Usuario():
    '''
        Inicia el paso que crea el usuario del sistema
    '''
    def __init__(self, CFG):

        if WIZ.indice(WIZ.nombres, 'UsuarioRoot') == -1:
            a = WIZ.agregar('UsuarioRoot', usuario.Main())

        m = WIZ.mostrar('UsuarioRoot')
        c = aconnect(WIZ.siguiente, self.siguiente, CFG['next'], CFG)
        c = aconnect(WIZ.anterior, self.anterior, CFG['prev'], CFG)

    def siguiente(self, CFG):
        '''
            Función para el evento del botón siguiente
        '''
        frm_usuario_root = WIZ.formulario('UsuarioRoot')
        CFG['passroot'] = frm_usuario_root.txt_passroot.get_text()
        CFG['passroot2'] = frm_usuario_root.txt_passroot2.get_text()
        CFG['nombre'] = frm_usuario_root.txt_nombre.get_text()
        CFG['usuario'] = frm_usuario_root.txt_usuario.get_text()
        CFG['passuser'] = frm_usuario_root.txt_passuser.get_text()
        CFG['passuser2'] = frm_usuario_root.txt_passuser2.get_text()
        CFG['maquina'] = frm_usuario_root.txt_maquina.get_text()
        CFG['oem'] = frm_usuario_root.chkoem.get_active()

        if CFG['oem'] == False:
            if CFG['passroot'].strip() == '':
                self.msg_error("Debe escribir una contraseña para root")
                return
            if CFG['passroot'] != CFG['passroot2']:
                self.msg_error("Las contraseñas de root no coinciden")
                return
            if CFG['nombre'].strip() == '':
                self.msg_error("Debe escribir un nombre")
                return
            if CFG['usuario'].strip() == '':
                self.msg_error("Debe escribir un nombre de usuario")
                return
            if re.compile('^[a-z][-a-z-0-9]*$').search(CFG['usuario']) == None:
                self.msg_error("El nombre de usuario no está correctamente escrito")
                return
            if CFG['passuser'].strip() == '':
                self.msg_error("Debe escribir una contraseña para el usuario")
                return
            if CFG['passuser'] != CFG['passuser2']:
                self.msg_error("Las contraseñas del usuario no coinciden")
                return
            if re.compile("^(([a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])$").search(CFG['maquina']) == None:
                self.msg_error("El nombre de la máquina no está correctamente escrito")
                return
        Accesibilidad()

    def anterior(self, CFG):
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
        dialog = gtk.MessageDialog(WIZ,
             gtk.DIALOG_MODAL,
             gtk.MESSAGE_ERROR,
             gtk.BUTTONS_OK,
             mensaje)
        response = dialog.run()
        dialog.destroy()

class Accesibilidad():
    '''
        Inicia el paso que muestr la información general de la instalación
    '''
    def __init__(self):
        global ID_SIGUIENTE, ID_ANTERIOR, CFG
        if WIZ.indice(WIZ.nombres, 'accesibilidad') == -1:
            WIZ.agregar('accesibilidad', accesibilidad.Main())
        WIZ.mostrar('accesibilidad')
        c = aconnect(WIZ.siguiente, self.siguiente, CFG['next'], CFG)
        c = aconnect(WIZ.anterior, self.anterior, CFG['prev'], CFG)
    def siguiente(self, widget=None):
        '''
            Función para el evento del botón siguiente
        '''
        frm_accesibilidad = WIZ.formulario('accesibilidad')
        CFG['chkgdm'] = frm_accesibilidad.chkgdm.get_active()
        Info()
    def anterior(self, widget=None):
        '''
            Función para el evento del botón anterior
        '''
        Usuario()

class Info():
    '''
        Inicia el paso que muestr la información general de la instalación
    '''
    def __init__(self):
        global ID_SIGUIENTE, ID_ANTERIOR, CFG
        if WIZ.indice(WIZ.nombres, 'info') == -1:
            WIZ.agregar('info', info.Main(CFG))
        WIZ.mostrar('info')
        frm_info = WIZ.formulario('info')
        frm_info.mostrar_info()
        c = aconnect(WIZ.siguiente, self.siguiente, CFG['next'], CFG)
        c = aconnect(WIZ.anterior, self.anterior, CFG['prev'], CFG)

    def siguiente(self, widget=None):
        '''
            Función para el evento del botón siguiente
        '''
        Instalacion()

    def anterior(self, widget=None):
        '''
            Función para el evento del botón anterior
        '''
        Accesibilidad()

class Instalacion():
    '''
        Inicia el paso que realiza la instalación del sistema
    '''
    def __init__(self):

        if WIZ.indice(WIZ.nombres, 'Instalacion') == -1:
            WIZ.agregar('Instalacion', instalacion.Main(CFG, WIZ))

        WIZ.mostrar('Instalacion')
        c = aconnect(WIZ.siguiente, self.siguiente, CFG['next'], CFG)
        c = aconnect(WIZ.anterior, self.anterior, CFG['prev'], CFG)

    def siguiente(self, widget=None):
        '''
            Función para el evento del botón cerrar
        '''
        WIZ.close()

    def anterior(self, widget=None):
        '''
            Función para el evento del botón reiniciar
        '''
        os.system('reboot')

if __name__ == "__main__":
    if os.geteuid() != 0:
        dialog = UserMessage(
            message=MAIN_ROOT_ERROR_MSG, title=MAIN_ROOT_ERROR_TITLE,
            mtype=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK,
            c_1=gtk.RESPONSE_OK, f_1=sys.exit, p_1=(1,)
            )
    else:

        WIZ = Wizard(700, 450, "Canaima Instalador", BANNER)
        app = Bienvenida(CFG)
        gtk.main()
        sys.exit()

