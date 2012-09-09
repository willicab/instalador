#!/usr/bin/env python
#-*- coding: UTF-8 -*-

# Módulos globales
import gtk, os, sys, re, Image

# Módulos locales
from instalador.pasos import bienvenida, teclado, metodo, particion_auto, particion_todo
from instalador.pasos import particion_manual, instalacion, usuario, accesibilidad, info
from instalador.constructor import UserMessage, aconnect
from instalador.translator import MAIN_ROOT_ERROR_MSG, MAIN_ROOT_ERROR_TITLE
from instalador.config import *

class Wizard(gtk.Window):
    '''
        Clase del Asistente
    '''
    pasos = {}                  # Pasos
    nombres = []                # Nombres
    contenidos = []             # Contenidos
    actual = ''                 # Paso actual
    __count = 0                 # Número de pasos
    __c_principal = gtk.Fixed() # Contenedor Principal
    btn_aplicar = gtk.Button()  # Botón Aplicar
    c_pasos = gtk.VBox()

    def __init__(self, ancho, alto, titulo, banner):
        # Creo la ventana
        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        gtk.Window.set_position(self, gtk.WIN_POS_CENTER_ALWAYS)
        self.set_icon_from_file('instalador/data/img/icon.png')
        self.titulo = titulo
        self.set_title(titulo)
        self.set_size_request(ancho, alto)
        self.set_resizable(0)
        self.set_border_width(0)
        self.connect("delete-event", self.close)

        # Creo el contenedor principal
        self.add(self.__c_principal)

        # Calculo tamaño del banner
        self.banner_img = Image.open(banner)
        self.banner_w = self.banner_img.size[0]
        self.banner_h = self.banner_img.size[1]

        # Creo el banner
        self.banner = gtk.Image()
        self.banner.set_from_file(banner)
        self.banner.set_size_request(ancho, self.banner_h)
        self.__c_principal.put(self.banner, 0, 0)

        # Creo el contenedor de los pasos
        self.c_pasos.set_size_request((ancho - 10), (alto - 50 - self.banner_h))
        self.__c_principal.put(self.c_pasos, 5, (self.banner_h + 5))

        # Creo la botonera
        self.botonera = gtk.Fixed()
        self.botonera.set_size_request(ancho, 40)
        self.__c_principal.put(self.botonera, 0, (alto - 40))

        # Creo la linea divisoria
        self.linea = gtk.HSeparator()
        self.linea.set_size_request(ancho, 5)
        self.botonera.put(self.linea, 0, 0)

        # Anterior
        self.anterior = gtk.Button(stock=gtk.STOCK_GO_BACK)
        self.botonera.put(self.anterior, (ancho - 210), 10)
        self.anterior.set_size_request(100, 30)

        # Siguiente
        self.siguiente = gtk.Button(stock=gtk.STOCK_GO_FORWARD)
        self.botonera.put(self.siguiente, (ancho - 110), 10)
        self.siguiente.set_size_request(100, 30)

        # Cancelar
        self.cancelar = gtk.Button(stock=gtk.STOCK_CANCEL)
        self.botonera.put(self.cancelar, 10, 10)
        self.cancelar.set_size_request(100, 30)
        self.cancelar.connect("clicked", self.close)

        self.show_all()

    def next(self, nombre, init, params, paso):
        '''
            muestra el paso especificado en nombre
        '''
        if self.actual != nombre:
            if self.actual != '':
                self.pasos[self.actual].hide_all()
            self.actual = nombre

        if not nombre in self.pasos:
            print nombre, paso, self.pasos
            self.pasos[nombre] = paso
            init(params)
            self.c_pasos.add(self.pasos[nombre])
            self.pasos[nombre].show_all()

    def previous(self, nombre, init, params):
        '''
            muestra el paso especificado en nombre
        '''
        if self.actual != nombre:
            if self.actual != '':
                self.pasos[self.actual].hide_all()
                self.c_pasos.remove(self.pasos[self.actual])
                del self.pasos[self.actual]
            self.actual = nombre

        if nombre in self.pasos:
            print nombre, self.pasos[nombre], self.pasos
            init(params)
            self.pasos[nombre].show_all()

    def formulario(self, nombre):
        '''
            devulve el objeto asociado al paso
        '''
        return self.pasos[nombre]

    def close(self, widget=None, event=None):
        '''
            Cierra la ventana
        '''
        message = '¿Está seguro que desea cancelar la instalación?'
        dialog = gtk.MessageDialog(
                self, gtk.DIALOG_MODAL, gtk.MESSAGE_WARNING,
                gtk.BUTTONS_YES_NO, message
                )
        dialog.set_title("Salir del Instalador")
        response = dialog.run()
        dialog.destroy()

        if response == gtk.RESPONSE_YES:
            gtk.main_quit()
            return False
        else:
            return True

