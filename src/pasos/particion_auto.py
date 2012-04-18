#-*- coding: UTF-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
import commands
import clases.particiones
import clases.general as gen
import clases.barra_auto as widget
import clases.leyenda_auto as leyenda
#import mensaje

class Main(gtk.Fixed):
    # Valores para las particiones
    # swap = ''
    #root1 = '2GB'
    #root2 = '500MB'
    #boot = '512MB'
    #usr  = '1GB'
    #burning = None
    metodo = "particion_1"
    part = clases.particiones.Main()
    gen = clases.general
    particion = ''
    particiones = []
    libre = []
    minimo = '5GB'
    libre = '150MB'
    w = []
    cfg = {}
    def __init__(self, particion):
        gtk.Fixed.__init__(self)

        self.particion = particion
        self.disco = particion[:-1]
        self.num = particion[-1:]

        self.cfg['particion'] = particion
        self.cfg['disco'] = self.disco
        self.cfg['num'] = self.num

        p = self.part.lista_particiones(self.disco, self.particion)[0]
        self.particiones = self.part.lista_particiones(self.disco)
        self.ini = p[1]
        self.fin = p[2]
        self.fs = p[5]
        self.cfg['ini'] = self.ini
        self.cfg['fin'] = self.fin

        txt_info = "Seleccione el tamaño que desea usar para la instalación"
        self.lbl1 = gtk.Label(txt_info)
        self.lbl1.set_size_request(590, 20)
        self.lbl1.set_justify(gtk.JUSTIFY_CENTER)
        self.put(self.lbl1, 0, 0)
        self.lbl1.show()
        
        # Barra
        total = int(p[3][:-2])
        usado = gen.kb(p[7])
        minimo = gen.kb(self.minimo)
        libre = gen.kb(self.libre)
        self.swap = self.hay_swap()

        self.cur_value = ((total - minimo) - usado) / 2
        self.barra = widget.Barra(self, total, usado, libre, minimo, particion, self.swap)
        self.barra.set_size_request(590, 60)
        self.barra.show()
        self.put(self.barra, 0, 25)

        self.leyenda = leyenda.Main(self)
        self.leyenda.set_size_request(20, 100)
        self.put(self.leyenda, 0, 90)
        self.leyenda.show()

        # Etiqueta Información Espacio Usado
        msg = 'Espacio Usado en la partición'
        self.lbl_usado = gtk.Label('{0} ({1})'.format(msg, gen.hum(usado)))
        self.lbl_usado.set_size_request(590, 20)
        self.lbl_usado.set_alignment(0, 0)
        self.put(self.lbl_usado, 22, 90)
        self.lbl_usado.show()
        
        # Etiqueta Información Espacio Libre
        self.lbl_otra = gtk.Label('')
        self.lbl_otra.set_size_request(590, 20)
        self.lbl_otra.set_alignment(0, 0)
        self.put(self.lbl_otra, 22, 115)
        self.lbl_otra.show()
        
        # Etiqueta Información Instalación canaima
        self.lbl_canaima = gtk.Label('')
        self.lbl_canaima.set_size_request(590, 20)
        self.lbl_canaima.set_alignment(0, 0)
        self.put(self.lbl_canaima, 22, 140)
        self.lbl_canaima.show()

        # Etiqueta Información Espacio mínimo
        msg = 'Espacio mínimo requerido para instalar Canaima GNU/Linux'
        self.lbl_minimo = gtk.Label('{0} ({1})'.format(msg, gen.hum(self.minimo)))
        self.lbl_minimo.set_size_request(590, 20)
        self.lbl_minimo.set_alignment(0, 0)
        self.put(self.lbl_minimo, 22, 165)
        self.lbl_minimo.show()

        # Opciones
        button = gtk.RadioButton(None, 
            "Realizar la instalación en una sola partición")
        button.connect("toggled", self.RadioButton_on_changed, "particion_1")
        button.set_size_request(590, 20)
        button.set_active(True)
        self.put(button, 0, 190)
        button.show()

        button = gtk.RadioButton(button, 
            "Separar la partición /home (Recomendado)")
        button.connect("toggled", self.RadioButton_on_changed, "particion_2")
        button.set_size_request(590, 20)
        self.put(button, 0, 210)
        button.show()

        button = gtk.RadioButton(button, 
            "Separar las particiones /home, /usr y /boot")
        button.connect("toggled", self.RadioButton_on_changed, "particion_3")
        button.set_size_request(590, 20)
        self.put(button, 0, 230)
        button.show()

        button = gtk.RadioButton(button, 
            "Particionar Manualmente")
        button.connect("toggled", self.RadioButton_on_changed, "particion_4")
        button.set_size_request(590, 20)
        self.put(button, 0, 250)
        button.show()
        
        if self.swap != False:
            # Etiqueta Información Swap
            msg = 'Se usará la partición Swap Existente'
            self.lbl_usado = gtk.Label('{0}'.format(msg))
            self.lbl_usado.set_size_request(590, 20)
            self.lbl_usado.set_alignment(1, 0)
            self.put(self.lbl_usado, 0, 265)
            self.lbl_usado.show()

    def RadioButton_on_changed(self, widget, data=None):
        if widget.get_active() == True:
            self.cfg['metodo'] = data
            self.metodo = data
            
    def on_changed(self, widget=None):
        self.cur_value = int(self.barra.cur) #widget.get_value()
        if self.barra != None : self.barra.queue_draw()
        #print 'Changed: ', self.cur_value, gen.hum(self.cur_value)
        
    def get_cur_value(self):
        return self.cur_value
        
    def hay_swap(self):
        for p in self.particiones:
            if p[5].find('swap') != -1 : return True
        return False
        

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
