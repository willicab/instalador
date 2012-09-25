#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import gtk

class PasoInfo(gtk.Fixed):
    def __init__(self, CFG):
        gtk.Fixed.__init__(self)
        self.cfg = CFG

        altura = 260
        inc = 20

        msg = "Distribución del Teclado: {0}".format(self.cfg['teclado'])
        self.lbldist = gtk.Label(msg)
        self.lbldist.set_size_request(690, 30)
        self.lbldist.set_alignment(0, 0)
        self.put(self.lbldist, 0, altura)
        altura = altura - inc

        msg = "Tipo de instalación: "
        if self.cfg['forma'] == 'ROOT:SWAP':
            msg = msg + "Realizar la instalación en una sola partición."
        elif self.cfg['forma'] == 'ROOT:HOME:SWAP':
            msg = msg + "Separar la partición /home."
        elif self.cfg['forma'] == 'BOOT:ROOT:HOME:SWAP':
            msg = msg + "Separar la partición /home y /boot."
        elif self.cfg['forma'] == 'BOOT:ROOT:VAR:USR:HOME:SWAP':
            msg = msg + "Separar las particiones /home, /usr, /var y /boot."
        elif self.cfg['forma'] == 'MANUAL':
            msg = msg + "Particionado manual"

        self.lbltipo = gtk.Label(msg)
        self.lbltipo.set_size_request(690, 30)
        self.lbltipo.set_alignment(0, 0)
        self.put(self.lbltipo, 0, altura)
        altura = altura - inc

        if self.cfg['metodo'] == 'MANUAL':
            msg = "Dispositivo a usar: {0}".format(self.cfg['disco'])
            self.lblmetodo = gtk.Label(msg)
            self.lblmetodo.set_size_request(690, 30)
            self.lblmetodo.set_alignment(0, 0)
            self.put(self.lblmetodo, 0, altura)
            altura = altura - inc

        elif self.cfg['metodo'] == 'TODO':
            msg = "Dispositivo a usar: {0}".format(self.cfg['disco'])
            self.lblmetodo = gtk.Label(msg)
            self.lblmetodo.set_size_request(690, 30)
            self.lblmetodo.set_alignment(0, 0)
            self.put(self.lblmetodo, 0, altura)
            altura = altura - inc

        elif self.cfg['metodo'] == 'LIBRE':
            msg = "Dispositivo a usar: {0}".format(self.cfg['disco'])
            self.lblmetodo = gtk.Label(msg)
            self.lblmetodo.set_size_request(690, 30)
            self.lblmetodo.set_alignment(0, 0)
            self.put(self.lblmetodo, 0, altura)
            altura = altura - inc

        elif self.cfg['metodo'] == 'REDIM':
            msg = "Dispositivo a usar: {0}".format(self.cfg['disco'])
            self.lblmetodo = gtk.Label(msg)
            self.lblmetodo.set_size_request(690, 30)
            self.lblmetodo.set_alignment(0, 0)
            self.put(self.lblmetodo, 0, altura)
            altura = altura - inc

        else:
            pass

#        if self.cfg['metodo'] == 'todo':
#            msg = "Dispositivo a usar: {0}".format(self.cfg['disco'])
#            self.lblmetodo = gtk.Label(msg)
#            self.lblmetodo.set_size_request(690, 30)
#            self.lblmetodo.set_alignment(0, 0)
#            self.put(self.lblmetodo, 0, altura)
#            altura = altura - inc
#        elif self.cfg['metodo'] == 'vacio':
#            pass
#        else:
#            msg = "partición a usar: {0}".format(self.cfg['particion'])
#            self.lblparticion = gtk.Label(msg)
#            self.lblparticion.set_size_request(590, 30)
#            self.put(self.lblparticion, 0, altura)
#            self.lblparticion.set_alignment(0, 0)
#            self.lblparticion.show()
#            altura = altura - inc

#            msg = "Tamaño Anterior de la Partición: {0}".format(gen.hum(gen.h2kb(self.cfg['fin'])))
#            self.lbltam = gtk.Label(msg)
#            self.lbltam.set_size_request(590, 30)
#            self.put(self.lbltam, 0, altura)
#            self.lbltam.set_alignment(0, 0)
#            self.lbltam.show()
#            altura = altura - inc

#            msg = "Nuevo Tamaño de la Partición: {0}".format(gen.hum(gen.h2kb(self.cfg['nuevo_fin'])))
#            self.lblnuevo = gtk.Label(msg)
#            self.lblnuevo.set_size_request(590, 30)
#            self.put(self.lblnuevo, 0, altura)
#            self.lblnuevo.set_alignment(0, 0)
#            self.lblnuevo.show()
#            altura = altura - inc

        msg = "Nombre completo del usuario: {0}".format(self.cfg['nombre'])
        self.lblnombre = gtk.Label(msg)
        self.lblnombre.set_size_request(690, 30)
        self.lblnombre.set_alignment(0, 0)
        self.put(self.lblnombre, 0, altura)
        altura = altura - inc

        msg = "Nombre de usuario: {0}".format(self.cfg['usuario'])
        self.lblusuario = gtk.Label(msg)
        self.lblusuario.set_size_request(690, 30)
        self.lblusuario.set_alignment(0, 0)
        self.put(self.lblusuario, 0, altura)
        altura = altura - inc

        msg = "Nombre de la maquina: {0}".format(self.cfg['maquina'])
        self.lblmaquina = gtk.Label(msg)
        self.lblmaquina.set_size_request(690, 30)
        self.lblmaquina.set_alignment(0, 0)
        self.put(self.lblmaquina, 0, altura)
        altura = altura - inc

        self.linea = gtk.HSeparator()
        self.linea.set_size_request(690, 10);
        self.put(self.linea, 0, altura)
        altura = altura - inc

        msg = 'Confirme que todos los datos son correctos, al hacer click en siguiente comenzará la instalación y ya no podrá dar marcha atrás.'
        self.lblmsg = gtk.Label(msg)
        self.lblmsg.set_size_request(690, (260 - altura))
        self.put(self.lblmsg, 0, 0)

