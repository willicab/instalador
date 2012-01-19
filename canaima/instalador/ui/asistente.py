#!/usr/bin/python
# -*- coding: utf-8 -*-

''' Widget para el asistente de instalación de Canaima '''
# Autor: Wil Alvarez (aka satanas)
# Ene 18, 2012

import os
import gtk
import pygtk

pygtk.require('2.0')

from canaima.instalador.ui.teclado import Teclado
from canaima.instalador.ui.bienvenida import Bienvenida

class Asistente(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self)
        self.paso = 0
        
        # Imágenes
        img_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        img_icon= os.path.realpath(os.path.join(img_dir, 'canaima.png'))
        img_banner = os.path.realpath(os.path.join(img_dir, 'banner-app-top.png'))
        
        # Opciones de ventana
        self.set_title('Canaima Instalador')
        self.set_size_request(600, 450)
        self.set_border_width(0)
        self.set_resizable(False)
        self.set_icon(gtk.gdk.pixbuf_new_from_file(img_icon))
        self.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.connect('delete-event', self.__cerrar)
        
        pix = gtk.gdk.pixbuf_new_from_file(img_banner)
        banner = gtk.Image()
        banner.set_from_pixbuf(pix)
        del pix
        
        self.widget = None
        self.content = None
        self.container = gtk.VBox(False)
        
        self.btn_back = gtk.Button(stock=gtk.STOCK_GO_BACK)
        self.btn_back.connect('clicked', self.__anterior)
        self.btn_next = gtk.Button(stock=gtk.STOCK_GO_FORWARD)
        self.btn_next.connect('clicked', self.__siguiente)
        self.btn_cancel = gtk.Button(stock=gtk.STOCK_CANCEL)
        self.btn_cancel.connect('clicked', self.__cancelar)
        
        box_button = gtk.HButtonBox()
        box_button.set_spacing(6)
        box_button.set_border_width(10)
        box_button.set_layout(gtk.BUTTONBOX_END)
        box_button.pack_start(self.btn_cancel)
        box_button.pack_start(self.btn_back)
        box_button.pack_start(self.btn_next)
        
        vbox = gtk.VBox(False, 5)
        vbox.pack_start(banner, False, False)
        vbox.pack_start(self.container, True, True)
        vbox.pack_start(gtk.HSeparator(), False, False)
        vbox.pack_start(box_button, False, False)
        self.add(vbox)
        self.mostrar()
        
        try:
            self.show_all()
            gtk.main()
        except KeyboardInterrupt:
            self.__cerrar()
    
    def __cerrar(self, widget=None, event=None):
        gtk.main_quit()
        sys.exit(0)
    
    def __cancelar(self, widget):
        pass
    
    def __siguiente(self, widget):
        if self.paso == 1:
            self.mapa_teclado = self.widget.mapa_teclado()
        
        self.paso += 1
        self.mostrar()
    
    def __anterior(self, widget):
        self.paso -= 1
        if self.paso <= 0:
            self.paso = 0
        self.mostrar()
    
    def mostrar(self):
        if self.content is not None:
            self.container.remove(self.content)
        
        if self.paso == 0:
            vbox = Bienvenida()
            self.btn_back.set_sensitive(False)
        elif self.paso == 1:
            vbox = Teclado()
            self.btn_back.set_sensitive(True)
        
        self.content = gtk.VBox(False)
        self.content.pack_start(vbox, True, True)
        self.container.pack_start(self.content, True, True)
        self.show_all()
