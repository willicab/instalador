#-*- coding: UTF-8 -*-

import gtk
import clases.general as gen

class Main(gtk.Fixed):
    def __init__(self, cfg):
        gtk.Fixed.__init__(self)

        print cfg
        altura = 260
        inc = 20 
        
        msg = "Distribución del Teclado: {0}".format(cfg['teclado'])
        self.lbl1 = gtk.Label(msg)
        self.lbl1.set_size_request(590, 30)
        self.put(self.lbl1, 0, altura)
        self.lbl1.set_alignment(0, 0)
        self.lbl1.show()
        altura = altura - inc

        msg = "Tipo de instalación: "
        if cfg['tipo'] == 'particion_1':
            msg = msg + "Realizar la instalación en una sola partición"
        elif cfg['tipo'] == 'particion_2':
            msg = msg + "Separar la partición /home"
        elif cfg['tipo'] == 'particion_3':
            msg = msg + "Separar las particiones /home, /usr y /boot"
        self.lbl1 = gtk.Label(msg)
        self.lbl1.set_size_request(590, 30)
        self.put(self.lbl1, 0, altura)
        self.lbl1.set_alignment(0, 0)
        self.lbl1.show()
        altura = altura - inc

        if cfg['metodo'] == 'todo':
            msg = "Dispositivo a usar: {0}".format(cfg['disco'])
            self.lbl1 = gtk.Label(msg)
            self.lbl1.set_size_request(590, 30)
            self.put(self.lbl1, 0, altura)
            self.lbl1.set_alignment(0, 0)
            self.lbl1.show()
            altura = altura - inc
        elif cfg['metodo'] == 'vacio':
            pass
        else:
            msg = "partición a usar: {0}".format(cfg['particion'])
            self.lbl1 = gtk.Label(msg)
            self.lbl1.set_size_request(590, 30)
            self.put(self.lbl1, 0, altura)
            self.lbl1.set_alignment(0, 0)
            self.lbl1.show()
            altura = altura - inc

            msg = "Tamaño Anterior de la Partición: {0}".format(gen.hum(gen.h2kb(cfg['fin'])))
            self.lbl1 = gtk.Label(msg)
            self.lbl1.set_size_request(590, 30)
            self.put(self.lbl1, 0, altura)
            self.lbl1.set_alignment(0, 0)
            self.lbl1.show()
            altura = altura - inc

            msg = "Nuevo Tamaño de la Partición: {0}".format(gen.hum(gen.h2kb(cfg['nuevo_fin'])))
            self.lbl1 = gtk.Label(msg)
            self.lbl1.set_size_request(590, 30)
            self.put(self.lbl1, 0, altura)
            self.lbl1.set_alignment(0, 0)
            self.lbl1.show()
            altura = altura - inc

        msg = "Nombre completo del usuario: {0}".format(cfg['nombre'])
        self.lbl1 = gtk.Label(msg)
        self.lbl1.set_size_request(590, 30)
        self.put(self.lbl1, 0, altura)
        self.lbl1.set_alignment(0, 0)
        self.lbl1.show()
        altura = altura - inc
        
        msg = "Nombre de usuario: {0}".format(cfg['usuario'])
        self.lbl1 = gtk.Label(msg)
        self.lbl1.set_size_request(590, 30)
        self.put(self.lbl1, 0, altura)
        self.lbl1.set_alignment(0, 0)
        self.lbl1.show()
        altura = altura - inc
        
        msg = "Nombre de la maquina: {0}".format(cfg['maquina'])
        self.lbl1 = gtk.Label(msg)
        self.lbl1.set_size_request(590, 30)
        self.put(self.lbl1, 0, altura)
        self.lbl1.set_alignment(0, 0)
        self.lbl1.show()
        altura = altura - inc
        
        self.linea = gtk.HSeparator()   
        self.linea.set_size_request(590, 10);
        self.put(self.linea, 0, altura)
        self.linea.show()
        altura = altura - inc

        msg = 'Confirme que todos los datos son correctos, al hacer click en '
        msg = msg + 'siguiente comenzará la\ninstalación y ya no podrá dar '
        msg = msg + 'marcha atrás.'
        self.lbl1 = gtk.Label(msg)
        self.lbl1.set_size_request(590, (260 - altura))
        self.put(self.lbl1, 0, 0)
        #self.lbl1.set_alignment(0, 0)
        self.lbl1.show()

