#!/usr/bin/env python
#-*- coding: UTF-8 -*-
'''Script para probar la clase'''
# Autor: William Cabrera
# Fecha: 11/10/2011

import pygtk
pygtk.require('2.0')
import gtk
import Image

class Wizard(gtk.Window):
    __c_principal = gtk.Fixed() # Contenedor Principal
    btn_aplicar = gtk.Button()  # Botón Aplicar
    c_pasos = gtk.VBox()
    #pasos = {}                # Pasos
    pasos = []
    nombres = []
    contenidos = []
    __paso = ''                 # Paso actual
    __count = 0                 # Número de pasos
    def __init__(self, ancho, alto, titulo, banner, btn_apply):
        #Creo la ventana
        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        gtk.Window.set_position(self, gtk.WIN_POS_CENTER_ALWAYS)
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

        #Creo la linea divisoria
        self.linea = gtk.HSeparator()   
        self.linea.set_size_request(ancho, 5);
        self.__c_principal.put(self.linea, 0, (alto - 40))
        self.linea.show()
        #Creo la botonera
        #Anterior
        self.btn_anterior = gtk.Button(stock=gtk.STOCK_GO_BACK)
        self.__c_principal.put(self.btn_anterior, (ancho - 180), (alto - 30))
        self.btn_anterior.set_size_request(80, 30)
        #self.btn_anterior.connect("clicked", self.prev_step)
        self.btn_anterior.show()
        #Siguiente
        self.btn_siguiente = gtk.Button(stock=gtk.STOCK_GO_FORWARD)
        self.__c_principal.put(self.btn_siguiente, (ancho - 90), (alto - 30))
        self.btn_siguiente.set_size_request(80, 30)
        #self.btn_siguiente.connect("clicked", self.next_step)
        self.btn_siguiente.show()
        #Cancelar
        self.btn_cancelar = gtk.Button(stock=gtk.STOCK_CANCEL)
        self.__c_principal.put(self.btn_cancelar, 10, (alto - 30))
        self.btn_cancelar.set_size_request(80, 30)
        self.btn_cancelar.connect("clicked", self.close)
        self.btn_cancelar.show()
        #Aceptar
        self.btn_aplicar.set_label(btn_apply)
        self.__c_principal.put(self.btn_aplicar, (ancho - 90), (alto - 30))
        self.btn_aplicar.set_size_request(80, 30)

    #Método para cerrar la ventana
    def close(self, widget=None):
        self.destroy()
        gtk.main_quit()

    #Metodo para agregar nuevos pasos
    def agregar(self, nombre, paso):
        if self.indice(self.nombres, nombre) != -1: return
        self.nombres.append(nombre)
        self.pasos.append(paso)
        
    def mostrar(self, nombre):
        if self.__paso != '': 
            self.pasos[self.indice(self.nombres, self.__paso)].hide()
        if self.indice(self.contenidos, nombre) == -1:
            self.c_pasos.add(self.pasos[self.indice(self.nombres, nombre)])
            self.contenidos.append(nombre)
        self.pasos[self.indice(self.nombres, nombre)].show()
        self.__paso = nombre
        pass

    
    def indice(self, lista, valor):
        try:
            i = lista.index(valor)
        except ValueError:
            i = -1
        return i
