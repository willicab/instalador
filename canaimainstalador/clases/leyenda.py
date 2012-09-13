#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import gtk, cairo, gobject

from canaimainstalador.clases.common import humanize

class Leyenda(gtk.Fixed):
    def __init__(self, parent):
        gtk.Fixed.__init__(self)
        self.p = parent
        self.forma = self.p.forma

        label = ''
        self.lbl_1 = gtk.Label(label)
        self.lbl_1.set_size_request(270, 20)
        self.lbl_1.set_alignment(0, 0)
        self.put(self.lbl_1, 0, 0)

        self.lbl_2 = gtk.Label(label)
        self.lbl_2.set_size_request(270, 20)
        self.lbl_2.set_alignment(0, 0)
        self.put(self.lbl_2, 0, 25)

        self.lbl_3 = gtk.Label(label)
        self.lbl_3.set_size_request(270, 20)
        self.lbl_3.set_alignment(0, 0)
        self.put(self.lbl_3, 0, 50)

        self.lbl_4 = gtk.Label(label)
        self.lbl_4.set_size_request(270, 20)
        self.lbl_4.set_alignment(0, 0)
        self.put(self.lbl_4, 0, 75)

        self.lbl_5 = gtk.Label(label)
        self.lbl_5.set_size_request(270, 20)
        self.lbl_5.set_alignment(0, 0)
        self.put(self.lbl_5, 0, 100)

        self.lbl_6 = gtk.Label(label)
        self.lbl_6.set_size_request(270, 20)
        self.lbl_6.set_alignment(0, 0)
        self.put(self.lbl_6, 0, 125)

        self.lbl_7 = gtk.Label(label)
        self.lbl_7.set_size_request(270, 20)
        self.lbl_7.set_alignment(0, 0)
        self.put(self.lbl_7, 0, 150)

        self.show_all()

    def cambiar(self, forma):
        self.forma = forma
        self.expose()

    def expose(self, widget=None, event=None):
        render = self.p.render
        j = 1

        self.lbl_1.set_text('')
        self.lbl_2.set_text('')
        self.lbl_3.set_text('')
        self.lbl_4.set_text('')
        self.lbl_5.set_text('')
        self.lbl_6.set_text('')
        self.lbl_7.set_text('')

        for i in render:
            part = i.split(':')[0]
            size = humanize(i.split(':')[1])

            if part == 'ROOT':
                exec "self.lbl_"+str(j)+".set_text('Espacio principal (/): '+size)"
            elif part == 'SWAP':
                exec "self.lbl_"+str(j)+".set_text('Espacio de intercambio (swap): '+size)"
            elif part == 'HOME':
                exec "self.lbl_"+str(j)+".set_text('Espacio de usuarios (/home): '+size)"
            elif part == 'USR':
                exec "self.lbl_"+str(j)+".set_text('Espacio de aplicaciones (/usr): '+size)"
            elif part == 'BOOT':
                exec "self.lbl_"+str(j)+".set_text('Espacio de arranque (/boot): '+size)"
            elif part == 'VAR':
                exec "self.lbl_"+str(j)+".set_text('Espacio de variables (/var): '+size)"
            elif part == 'LIBRE':
                exec "self.lbl_"+str(j)+".set_text('Espacio Libre: '+size)"
            elif part == 'PART':
                exec "self.lbl_"+str(j)+".set_text('Partición redimensionada: '+size)"

            j += 1