class Bienvenida():
    '''
        Inicia el paso que muestra el mensaje de bienvenida
    '''
    def __init__(self, CFG):
        CFG['s'] = aconnect(CFG['w'].siguiente, CFG['s'], self.siguiente, (CFG))
        s = CFG['w'].anterior.set_sensitive(False)

    def init(self, CFG):
        m = CFG['w'].next('Bienvenida', Bienvenida, (CFG), bienvenida.Main())

    def siguiente(self, CFG):
        n = CFG['w'].next('Teclado', Teclado, (CFG), teclado.Main())
        print 'CFG: {0}'.format(CFG)

class Teclado():
    '''
        Inicia el paso que escoge la distribución del teclado
    '''
    def __init__(self, CFG):
        CFG['s'] = aconnect(CFG['w'].siguiente, CFG['s'], self.siguiente, CFG)
        CFG['s'] = aconnect(CFG['w'].anterior, CFG['s'], self.anterior, CFG)
        s = CFG['w'].anterior.set_sensitive(True)

    def anterior(self, CFG):
        m = CFG['w'].previous('Bienvenida', Bienvenida, (CFG))

    def siguiente(self, CFG):
        CFG['teclado'] = CFG['w'].formulario('Teclado').distribucion
        m = CFG['w'].next('Metodo', Metodo, (CFG), metodo.Main())
        print 'Distribución de teclado seleccionada: {0}'.format(CFG['teclado'])
        print 'CFG: {0}'.format(CFG)

class Metodo():
    '''
        Inicia el paso que escoge el método de particionado
    '''
    def __init__(self, CFG):
        CFG['s'] = aconnect(CFG['w'].siguiente, CFG['s'], self.siguiente, CFG)
        CFG['s'] = aconnect(CFG['w'].anterior, CFG['s'], self.anterior, CFG)

    def anterior(self, CFG):
        m = CFG['w'].previous('Teclado', Teclado, (CFG))

    def siguiente(self, CFG):
        CFG['metodo'] = CFG['w'].formulario('Metodo').metodo
        CFG['disco'] = CFG['w'].formulario('Metodo').disco
        CFG['particion'] = CFG['w'].formulario('Metodo').particion
        CFG['ini'] = CFG['w'].formulario('Metodo').ini
        CFG['fin'] = CFG['w'].formulario('Metodo').fin
        print CFG['disco'], CFG['metodo'], CFG['particion'], CFG['ini'], CFG['fin']

        print 'El metodo de instalación escogido es: {0}'.format(CFG['metodo'])
        print 'CFG: {0}\n'.format(CFG)

        if CFG['metodo'] == 'MANUAL':
            m = CFG['w'].next('PartManual', PartManual, (CFG), particion_manual.Main(CFG))
        elif CFG['metodo'] == 'TODO':
            m = CFG['w'].next('PartTodo', PartTodo, (CFG), particion_todo.Main(CFG))
        elif CFG['metodo'] == 'LIBRE':
            m = CFG['w'].next('PartTodo', PartTodo, (CFG), particion_todo.Main(CFG))
        elif CFG['metodo'] == 'REDIM':
            m = CFG['w'].next('PartAuto', PartAuto, (CFG), particion_auto.Main(CFG))
        else:
            pass

class PartAuto():
    '''
        Inicia el paso que redimensiona la partición
    '''
    def __init__(self, CFG):
        CFG['s'] = aconnect(CFG['w'].siguiente, CFG['s'], self.siguiente, CFG)
        CFG['s'] = aconnect(CFG['w'].anterior, CFG['s'], self.anterior, CFG)

    def anterior(self, CFG):
        m = CFG['w'].previous('Metodo', Metodo, (CFG))

    def siguiente(self, CFG):
        CFG['particion'] = CFG['w'].formulario('PartAuto').particion
        CFG['inicio'] = CFG['w'].formulario('PartAuto').ini
        CFG['fin'] = CFG['w'].formulario('PartAuto').fin
        CFG['nuevo_fin'] = CFG['w'].formulario('PartAuto').cur_value
        CFG['forma'] = CFG['w'].formulario('PartAuto').forma
        CFG['swap'] = CFG['w'].formulario('PartAuto').swap
        CFG['fs'] = CFG['w'].formulario('PartAuto').fs

        if CFG['tipo'] == 'particion_4':
            m = CFG['w'].next('PartManual', PartManual, (CFG), particion_manual.Main(CFG))
        else:
            m = CFG['w'].next('Usuario', Usuario, (CFG), particion_manual.Main(CFG))

class PartTodo():
    '''
        Inicia el paso que particiona el disco
    '''
    def __init__(self, CFG):
        CFG['s'] = aconnect(CFG['w'].siguiente, CFG['s'], self.siguiente, CFG)
        CFG['s'] = aconnect(CFG['w'].anterior, CFG['s'], self.anterior, CFG)

    def anterior(self, CFG):
        m = CFG['w'].previous('Metodo', Metodo, (CFG))

    def siguiente(self, CFG):
        CFG['ini'] = CFG['w'].formulario('PartTodo').ini
        CFG['fin'] = CFG['w'].formulario('PartTodo').fin
        CFG['forma'] = CFG['w'].formulario('PartTodo').forma

        if CFG['tipo'] == 'particion_4':
            m = CFG['w'].next('PartManual', PartManual, (CFG), particion_manual.Main(CFG))
        else:
            m = CFG['w'].next('Usuario', Usuario, (CFG), particion_manual.Main(CFG))

