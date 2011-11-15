#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import pygtk
pygtk.require('2.0')
import gtk

class Ventana(gtk.Window):
  fixed = gtk.Fixed()
  banner = gtk.Image()
  linea = gtk.HSeparator()
  btn_anterior = gtk.Button(stock=gtk.STOCK_GO_BACK)
  btn_siguiente = gtk.Button(stock=gtk.STOCK_GO_FORWARD)
  btn_cancelar = gtk.Button(stock=gtk.STOCK_CANCEL)
  
  def __init__(self):
    gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
    gtk.Window.set_position(self, gtk.WIN_POS_CENTER_ALWAYS)
    self.set_title("Instalador Vivo Canaima")
    self.set_size_request(600, 400)
    self.set_resizable(0)
    self.set_border_width(0)


    #self.fixed = gtk.Fixed()
    self.add(self.fixed)
    self.fixed.show()

    #self.banner = gtk.Image()
    self.banner.set_from_file('/usr/share/canaima-estilo-visual/arte/banner-app-top.png')
    self.fixed.put(self.banner, 0, 0)
    self.banner.show()

    #self.linea = gtk.HSeparator()    
    self.linea.set_size_request(600, 5);
    self.fixed.put(self.linea, 0, 360)
    self.linea.show()
    
    #self.btn_siguiente = gtk.Button(stock=gtk.STOCK_GO_FORWARD)
    self.fixed.put(self.btn_siguiente, 510, 370)
    self.btn_siguiente.set_size_request(80, 30)
    self.btn_siguiente.show()

    #self.btn_cancelar = gtk.Button(stock=gtk.STOCK_CANCEL)
    self.fixed.put(self.btn_cancelar, 10, 370)
    self.btn_cancelar.set_size_request(80, 30)
    self.btn_cancelar.show()

    #self.btn_anterior = gtk.Button(stock=gtk.STOCK_GO_BACK)
    self.fixed.put(self.btn_anterior, 420, 370)
    self.btn_anterior.set_size_request(80, 30)
    #self.btn_anterior.set_sensitive(False)
    self.btn_anterior.show()

class Bienvenida:
  ventana = Ventana()
  contenedor = gtk.HBox()
  msg = "Bienvenido al asistente de instalación de Canaima GNU/Linux.\n\n" \
        "Este asistente le guiará por los pasos para instalar\n"\
        "Canaima GNU/Linux en tu equipo."
  def __init__(self):
    self.contenedor.set_size_request(580, 260)
    self.ventana.fixed.put(self.contenedor, 10, 90)
    
    self.lbl_info = gtk.Label(self.msg)
    self.lbl_info.set_justify(gtk.JUSTIFY_CENTER)
    #ventana.fixed.put(self.lbl_info, 5, 85)

    self.ventana.btn_anterior.set_sensitive(False)

    self.contenedor.add(self.lbl_info)
    
    self.ventana.connect("destroy", self.__close)
    self.ventana.btn_cancelar.connect("clicked", self.__close)
    self.ventana.btn_siguiente.connect("clicked", self.__siguiente)
    
    self.contenedor.show()
    self.lbl_info.show()
    self.ventana.show()
  
  def __close(self, widget=None):
    self.ventana.destroy()
    gtk.main_quit()

  def __siguiente(self, widget=None):
    print "Bienvenida"
    self.ventana.destroy()
    #self.contenedor.hide()
    Paso1()

class Paso1:
  ventana = Ventana()
  contenedor = gtk.Fixed()
  contenedor.show()
  msg = "<big>Paso 1.</big>"
  def __init__(self):
    self.contenedor.set_size_request(580, 260)
    self.ventana.fixed.put(self.contenedor, 10, 90)
    self.ventana.btn_siguiente.connect("clicked", self.__siguiente)
    
    self.cont_lbl = gtk.HBox()
    self.cont_lbl.set_size_request(580, 14)
    self.contenedor.put(self.cont_lbl, 0, 0)
    self.cont_lbl.show()
    
    self.lbl_paso1 = gtk.Label()
    self.lbl_paso1.set_justify(gtk.JUSTIFY_CENTER)
    self.lbl_paso1.set_use_markup(True)
    self.lbl_paso1.set_markup('<b><big>Paso 1.</big></b>')
    self.cont_lbl.add(self.lbl_paso1)
    self.lbl_paso1.show()
    
    self.ventana.show()

  def __siguiente(self, widget=None):
    print "paso 1"
    #self.contenedor.hide()
    #Paso1()

def main():
    # Enter the event loop
    gtk.main()
    return 0

if __name__ == "__main__":
    Bienvenida()
    main()
