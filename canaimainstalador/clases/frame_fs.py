#-*- coding: UTF-8 -*-
'''
Created on 21/09/2012

@author: erick
'''
import gtk
from canaimainstalador.clases.common import is_extended, has_extended, TblCol
from canaimainstalador.translator import msj
from canaimainstalador.config import FSPROGS


class frame_fs(gtk.Table):
    '''
    Este marco será insertado tanto en la ventana de particiones nuevas como en
    la de usar particion existente, permite seleccionar el punto de montaje, el
    sistema de archivos e indicar si se formateará o no la particion
    '''

    def __init__(self, lista, part_act, parent_diag):
        '''
        Constructor
        '''
        gtk.Table.__init__(self, 6, 6)

        self.lista = lista
        self.part_act = part_act
        self.parent_diag = parent_diag

        #Tipo de partición
        self.lbl1 = gtk.Label('Tipo de partición')
        self.lbl1.set_alignment(0, 0.5)
        self.attach(self.lbl1, 0, 1, 0, 1)
        self.lbl1.show()

        self.cmb_tipo = gtk.combo_box_new_text()
        if is_extended(self.part_act):
            self.cmb_tipo.append_text(msj.particion.logica)
            self.cmb_tipo.set_sensitive(False)
        else:
            self.cmb_tipo.append_text(msj.particion.primaria)
            # Solo se permite una particion extendida en el disco
            if not has_extended(self.lista):
                self.cmb_tipo.append_text(msj.particion.extendida)
        self.cmb_tipo.set_active(0)
        self.attach(self.cmb_tipo, 1, 2, 0, 1)
        self.cmb_tipo.connect("changed", self.cmb_tipo_on_changed)
        self.cmb_tipo.show()

        #Sistema de Archivos
        self.lbl2 = gtk.Label('Sistema de Archivos')
        self.lbl2.set_alignment(0, 0.5)
        self.attach(self.lbl2, 0, 1, 1, 2)
        self.lbl2.show()


        self.cmb_fs = gtk.combo_box_new_text()
        self.cmb_fs_fill()
        self.cmb_fs.connect("changed", self.cmb_fs_on_changed)
        self.attach(self.cmb_fs, 1, 2, 1, 2)
        self.cmb_fs.show()

        # Punto de Montaje
        self.lbl3 = gtk.Label('Punto de Montaje')
        self.lbl3.set_alignment(0, 0.5)
        self.lbl3.set_size_request(200, 30)
        self.attach(self.lbl3, 0, 1, 2, 3)
        self.lbl3.show()

        self.cmb_montaje = gtk.combo_box_new_text()
        self.cmb_montaje_fill()
        self.attach(self.cmb_montaje, 1, 2, 2, 3)
        self.cmb_montaje.connect("changed", self.cmb_montaje_on_changed)
        self.cmb_montaje.show()

        self.entrada = gtk.Entry()
        self.entrada.set_text('/')
        self.attach(self.entrada, 1, 2, 2, 3)
        self.entrada.connect("changed", self.validar_punto)

        self.show()


    def cmb_tipo_on_changed(self, widget=None):
        tipo = widget.get_active_text()
        if tipo == 'Extendida':
            self.cmb_fs.set_sensitive(False)
            self.cmb_montaje.set_sensitive(False)
        else:
            self.cmb_fs.set_sensitive(True)
            self.cmb_montaje.set_sensitive(True)

    def cmb_fs_fill(self):
        fs_list = FSPROGS.keys()
        fs_list.sort()
        for fs in fs_list:
            self.cmb_fs.append_text(fs)
        self.cmb_fs.set_active(3)

    def cmb_fs_on_changed(self, widget=None):
        fs = widget.get_active_text()
        if fs == 'swap':
            self.cmb_montaje.set_sensitive(False)
        else:
            self.cmb_montaje.set_sensitive(True)

    def cmb_montaje_fill(self):
        self.cmb_montaje_add('/')
        self.cmb_montaje_add('/boot')
        self.cmb_montaje_add('/home')
        self.cmb_montaje_add('/opt')
        self.cmb_montaje_add('/srv')
        self.cmb_montaje_add('/tmp')
        self.cmb_montaje_add('/usr')
        self.cmb_montaje_add('/usr/local')
        self.cmb_montaje_add('/var')
        self.cmb_montaje_add('Ninguno')
        self.cmb_montaje_add('Escoger manualmente...')
        self.cmb_montaje.set_active(0)

    def cmb_montaje_add(self, point):
        '''Filtra los puntos de montaje que ya están siendo usados para no
        agregarlos a la lista del combobox'''
        data = self.lista
        appear = False
        for row in data:
            if row[TblCol.MONTAJE] == point:
                appear = True
        if not appear:
            self.cmb_montaje.append_text(point)

    def cmb_montaje_on_changed(self, widget=None):
        montaje = widget.get_active_text()
        if montaje == 'Escoger manualmente...':
            self.entrada.show()
            self.validar_punto()
        else:
            self.entrada.hide()
            self.set_response_sensitive(gtk.RESPONSE_OK, True)

    def validar_punto(self, widget=None):
        '''Valida que el punto de montaje no esté ya asignado a otra
        partición'''
        aparece = False
        for fila in self.lista:
            if fila[TblCol.MONTAJE] == widget.get_text().strip():
                aparece = True
        if aparece == False:
            self.parent_diag.set_response_sensitive(gtk.RESPONSE_OK, True)
        else:
            self.parent_diag.set_response_sensitive(gtk.RESPONSE_OK, False)

if __name__ == "__main__":
    lst = [
          ['/dev/sda1', 'Primaria', 'ext3', '', '31.28GB', '22.85GB', '8.43GB', 31.0, 32804729.0, False],
          ['', 'Primaria', 'Espacio Libre', '', '134.0KB', '0.0KB', '134.0KB', 32804730.0, 32804863.0, False],
          ['/dev/sda2', 'Primaria', 'swap', '', '1024.0MB', '1024.0MB', '0.0KB', 32804864.0, 33853439.0, False],
          ['/dev/sda3', 'Primaria', 'ext3', '', '42.24GB', '36.37GB', '5.86GB', 33853440.0, 78150655.0, False],
          ]

    pa = ['', 'Primaria', 'Espacio Libre', '', '31.28GB', '0.0KB', '31.28GB', 31, 32804863, False]

    w = gtk.Dialog()
    frame = frame_fs(lst, pa, w)
    w.vbox.pack_start(frame)
    w.show()
    gtk.main()