class PartManual():
    '''
        Inicia el paso que particiona el disco
    '''
    def __init__(self, CFG):
        CFG['s'] = aconnect(CFG['w'].siguiente, CFG['s'], self.siguiente, CFG)
        CFG['s'] = aconnect(CFG['w'].anterior, CFG['s'], self.anterior, CFG)

    def anterior(self, CFG):
        m = CFG['w'].previous('Metodo', Metodo, (CFG))

    def siguiente(self, CFG):
        if CFG['w'].formulario('PartManual').raiz == False:
            msg_error("Debe existir una partición raiz (/)")
            return False

        CFG['lista_manual'] = CFG['w'].formulario('PartManual').lista
        CFG['disco'] = CFG['w'].formulario('PartManual').disco
        m = CFG['w'].next('Usuario', Usuario, (CFG), particion_manual.Main(CFG))

class Usuario():
    '''
        Inicia el paso que crea el usuario del sistema
    '''
    def __init__(self, CFG):
        CFG['s'] = aconnect(CFG['w'].siguiente, CFG['s'], self.siguiente, CFG)
        CFG['s'] = aconnect(CFG['w'].anterior, CFG['s'], self.anterior, CFG)

    def anterior(self, CFG):
        m = CFG['w'].previous('Metodo', Metodo, (CFG))

    def siguiente(self, CFG):
        CFG['passroot'] = CFG['w'].formulario('Usuario').txt_passroot.get_text()
        CFG['passroot2'] = CFG['w'].formulario('Usuario').txt_passroot2.get_text()
        CFG['nombre'] = CFG['w'].formulario('Usuario').txt_nombre.get_text()
        CFG['usuario'] = CFG['w'].formulario('Usuario').txt_usuario.get_text()
        CFG['passuser'] = CFG['w'].formulario('Usuario').txt_passuser.get_text()
        CFG['passuser2'] = CFG['w'].formulario('Usuario').txt_passuser2.get_text()
        CFG['maquina'] = CFG['w'].formulario('Usuario').txt_maquina.get_text()
        CFG['oem'] = CFG['w'].formulario('Usuario').chkoem.get_active()

        if CFG['oem'] == False:
            if CFG['passroot'].strip() == '':
                msg_error("Debe escribir una contraseña para root")
                return
            if CFG['passroot'] != CFG['passroot2']:
                msg_error("Las contraseñas de root no coinciden")
                return
            if CFG['nombre'].strip() == '':
                msg_error("Debe escribir un nombre")
                return
            if CFG['usuario'].strip() == '':
                msg_error("Debe escribir un nombre de usuario")
                return
            if re.compile('^[a-z][-a-z-0-9]*$').search(CFG['usuario']) == None:
                msg_error("El nombre de usuario tiene caracteres inválidos")
                return
            if CFG['passuser'].strip() == '':
                msg_error("Debe escribir una contraseña para el usuario")
                return
            if CFG['passuser'] != CFG['passuser2']:
                msg_error("Las contraseñas del usuario no coinciden")
                return
            if re.compile("^(([a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])$").search(CFG['maquina']) == None:
                msg_error("El nombre de la máquina no está correctamente escrito")
                return
            m = CFG['w'].next('Accesibilidad', Accesibilidad, (CFG), accesibilidad.Main(CFG))

class Accesibilidad():
    '''
        Inicia el paso que muestr la información general de la instalación
    '''
    def __init__(self, CFG):
        CFG['s'] = aconnect(CFG['w'].siguiente, CFG['s'], self.siguiente, CFG)
        CFG['s'] = aconnect(CFG['w'].anterior, CFG['s'], self.anterior, CFG)

    def anterior(self, CFG):
        m = CFG['w'].previous('Usuario', Usuario, (CFG))

    def siguiente(self, widget=None):
        CFG['chkgdm'] = CFG['w'].formulario('Accesibilidad').chkgdm.get_active()
        m = CFG['w'].next('Info', Info, (CFG), info.Main(CFG))

class Info():
    '''
        Inicia el paso que muestr la información general de la instalación
    '''
    def __init__(self, CFG):
        CFG['s'] = aconnect(CFG['w'].siguiente, CFG['s'], self.siguiente, CFG)
        CFG['s'] = aconnect(CFG['w'].anterior, CFG['s'], self.anterior, CFG)

    def anterior(self, CFG):
        m = CFG['w'].previous('Accesibilidad', Accesibilidad, (CFG))

    def siguiente(self, CFG):
        m = CFG['w'].next('Instalacion', Instalacion, (CFG), instalacion.Main(CFG))

class Instalacion():
    '''
        Inicia el paso que realiza la instalación del sistema
    '''
    def __init__(self, CFG):
        CFG['s'] = aconnect(CFG['w'].siguiente, CFG['s'], self.siguiente, CFG)
        CFG['s'] = aconnect(CFG['w'].anterior, CFG['s'], self.anterior, CFG)

    def anterior(self, CFG):
        os.system('reboot')

    def siguiente(self, CFG):
        CFG['w'].close()
