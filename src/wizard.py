#!/usr/bin/env python
#-*- coding: UTF-8 -*-
# Autor: William Cabrera
# Fecha: 11/10/2011

import pygtk
pygtk.require('2.0')
import gtk
import Image
import threading

class Barra(gtk.ProgressBar):
    '''
        Clase que muestra la barra de progreso
    '''
    hilo = True
    def __init__(self):
        gtk.ProgressBar.__init__(self)
        #self.hilo = True

    def accion(self, accion): # Agrega el mensaje de acción
        '''
            Muestra el texto en la barra de progreso
        '''
        self.set_text(accion)

    def start(self): # Inicia la animación del progress bar
        '''
            Inicia la animación de la barra
        '''
        #self.hilo == True
        self.show()
        thread = threading.Thread(target=self.anim, args=())
        thread.start()

    def stop(self): # finaliza la animación del progress bar
        '''
            Detiene la animación de la barra
        '''
        #self.hilo = False
        self.hide()

    def anim(self): # Genera la animación en el progress bar
        '''
            Función que realiza la animación
        '''
        import time
        while self.hilo == True:
            self.pulse()
            time.sleep(0.1)

class Wizard(gtk.Window):
    '''
        Clase del Asistente
    '''
    __c_principal = gtk.Fixed() # Contenedor Principal
    btn_aplicar = gtk.Button()  # Botón Aplicar
    c_pasos = gtk.VBox()
    #pasos = {}                # Pasos
    pasos = []
    nombres = []
    contenidos = []
    __paso = ''                 # Paso actual
    __count = 0                 # Número de pasos
    def __init__(self, ancho, alto, titulo, banner):
        #Creo la ventana
        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        gtk.Window.set_position(self, gtk.WIN_POS_CENTER_ALWAYS)
        self.set_icon_from_file('data/canaima.png')
        self.titulo = titulo
        self.set_title(titulo)
        self.set_size_request(ancho, alto)
        self.set_resizable(0)
        self.set_border_width(0)
        self.connect("destroy", self.close)
        #Creo el contenedor principal
        self.add(self.__c_principal)
        self.__c_principal.show()
        #Calculo tamaño del banner
        self.banner_img = Image.open (banner)
        self.banner_w = self.banner_img.size[0]
        self.banner_h = self.banner_img.size[1]
        #Creo el banner
        self.banner = gtk.Image()
        self.banner.set_from_file(banner)
        self.banner.set_size_request(ancho, self.banner_h)
        self.__c_principal.put(self.banner, 0, 0)
        self.banner.show()
        #Creo el contenedor de los pasos
        self.c_pasos.set_size_request((ancho - 10), (alto - 50 - self.banner_h))
        self.__c_principal.put(self.c_pasos, 5, (self.banner_h + 5))
        self.c_pasos.show()

        #self.banner = gtk.Image()
        #self.banner.set_from_file(banner)
        #self.banner.set_size_request(ancho, self.banner_h)
        #self.__c_principal.put(self.banner, 0, (alto - 80))
        #self.banner.show()

        self.botonera = gtk.Fixed()
        self.botonera.set_size_request(ancho, 40)
        self.__c_principal.put(self.botonera, 0, (alto - 40))
        self.botonera.show()


        #Creo la linea divisoria
        self.linea = gtk.HSeparator()
        self.linea.set_size_request(ancho, 5)
        self.botonera.put(self.linea, 0, 0)
        self.linea.show()
        #Creo la botonera
        #Anterior
        self.btn_anterior = gtk.Button(stock=gtk.STOCK_GO_BACK)
        self.botonera.put(self.btn_anterior, (ancho - 180), 10)
        self.btn_anterior.set_size_request(80, 30)
        self.btn_anterior.show()
        #Siguiente
        self.btn_siguiente = gtk.Button(stock=gtk.STOCK_GO_FORWARD)
        self.botonera.put(self.btn_siguiente, (ancho - 90), 10)
        self.btn_siguiente.set_size_request(80, 30)
        self.btn_siguiente.show()
        #Cancelar
        self.btn_cancelar = gtk.Button(stock=gtk.STOCK_CANCEL)
        #self.botonera.put(self.btn_cancelar, (ancho - 180), 10)
        self.botonera.put(self.btn_cancelar, 10, 10)
        self.btn_cancelar.set_size_request(80, 30)
        self.btn_cancelar.connect("clicked", self.close)
        self.btn_cancelar.show()
        #Aceptar
#        self.btn_aplicar.set_label(btn_apply)
#        self.botonera.put(self.btn_aplicar, (ancho - 90), 10)
#        self.__c_principal.put(self.btn_aplicar, (ancho - 90), (alto - 30))
#        self.btn_aplicar.set_size_request(80, 30)

        self.barra = gtk.VBox()
        self.barra.set_size_request(ancho, 40)
        self.__c_principal.put(self.barra, 0, (alto - 40))
#        self.barra.show()

        self.lbl_info = gtk.Label('')
        self.lbl_info.set_size_request(590, 20)
        self.lbl_info.set_justify(gtk.JUSTIFY_CENTER)
        self.barra.add(self.lbl_info)
        self.lbl_info.show()

        self.progreso = Barra() # Barra de progreso
        self.progreso.set_size_request(590, 30)
        self.barra.add(self.progreso)
        self.progreso.set_pulse_step(0.05)
        self.progreso.show()

    def mostrar_barra(self):
        '''
            Muestra la barra de progreso y oculta la botonera
        '''
        self.botonera.hide()
        self.barra.show()
        self.progreso.start()

    def ocultar_barra(self):
        '''
            Oculta la barra de progreso y muestra la botonera
        '''
        self.barra.hide()
        self.botonera.show()
        self.progreso.stop()

    def accion(self, accion):
        '''
            llama a la función accion de la barra
        '''
        self.progreso.accion(accion)

    def info_barra(self, info):
        '''
            Mustra la info de la etiqueta sobre la barra de progreso
        '''
        self.lbl_info.set_text(info)

    def close(self, widget=None):
        '''
            Cierra la ventana
        '''
        #dialog = gtk.MessageDialog(self, gtk.DIALOG_MODAL,
        #                           gtk.MESSAGE_INFO, gtk.BUTTONS_YES_NO,
        #                       "¿Está seguro que desea salir del asistente?")
        #dialog.set_title("Salir del Instalador")
        #response = dialog.run()
        #dialog.destroy()
        #if response == gtk.RESPONSE_YES:
        #    gtk.main_quit()
        #    return False
        #else:
        #    return True
        #self.destroy()
        #print widget
        self.progreso.hilo = False
        gtk.main_quit()

    def agregar(self, nombre, paso):
        '''
            Oculta la barra de progreso y muestra la botonera
        '''
        if self.indice(self.nombres, nombre) != -1:
            return
        self.nombres.append(nombre)
        self.pasos.append(paso)

    def mostrar(self, nombre):
        '''
            muestra el paso especificado en nombre
        '''
        if self.__paso != '':
            self.pasos[self.indice(self.nombres, self.__paso)].hide()
        if self.indice(self.contenidos, nombre) == -1:
            self.c_pasos.add(self.pasos[self.indice(self.nombres, nombre)])
            self.contenidos.append(nombre)
        self.pasos[self.indice(self.nombres, nombre)].show()
        self.__paso = nombre

    def indice(self, lista, valor):
        '''
            devuelve el indice del paso
        '''
        try:
            i = lista.index(valor)
        except ValueError:
            i = -1
        return i

    def formulario(self, nombre):
        '''
            devulve el objeto asociado al paso
        '''
        return self.pasos[self.indice(self.nombres, nombre)]
