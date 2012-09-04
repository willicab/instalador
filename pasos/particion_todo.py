#-*- coding: UTF-8 -*-

import gtk
import clases.particiones
import clases.general as gen
import clases.barra_todo as barra
import clases.leyenda_todo as leyenda

class Main(gtk.Fixed):
    ini = ''
    fin = ''
    disco = ''
    swap = ''
    cfg = None
    part = clases.particiones.Main()
    barra = None
    button = None

    def __init__(self, disco, ini=0, fin=0):
        gtk.Fixed.__init__(self)
        self.disco = disco

        if ini == 0 and fin == 0:
            self.set_limite()
        else:
            self.ini = ini
            self.fin = fin

        self.swap = gen.ram() if int(gen.ram()) >= 1048576 else int(gen.ram()) * 2
        self.ini = int(float(str(self.ini).replace(',', '.')))
        self.fin = int(float(str(self.fin).replace(',', '.')))
        self.metodo = 'particion_2'
        self.conf = (self.disco, self.ini, self.fin, self.swap, self.metodo)

        txt_info = "Seleccione tipo de instalación que desea realizar"
        self.lbl1 = gtk.Label(txt_info)
        self.lbl1.set_size_request(690, 20)
        self.lbl1.set_justify(gtk.JUSTIFY_CENTER)
        self.put(self.lbl1, 0, 0)

        self.barra = None
        self.barra = barra.Main(self.conf)
        self.barra.set_size_request(690, 100)
        self.put(self.barra, 0, 30)

        # Opciones
        msg_1 = "Instalar todo en una sola partición."
        self.option_1 = gtk.RadioButton(None, msg_1)
        self.option_1.connect("toggled", self.change_option, "particion_1")
        self.option_1.set_size_request(350, 20)
        self.put(self.option_1, 0, 140)

        msg_2 = "Separar la partición /home (Recomendado)."
        self.option_2 = gtk.RadioButton(self.option_1, msg_2)
        self.option_2.set_active(True)
        self.option_2.connect("toggled", self.change_option, "particion_2")
        self.option_2.set_size_request(350, 20)
        self.put(self.option_2, 0, 165)

        msg_3 = "Separar las particiones /home, /usr y /boot."
        self.option_3 = gtk.RadioButton(self.option_1, msg_3)
        self.option_3.connect("toggled", self.change_option, "particion_3")
        self.option_3.set_size_request(350, 20)
        self.put(self.option_3, 0, 190)

        msg_4 = "Particionar manualmente."
        self.option_4 = gtk.RadioButton(self.option_1, msg_4)
        self.option_4.connect("toggled", self.change_option, "particion_4")
        self.option_4.set_size_request(350, 20)
        self.put(self.option_4, 0, 215)

        self.leyenda = leyenda.Main(self, 'particion_1')
        self.leyenda.set_size_request(20, 125)
        self.put(self.leyenda, 390, 140)

        # Etiqueta partición swap
        self.lbl_swap = gtk.Label('Espacio de intercambio (swap)')
        self.lbl_swap.set_size_request(270, 20)
        self.lbl_swap.set_alignment(0, 0)
        self.put(self.lbl_swap, 420, 140)
        
        # Etiqueta partición root
        self.lbl_root = gtk.Label('Espacio de administrador (/root)')
        self.lbl_root.set_size_request(270, 20)
        self.lbl_root.set_alignment(0, 0)
        self.put(self.lbl_root, 420, 165)

        # Etiqueta partición home
        self.lbl_home = gtk.Label('Espacio de usuarios (/home)')
        self.lbl_home.set_size_request(270, 20)
        self.lbl_home.set_alignment(0, 0)
        self.put(self.lbl_home, 420, 190)

        # Etiqueta partición usr
        self.lbl_usr = gtk.Label('Espacio de aplicaciones (/usr)')
        self.lbl_usr.set_size_request(270, 20)
        self.lbl_usr.set_alignment(0, 0)
        self.put(self.lbl_usr, 420, 215)

        # Etiqueta partición boot
        self.lbl_boot = gtk.Label('Espacio de arranque (/boot)')
        self.lbl_boot.set_size_request(270, 20)
        self.lbl_boot.set_alignment(0, 0)
        self.put(self.lbl_boot, 420, 240)

        self.show_all()

    def change_option(self, widget, data=None):
        if widget.get_active() == True:
            self.metodo = data
            self.barra.cambiar(self.metodo)
            self.leyenda.cambiar(self.metodo)

    def set_limite(self):
        p = self.part.lista_particiones(self.disco)
        self.ini = float(p[0][1][:-2].replace(',', '.'))
        self.fin = float(p[0][2][:-2].replace(',', '.'))
        for t in p:
            ini = float(t[1][:-2].replace(',', '.'))
            fin = float(t[2][:-2].replace(',', '.'))
            if self.ini > ini : self.ini = ini
            if self.fin < fin : self.fin = fin
        self.ini = str(self.ini)
        self.fin = str(self.fin)

