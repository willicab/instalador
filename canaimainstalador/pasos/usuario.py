#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import gtk

class PasoUsuario(gtk.Fixed):
    def __init__(self, CFG):
        gtk.Fixed.__init__(self)

        self.lbl1 = gtk.Label("Configuración de la cuenta de administrador")
        self.lbl1.set_size_request(690, 25)
        self.lbl1.set_alignment(0, 0)
        self.put(self.lbl1, 0, 0)

        self.lbl1 = gtk.Label("Escriba una contraseña")
        self.lbl1.set_size_request(690, 25)
        self.lbl1.set_alignment(0, 0)
        self.put(self.lbl1, 0, 25)

        self.lbl1 = gtk.Label("Repita la contraseña")
        self.lbl1.set_size_request(690, 25)
        self.lbl1.set_alignment(0, 0)
        self.put(self.lbl1, 0, 50)

        self.linea = gtk.HSeparator()
        self.linea.set_size_request(690, 10);
        self.put(self.linea, 0, 75)

        self.lbl1 = gtk.Label("Configuración de la cuenta de Usuario")
        self.lbl1.set_size_request(690, 25)
        self.lbl1.set_alignment(0, 0)
        self.put(self.lbl1, 0, 80)

        self.lbl1 = gtk.Label("Nombre Completo")
        self.lbl1.set_size_request(690, 25)
        self.lbl1.set_alignment(0, 0)
        self.put(self.lbl1, 0, 105)

        self.lbl1 = gtk.Label('Nombre de usuario')
        self.lbl1.set_size_request(690, 25)
        self.lbl1.set_alignment(0, 0)
        self.put(self.lbl1, 0, 130)

        self.lbl1 = gtk.Label("Escriba una contraseña")
        self.lbl1.set_size_request(690, 25)
        self.lbl1.set_alignment(0, 0)
        self.put(self.lbl1, 0, 155)

        self.lbl1 = gtk.Label("Repita la contraseña")
        self.lbl1.set_size_request(690, 25)
        self.lbl1.set_alignment(0, 0)
        self.put(self.lbl1, 0, 180)

        self.lbl1 = gtk.Label("Configuraciones avanzadas")
        self.lbl1.set_size_request(690, 25)
        self.put(self.lbl1, 0, 210)

        self.lbl1 = gtk.Label('Nombre de la máquina')
        self.lbl1.set_size_request(690, 25)
        self.lbl1.set_alignment(0, 0)
        self.put(self.lbl1, 0, 235)

        self.txt_passroot = gtk.Entry()
        self.txt_passroot.set_size_request(440, 25)
        self.txt_passroot.set_visibility(False)
        self.put(self.txt_passroot, 250, 25)

        self.txt_passroot2 = gtk.Entry()
        self.txt_passroot2.set_size_request(440, 25)
        self.txt_passroot2.set_visibility(False)
        self.put(self.txt_passroot2, 250, 50)

        self.txt_nombre = gtk.Entry()
        self.txt_nombre.set_size_request(440, 25)
        self.put(self.txt_nombre, 250, 105)

        self.txt_usuario = gtk.Entry()
        self.txt_usuario.set_size_request(440, 25)
        self.put(self.txt_usuario, 250, 130)

        self.txt_passuser = gtk.Entry()
        self.txt_passuser.set_size_request(440, 25)
        self.txt_passuser.set_visibility(False)
        self.put(self.txt_passuser, 250, 155)

        self.txt_passuser2 = gtk.Entry()
        self.txt_passuser2.set_size_request(440, 25)
        self.txt_passuser2.set_visibility(False)
        self.put(self.txt_passuser2, 250, 180)

        self.linea = gtk.HSeparator()
        self.linea.set_size_request(690, 10);
        self.put(self.linea, 0, 205)

        self.txt_maquina = gtk.Entry()
        self.txt_maquina.set_text('canaima-popular')
        self.txt_maquina.set_size_request(440, 25)
        self.txt_maquina.set_max_length(255)
        self.put(self.txt_maquina, 250, 235)

        self.chkoem = gtk.CheckButton("Instalación OEM (Ignora esta configuración y la realiza al primer inicio)")
        self.chkoem.connect("toggled", self.CheckButton_on_changed)
        self.chkoem.set_size_request(690, 25)
        self.put(self.chkoem, 0, 260)

    def CheckButton_on_changed(self, widget=None):
        active = not self.chkoem.get_active()
        self.txt_passroot.set_sensitive(active)
        self.txt_passroot2.set_sensitive(active)
        self.txt_nombre.set_sensitive(active)
        self.txt_usuario.set_sensitive(active)
        self.txt_passuser.set_sensitive(active)
        self.txt_passuser2.set_sensitive(active)
        self.txt_maquina.set_sensitive(active)
