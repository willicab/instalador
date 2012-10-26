#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ==============================================================================
# PAQUETE: canaima-instalador
# ARCHIVO: canaimainstalador/main.py
# COPYRIGHT:
#       (C) 2012 William Abrahan Cabrera Reyes <william@linux.es>
#       (C) 2012 Erick Manuel Birbe Salazar <erickcion@gmail.com>
#       (C) 2012 Luis Alejandro Martínez Faneyth <luis@huntingbears.com.ve>
# LICENCIA: GPL-3
# ==============================================================================
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# COPYING file for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# CODE IS POETRY

# Módulos globales
import gtk, os, re, Image

# Módulos locales
from canaimainstalador.pasos.bienvenida import PasoBienvenida
from canaimainstalador.pasos.teclado import PasoTeclado
from canaimainstalador.pasos.metodo import PasoMetodo
from canaimainstalador.pasos.particion_auto import PasoPartAuto
from canaimainstalador.pasos.particion_todo import PasoPartTodo
from canaimainstalador.pasos.particion_manual import PasoPartManual
from canaimainstalador.pasos.instalacion import PasoInstalacion
from canaimainstalador.pasos.usuario import PasoUsuario
from canaimainstalador.pasos.info import PasoInfo
from canaimainstalador.clases.common import UserMessage, AboutWindow, aconnect, \
    ThreadGenerator
from canaimainstalador.config import CFG, BAR_ICON

