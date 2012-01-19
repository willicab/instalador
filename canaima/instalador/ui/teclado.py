#-*- coding: UTF-8 -*-

''' Configuración de la distribución del teclado '''
# Autor: William Cabrera, Wil Alvarez
# Fecha: 19/01/2012

import os
import gtk
import pango

from canaima.instalador.lib.distribuciones import DISTRIBUCIONES

TITULO = "Escoge la configuración del teclado:"
IMG_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

class Teclado(gtk.VBox):
    def __init__(self):
        gtk.VBox.__init__(self, False)
        
        title = gtk.Label(TITULO)
        title_align = gtk.Alignment(xalign=0)
        title_align.add(title)
        
        liststore = gtk.ListStore(str, str) # id, tipo
        for key, value in DISTRIBUCIONES.iteritems():
            liststore.append([key, value])
        
        self.treeview = gtk.TreeView(liststore)
        self.treeview.set_headers_visible(False)
        cell = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Distribuciones')
        column.pack_start(cell, True)
        column.add_attribute(cell, 'text', 1)
        self.treeview.append_column(column)
        
        scrollwin = gtk.ScrolledWindow()
        scrollwin.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        scrollwin.set_shadow_type(gtk.SHADOW_OUT)
        scrollwin.add(self.treeview)
        
        dists = gtk.HBox(False)
        dists.pack_start(scrollwin)
        
        label = gtk.Label("Escriba para probar la configuración")
        txt_prueba = gtk.Entry()
        
        self.pack_start(title_align, False, False, 5)
        self.pack_start(dists, True, True)
        self.pack_start(label, False, False)
        self.pack_start(txt_prueba, False, False)
        self.set_border_width(10)
        
        self.treeview.connect("cursor-changed", self.__seleccionar)
    
    def __seleccionar(self, widget):
        model, row = widget.get_selection().get_selected()
        if (row is None):
            return False
        
        key = model.get_value(row, 0)
        
        cmd = 'gconftool-2 -s /desktop/gnome/peripherals/keyboard/kbd/layouts '
        cmd += '-t list --list-type=string [{0}]'.format(key)
        print cmd
        #os.system('{0}'.format(cmd))
        img_keymap= os.path.realpath(os.path.join(IMG_DIR, key + '.png'))
        #self.img_distribucion.set_from_file(path)
    
    def mapa_teclado(self):
        model, row = self.treeview.get_selection().get_selected()
        return model.get_value(row, 0)
