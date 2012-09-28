#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import gtk

class PasoInfo(gtk.Fixed):
    def __init__(self, CFG):
        gtk.Fixed.__init__(self)

        msg_teclado = '● Se utilizará "{0}" como distribución de teclado.'.format(CFG['teclado'])
        msg_final = 'Presione el botón "Siguiente" para iniciar la instalación del sistema. Después de este paso no podrá detener la instalación, asegúrese de que sus datos son correctos.'

        if CFG['oem'] == False:
            msg_nombre = '● Su nombre completo ({0}) será utilizado para identificar su cuenta de usuario.'.format(CFG['nombre'])
            msg_usuario = '● Se creará una cuenta de usuario con nombre "{0}"'.format(CFG['usuario'])
            msg_maquina = '● Se utilizará "{0}" para identificar a su equipo en la red local.'.format(CFG['maquina'])
        else:
            msg_nombre = '● Se instalará en modo OEM, sus datos serán requeridos en el primer inicio de sesión.'
            msg_usuario = ''
            msg_maquina = ''

        if CFG['metodo']['tipo'] != 'MANUAL':
            if CFG['forma'] == 'ROOT:SWAP:LIBRE' or \
                CFG['forma'] == 'PART:ROOT:SWAP':
                msg_tipo = '● La instalación se realizará en una partición para el sistema y otra para el área de intercambio.'

            elif CFG['forma'] == 'ROOT:HOME:SWAP:LIBRE' or \
                CFG['forma'] == 'PART:ROOT:HOME:SWAP':
                msg_tipo = "Tipo de instalación: {0}".format("Separar la partición /home.")

            elif CFG['forma'] == 'BOOT:ROOT:HOME:SWAP:LIBRE' or \
                CFG['forma'] == 'PART:BOOT:ROOT:HOME:SWAP':
                msg_tipo = "Tipo de instalación: {0}".format("Separar las particiones /home y /boot.")

            elif CFG['forma'] == 'BOOT:ROOT:VAR:USR:HOME:SWAP:LIBRE' or \
                CFG['forma'] == 'PART:BOOT:ROOT:VAR:USR:HOME:SWAP':
                msg_tipo = "Tipo de instalación: {0}".format("Separar las particiones /home, /boot, /var y /usr.")

            elif CFG['forma'] == 'MANUAL':
                msg_tipo = "Distribución: {0}".format("Particionado manual.")

            else:
                msg_tipo = ''

        else:
            msg_tipo = ''

        if CFG['metodo']['tipo'] == 'MANUAL':
            msg_metodo = "Método: {0}"

        elif CFG['metodo']['tipo'] == 'TODO':
            msg_metodo = "Dispositivo a utilizar: {0}"

        elif CFG['metodo']['tipo'] == 'LIBRE':
            msg_metodo = "Dispositivo a utilizar: {0}"

        elif CFG['metodo']['tipo'] == 'REDIM':
            msg_metodo = "Dispositivo a utilizar: {0}"

        else:
            msg_metodo = ''

        self.lblusuario = gtk.Label(msg_usuario)
        self.lblusuario.set_size_request(640, 30)
        self.lblusuario.set_alignment(0, 0)
        self.put(self.lblusuario, 50, 150)

        self.lblnombre = gtk.Label(msg_nombre)
        self.lblnombre.set_size_request(640, 30)
        self.lblnombre.set_alignment(0, 0)
        self.put(self.lblnombre, 50, 170)

        self.lblteclado = gtk.Label(msg_teclado)
        self.lblteclado.set_size_request(640, 30)
        self.lblteclado.set_alignment(0, 0)
        self.put(self.lblteclado, 50, 190)

        self.lblmaquina = gtk.Label(msg_maquina)
        self.lblmaquina.set_size_request(640, 30)
        self.lblmaquina.set_alignment(0, 0)
        self.put(self.lblmaquina, 50, 210)

        self.lbltipo = gtk.Label(msg_tipo)
        self.lbltipo.set_size_request(690, 30)
        self.lbltipo.set_alignment(0, 0)
        self.put(self.lbltipo, 50, 230)

        self.lblmetodo = gtk.Label(msg_metodo)
        self.lblmetodo.set_size_request(640, 30)
        self.lblmetodo.set_alignment(0, 0)
        self.put(self.lblmetodo, 50, 250)

        self.lblmsg = gtk.Label(msg_final)
        self.lblmsg.set_size_request(640, 30)
        self.lblmsg.set_line_wrap(True)
        self.put(self.lblmsg, 50, 300)

