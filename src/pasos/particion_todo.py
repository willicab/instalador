#-*- coding: UTF-8 -*-

import gtk
import clases.particiones
import clases.general as gen
import clases.barra_todo as barra
import clases.leyenda_todo as leyenda

class Main(gtk.Fixed):
    #root1 = '20GB'
    #root2 = '3GB'
    #usr = '18GB'
    #boot = '256MB'
    ini = ''
    fin = ''
    disco = ''
    swap = ''
    cfg = None
    part = clases.particiones.Main()
    
    def __init__(self, disco):
        gtk.Fixed.__init__(self)
        self.disco = disco
        self.set_limite()
        self.swap = gen.ram() if int(gen.ram()) >= 1048576 else int(gen.ram()) * 2
        self.ini = int(float(self.ini.replace(',', '.')))
        self.metodo = 'particion_1'
        cfg = (self.disco, self.ini, self.fin, self.swap, self.metodo)
        
        txt_info = "Seleccione tipo de instalación que desea realizar"
        self.lbl1 = gtk.Label(txt_info)
        self.lbl1.set_size_request(590, 20)
        self.lbl1.set_justify(gtk.JUSTIFY_CENTER)
        self.put(self.lbl1, 0, 0)
        self.lbl1.show()

        self.leyenda = leyenda.Main(self, 'particion_1')
        self.leyenda.set_size_request(20, 125)
        self.put(self.leyenda, 310, 90)
        self.leyenda.show()

        self.barra = barra.Main(cfg)
        self.barra.set_size_request(590, 60)
        self.barra.show()
        self.put(self.barra, 0, 25)

        # Opciones
        button = gtk.RadioButton(None, 
            "Realizar la instalación en una sola partición")
        button.connect("toggled", self.RadioButton_on_changed, "particion_1")
        button.set_size_request(300, 20)
        button.set_active(True)
        self.put(button, 0, 90)
        button.show()

        button = gtk.RadioButton(button, 
            "Separar la partición /home (Recomendado)")
        button.connect("toggled", self.RadioButton_on_changed, "particion_2")
        button.set_size_request(300, 20)
        self.put(button, 0, 110)
        button.show()

        button = gtk.RadioButton(button, 
            "Separar las particiones /home, /usr y /boot")
        button.connect("toggled", self.RadioButton_on_changed, "particion_3")
        button.set_size_request(300, 20)
        self.put(button, 0, 130)
        button.show()

        # Etiqueta Información Espacio Usado
        msg = 'Partición Swap'
        self.lbl_usado = gtk.Label('{0}'.format(msg))
        self.lbl_usado.set_size_request(590, 20)
        self.lbl_usado.set_alignment(0, 0)
        self.put(self.lbl_usado, 332, 90)
        self.lbl_usado.show()
        
        # Etiqueta Información Espacio Libre
        self.lbl_otra = gtk.Label('Partición Root')
        self.lbl_otra.set_size_request(590, 20)
        self.lbl_otra.set_alignment(0, 0)
        self.put(self.lbl_otra, 332, 115)
        self.lbl_otra.show()
        
        # Etiqueta Información Instalación canaima
        self.lbl_canaima = gtk.Label('Partición Home')
        self.lbl_canaima.set_size_request(590, 20)
        self.lbl_canaima.set_alignment(0, 0)
        self.put(self.lbl_canaima, 332, 140)
        self.lbl_canaima.show()

        # Etiqueta Información Espacio mínimo
        msg = 'Partición Usr'
        self.lbl_minimo = gtk.Label('{0}'.format(msg))
        self.lbl_minimo.set_size_request(590, 20)
        self.lbl_minimo.set_alignment(0, 0)
        self.put(self.lbl_minimo, 332, 165)
        self.lbl_minimo.show()

        # Etiqueta Información Espacio mínimo
        msg = 'Partición Boot'
        self.lbl_minimo = gtk.Label('{0}'.format(msg))
        self.lbl_minimo.set_size_request(590, 20)
        self.lbl_minimo.set_alignment(0, 0)
        self.put(self.lbl_minimo, 332, 190)
        self.lbl_minimo.show()
        
    def RadioButton_on_changed(self, widget, data=None):
        if widget.get_active() == True:
            self.metodo = data
            self.barra.cambiar(self.metodo)
            self.leyenda.cambiar(self.metodo)
        
    
    def set_limite(self):
        p = self.part.lista_particiones(self.disco)
        self.ini = float(p[0][1][:-2].replace(',', '.'))
        self.fin = float(p[0][2][:-2].replace(',', '.'))
        #print self.ini, self.fin
        for t in p:
            ini = float(t[1][:-2].replace(',', '.'))
            fin = float(t[2][:-2].replace(',', '.'))
            if self.ini > ini : self.ini = ini
            if self.fin < fin : self.fin = fin
        self.ini = str(self.ini)
        self.fin = str(self.fin)
        

