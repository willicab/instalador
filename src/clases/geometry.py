#-*- coding: UTF-8 -*-

import pygtk
pygtk.require('2.0')
import gtk

class Main(gtk.Dialog): 
    inicio = 0
    fin = 0
    def __init__(self, padre, disco):
        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        gtk.Window.set_position(self, gtk.WIN_POS_CENTER_ALWAYS)
        self.set_title("")
        self.padre = padre
        self.disco = disco
        self.set_size_request(400, 200)
        self.set_resizable(0)
        self.set_border_width(0)