class Wizard(gtk.Window):
    def __init__(self, ancho, alto, titulo, banner):
        self.pasos = {}
        self.actual = ''

        # Creo la ventana
        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        gtk.Window.set_position(self, gtk.WIN_POS_CENTER_ALWAYS)
        self.set_icon_from_file(BAR_ICON)
        self.titulo = titulo
        self.set_title(titulo)
        self.set_size_request(ancho, alto)
        self.set_resizable(0)
        self.set_border_width(0)

        # Creo el contenedor principal
        self.c_principal = gtk.Fixed()
        self.add(self.c_principal)

        # Calculo tamaño del banner
        self.banner_img = Image.open(banner)
        self.banner_w = self.banner_img.size[0]
        self.banner_h = self.banner_img.size[1]

        # Creo el banner
        self.banner = gtk.Image()
        self.banner.set_from_file(banner)
        self.banner.set_size_request(ancho, self.banner_h)
        self.c_principal.put(self.banner, 0, 0)

        # Creo el contenedor de los pasos
        self.c_pasos = gtk.VBox()
        self.c_pasos.set_size_request((ancho - 10), (alto - 50 - self.banner_h))
        self.c_principal.put(self.c_pasos, 5, (self.banner_h + 5))

        # Creo la botonera
        self.botonera = gtk.Fixed()
        self.botonera.set_size_request(ancho, 40)
        self.c_principal.put(self.botonera, 0, (alto - 40))

        # Creo la linea divisoria
        self.linea = gtk.HSeparator()
        self.linea.set_size_request(ancho, 5)
        self.botonera.put(self.linea, 0, 0)

        # Anterior
        self.anterior = gtk.Button(stock=gtk.STOCK_GO_BACK)
        self.anterior.set_size_request(100, 30)
        self.botonera.put(self.anterior, (ancho - 210), 10)

        # Siguiente
        self.siguiente = gtk.Button(stock=gtk.STOCK_GO_FORWARD)
        self.siguiente.set_size_request(100, 30)
        self.botonera.put(self.siguiente, (ancho - 110), 10)

        # Cancelar
        self.cancelar = gtk.Button(stock=gtk.STOCK_QUIT)
        self.cancelar.set_size_request(100, 30)
        self.cancelar.connect('clicked', self.close)
        self.botonera.put(self.cancelar, 10, 10)

        # Acerca
        self.acerca = gtk.Button(stock=gtk.STOCK_ABOUT)
        self.acerca.set_size_request(100, 30)
        self.acerca.connect('clicked', AboutWindow)
        self.botonera.put(self.acerca, 110, 10)

        self.connect("destroy", self.close)
        self.connect("delete-event", self.close)

        self.show_all()

    def close(self, widget=None, event=None):
        '''
            Cierra la ventana
        '''
        return UserMessage(
            '¿Está seguro que desea cancelar la instalación?', 'Salir',
            gtk.MESSAGE_WARNING, gtk.BUTTONS_YES_NO, c_1=gtk.RESPONSE_YES,
            f_1=gtk.main_quit, p_1=()
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
        CFG['w'].anterior.set_sensitive(False)

    def init(self, CFG):
        CFG['w'].next('Bienvenida', Bienvenida, (CFG), PasoBienvenida(CFG))

    def siguiente(self, CFG):
        CFG['w'].next('Teclado', Teclado, (CFG), PasoTeclado(CFG))

class Teclado():
    '''
        Inicia el paso que escoge la distribución del teclado
    '''
    def __init__(self, CFG):
        CFG['s'] = aconnect(CFG['w'].siguiente, CFG['s'], self.siguiente, CFG)
        CFG['s'] = aconnect(CFG['w'].anterior, CFG['s'], self.anterior, CFG)
        CFG['w'].anterior.set_sensitive(True)

    def anterior(self, CFG):
        CFG['w'].previous('Bienvenida', Bienvenida, (CFG))

    def siguiente(self, CFG):
        CFG['teclado'] = CFG['w'].formulario('Teclado').distribucion
        print 'Distribución de teclado seleccionada: {0}'.format(CFG['teclado'])

        CFG['w'].next('Metodo', Metodo, (CFG), PasoMetodo(CFG))

class Metodo():
    '''
        Inicia el paso que escoge el método de particionado
    '''
    def __init__(self, CFG):
        CFG['s'] = aconnect(CFG['w'].siguiente, CFG['s'], self.siguiente, CFG)
        CFG['s'] = aconnect(CFG['w'].anterior, CFG['s'], self.anterior, CFG)

    def anterior(self, CFG):
        CFG['w'].previous('Teclado', Teclado, (CFG))

    def siguiente(self, CFG):
        CFG['metodo'] = CFG['w'].formulario('Metodo').metodo
        CFG['particiones'] = CFG['w'].formulario('Metodo').particiones
        print 'El metodo de instalación escogido es: {0}'.format(CFG['metodo']['tipo'])
        print 'CFG: {0}'.format(CFG)

        if CFG['metodo']['tipo'] == 'MANUAL':
            CFG['w'].next('PartManual', PartManual, (CFG), PasoPartManual(CFG))
        elif CFG['metodo']['tipo'] == 'TODO' or CFG['metodo']['tipo'] == 'LIBRE':
            CFG['w'].next('PartTodo', PartTodo, (CFG), PasoPartTodo(CFG))
        elif CFG['metodo']['tipo'] == 'REDIM':
            CFG['w'].next('PartAuto', PartAuto, (CFG), PasoPartAuto(CFG))
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
        CFG['w'].previous('Metodo', Metodo, (CFG))

    def siguiente(self, CFG):
        CFG['acciones'] = CFG['w'].formulario('PartTodo').acciones
        CFG['forma'] = CFG['w'].formulario('PartTodo').forma
        CFG['w'].next('Usuario', Usuario, (CFG), PasoUsuario(CFG))
        print 'CFG: {0}'.format(CFG)

class PartAuto():
    '''
        Inicia el paso que redimensiona la partición
    '''
    def __init__(self, CFG):
        CFG['s'] = aconnect(CFG['w'].siguiente, CFG['s'], self.siguiente, CFG)
        CFG['s'] = aconnect(CFG['w'].anterior, CFG['s'], self.anterior, CFG)

    def anterior(self, CFG):
        CFG['w'].previous('Metodo', Metodo, (CFG))

    def siguiente(self, CFG):
        CFG['acciones'] = CFG['w'].formulario('PartAuto').acciones
        CFG['forma'] = CFG['w'].formulario('PartAuto').forma
        CFG['w'].next('Usuario', Usuario, (CFG), PasoUsuario(CFG))
        print 'CFG: {0}'.format(CFG)

class PartManual():
    '''
        Inicia el paso que particiona el disco
    '''
    def __init__(self, CFG):
        CFG['s'] = aconnect(CFG['w'].siguiente, CFG['s'], self.siguiente, CFG)
        CFG['s'] = aconnect(CFG['w'].anterior, CFG['s'], self.anterior, CFG)

    def anterior(self, CFG):
        CFG['w'].previous('Metodo', Metodo, (CFG))

    def siguiente(self, CFG):
        if CFG['w'].formulario('PartManual').raiz == False:
            message = "Debe existir una partición raiz (/)"
            UserMessage(message, 'ERROR', gtk.MESSAGE_ERROR, gtk.BUTTONS_OK)
            return False

        CFG['acciones'] = CFG['w'].formulario('PartManual').acciones
        CFG['w'].next('Usuario', Usuario, (CFG), PasoUsuario(CFG))
        print 'CFG: {0}'.format(CFG)

class Usuario():
    '''
        Inicia el paso que crea el usuario del sistema
    '''
    def __init__(self, CFG):
        CFG['s'] = aconnect(CFG['w'].siguiente, CFG['s'], self.siguiente, CFG)
        CFG['s'] = aconnect(CFG['w'].anterior, CFG['s'], self.anterior, CFG)

    def anterior(self, CFG):
        CFG['w'].previous('PartAuto', PartAuto, (CFG))
        CFG['w'].previous('PartTodo', PartTodo, (CFG))
        CFG['w'].previous('PartManual', PartManual, (CFG))
        CFG['w'].previous('Metodo', Metodo, (CFG))

    def siguiente(self, CFG):
        CFG['passroot1'] = CFG['w'].formulario('Usuario').txtpassroot1.get_text()
        CFG['passroot2'] = CFG['w'].formulario('Usuario').txtpassroot2.get_text()
        CFG['nombre'] = CFG['w'].formulario('Usuario').txtnombre.get_text()
        CFG['usuario'] = CFG['w'].formulario('Usuario').txtusuario.get_text()
        CFG['passuser1'] = CFG['w'].formulario('Usuario').txtpassuser1.get_text()
        CFG['passuser2'] = CFG['w'].formulario('Usuario').txtpassuser2.get_text()
        CFG['maquina'] = CFG['w'].formulario('Usuario').txtmaquina.get_text()
        CFG['oem'] = CFG['w'].formulario('Usuario').chkoem.get_active()
        CFG['gdm'] = CFG['w'].formulario('Usuario').chkgdm.get_active()

        if CFG['oem'] == False:
            if CFG['passroot1'].strip() == '':
                message = "Debe escribir una contraseña para el administrador."
                UserMessage(message, 'ERROR', gtk.MESSAGE_ERROR, gtk.BUTTONS_OK)
                return
            if CFG['passroot1'] != CFG['passroot2']:
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
            if CFG['passuser1'].strip() == '':
                message = "Debe escribir una contraseña para el usuario."
                UserMessage(message, 'ERROR', gtk.MESSAGE_ERROR, gtk.BUTTONS_OK)
                return
            if CFG['passuser1'] != CFG['passuser2']:
                message = "Las contraseñas de usuario no coinciden."
                UserMessage(message, 'ERROR', gtk.MESSAGE_ERROR, gtk.BUTTONS_OK)
                return
            if re.compile("^(([a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])$").search(CFG['maquina']) == None:
                message = "El nombre de la máquina no está correctamente escrito."
                UserMessage(message, 'ERROR', gtk.MESSAGE_ERROR, gtk.BUTTONS_OK)
                return

        CFG['w'].next('Info', Info, (CFG), PasoInfo(CFG))

class Info():
    '''
        Inicia el paso que muestr la información general de la instalación
    '''
    def __init__(self, CFG):
        CFG['s'] = aconnect(CFG['w'].siguiente, CFG['s'], self.siguiente, CFG)
        CFG['s'] = aconnect(CFG['w'].anterior, CFG['s'], self.anterior, CFG)

    def anterior(self, CFG):
        CFG['w'].previous('Usuario', Usuario, (CFG))

    def siguiente(self, CFG):
        CFG['w'].hide_all()
        PasoInstalacion(CFG)
