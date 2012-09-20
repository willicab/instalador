#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Módulos globales
import gtk, os, sys, re, Image

# Módulos locales
from canaimainstalador.pasos.bienvenida import PasoBienvenida
from canaimainstalador.pasos.teclado import PasoTeclado
from canaimainstalador.pasos.metodo import PasoMetodo
from canaimainstalador.pasos.particion_auto import PasoPartAuto
from canaimainstalador.pasos.particion_todo import PasoPartTodo
from canaimainstalador.pasos.particion_manual import PasoPartManual
from canaimainstalador.pasos.instalacion import PasoInstalacion
from canaimainstalador.pasos.usuario import PasoUsuario
from canaimainstalador.pasos.accesibilidad import PasoAccesibilidad
from canaimainstalador.pasos.info import PasoInfo
from canaimainstalador.clases.common import UserMessage, aconnect
from canaimainstalador.translator import MAIN_ROOT_ERROR_MSG, MAIN_ROOT_ERROR_TITLE
from canaimainstalador.config import *

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
        self.set_icon_from_file('canaimainstalador/data/img/icon.png')
        self.titulo = titulo
        self.set_title(titulo)
        self.set_size_request(ancho, alto)
        self.set_resizable(0)
        self.set_border_width(0)

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

        self.cancelar.connect('clicked', self.close)
        self.connect("delete-event", self.close)

        self.show_all()

    def close(self, widget=None, event=None):
        '''
            Cierra la ventana
        '''
        return UserMessage(
            '¿Está seguro que desea cancelar la instalación?', 'Salir',
            gtk.MESSAGE_WARNING, gtk.BUTTONS_YES_NO, c_1 = gtk.RESPONSE_YES,
            f_1 = gtk.main_quit, p_1 = ()
            )

    def next(self, nombre, init, params, paso):
        '''
            muestra el paso especificado en nombre
        '''
        if not nombre in self.pasos:
            if self.actual != nombre:
                if self.actual != '':
                    self.pasos[self.actual].hide_all()
                self.actual = nombre

            init(params)
            self.pasos[nombre] = paso
            self.c_pasos.add(self.pasos[nombre])
            self.pasos[nombre].show_all()

    def previous(self, nombre, init, params):
        '''
            muestra el paso especificado en nombre
        '''
        if nombre in self.pasos:
            if self.actual != nombre:
                if self.actual != '':
                    self.pasos[self.actual].hide_all()
                    self.c_pasos.remove(self.pasos[self.actual])
                    del self.pasos[self.actual]
                self.actual = nombre

            init(params)
            self.pasos[nombre].show_all()

    def formulario(self, nombre):
        '''
            devulve el objeto asociado al paso
        '''
        if nombre in self.pasos:
            return self.pasos[nombre]
        else:
            return False

class Bienvenida():
    '''
        Inicia el paso que muestra el mensaje de bienvenida
    '''
    def __init__(self, CFG):
        CFG['s'] = aconnect(CFG['w'].siguiente, CFG['s'], self.siguiente, (CFG))
        s = CFG['w'].anterior.set_sensitive(False)

    def init(self, CFG):
        m = CFG['w'].next('Bienvenida', Bienvenida, (CFG), PasoBienvenida(CFG))

    def siguiente(self, CFG):
        n = CFG['w'].next('Teclado', Teclado, (CFG), PasoTeclado(CFG))

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
        print 'Distribución de teclado seleccionada: {0}'.format(CFG['teclado'])

        m = CFG['w'].next('Metodo', Metodo, (CFG), PasoMetodo(CFG))

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
        CFG['particiones'] = CFG['w'].formulario('Metodo').particiones
        print 'El metodo de instalación escogido es: {0}'.format(CFG['metodo']['tipo'])
        print 'CFG: {0}'.format(CFG)

        if CFG['metodo']['tipo'] == 'MANUAL':
            m = CFG['w'].next('PartManual', PartManual, (CFG), PasoPartManual(CFG))
        elif CFG['metodo']['tipo'] == 'TODO' or CFG['metodo']['tipo'] == 'LIBRE':
            m = CFG['w'].next('PartTodo', PartTodo, (CFG), PasoPartTodo(CFG))
        elif CFG['metodo']['tipo'] == 'REDIM':
            m = CFG['w'].next('PartAuto', PartAuto, (CFG), PasoPartAuto(CFG))
        else:
            pass

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
        CFG['acciones'] = CFG['w'].formulario('PartAuto').acciones
        m = CFG['w'].next('Usuario', Usuario, (CFG), PasoUsuario(CFG))

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
        CFG['acciones'] = CFG['w'].formulario('PartAuto').acciones
        m = CFG['w'].next('Usuario', Usuario, (CFG), PasoUsuario(CFG))

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
        m = CFG['w'].next('Usuario', Usuario, (CFG), PasoUsuario(CFG))

class Usuario():
    '''
        Inicia el paso que crea el usuario del sistema
    '''
    def __init__(self, CFG):
        CFG['s'] = aconnect(CFG['w'].siguiente, CFG['s'], self.siguiente, CFG)
        CFG['s'] = aconnect(CFG['w'].anterior, CFG['s'], self.anterior, CFG)

    def anterior(self, CFG):
        m = CFG['w'].previous('PartAuto', PartAuto, (CFG))
        m = CFG['w'].previous('PartTodo', PartTodo, (CFG))
        m = CFG['w'].previous('PartManual', PartManual, (CFG))
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
                message = "Debe escribir una contraseña para el administrador."
                UserMessage(message, 'ERROR', gtk.MESSAGE_ERROR, gtk.BUTTONS_OK)
                return
            if CFG['passroot'] != CFG['passroot2']:
                message = "Las contraseñas de administrador no coinciden."
                UserMessage(message, 'ERROR', gtk.MESSAGE_ERROR, gtk.BUTTONS_OK)
                return
            if CFG['nombre'].strip() == '':
                message = "Debe escribir un nombre."
                UserMessage(message, 'ERROR', gtk.MESSAGE_ERROR, gtk.BUTTONS_OK)
                return
            if CFG['usuario'].strip() == '':
                message = "Debe escribir un nombre de usuario."
                UserMessage(message, 'ERROR', gtk.MESSAGE_ERROR, gtk.BUTTONS_OK)
                return
            if re.compile('^[a-z][-a-z-0-9]*$').search(CFG['usuario']) == None:
                message = "El nombre de usuario tiene caracteres inválidos."
                UserMessage(message, 'ERROR', gtk.MESSAGE_ERROR, gtk.BUTTONS_OK)
                return
            if CFG['passuser'].strip() == '':
                message = "Debe escribir una contraseña para el usuario."
                UserMessage(message, 'ERROR', gtk.MESSAGE_ERROR, gtk.BUTTONS_OK)
                return
            if CFG['passuser'] != CFG['passuser2']:
                message = "Las contraseñas de usuario no coinciden."
                UserMessage(message, 'ERROR', gtk.MESSAGE_ERROR, gtk.BUTTONS_OK)
                return
            if re.compile("^(([a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])$").search(CFG['maquina']) == None:
                message = "El nombre de la máquina no está correctamente escrito."
                UserMessage(message, 'ERROR', gtk.MESSAGE_ERROR, gtk.BUTTONS_OK)
                return
            m = CFG['w'].next('Accesibilidad', Accesibilidad, (CFG), PasoAccesibilidad(CFG))

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
        m = CFG['w'].next('Info', Info, (CFG), PasoInfo(CFG))

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
        m = CFG['w'].next('Instalacion', Instalacion, (CFG), PasoInstalacion(CFG))

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
