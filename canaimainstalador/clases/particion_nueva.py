#-*- coding: UTF-8 -*-

import gtk

from canaimainstalador.clases.common import floatify, humanize, get_active_text, \
    TblCol
from canaimainstalador.translator import msj

class Main(gtk.Dialog):

    inicio = 0
    fin = 0

    def __init__(self, padre):
        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        gtk.Window.set_position(self, gtk.WIN_POS_CENTER_ALWAYS)

        self.padre = padre
        # Toma el inicio y fin de la particion seleccionada
        self.inicio = self.padre.fila_selec[TblCol.INICIO]
        self.fin = self.padre.fila_selec[TblCol.FIN]

        self.set_title("Nueva Partición")
        self.set_size_request(400, 200)
        self.set_resizable(0)

        self.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        self.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        self.set_default_response(gtk.RESPONSE_CANCEL)

        # Contenedor General
        self.cont = gtk.Fixed()
        self.cont.show()
        self.vbox.pack_start(self.cont)

        #Tamaño de la partición
        self.lbl = gtk.Label('Tamaño')
        self.lbl.set_alignment(0, 0.5)
        self.lbl.set_size_request(200, 30)
        self.lbl.show()
        self.cont.put(self.lbl, 5, 5)
        adj = gtk.Adjustment(float(self.fin),
                             float(self.inicio),
                             float(self.fin),
                             1.0,
                             5.0,
                             0.0)
        self.escala = gtk.HScale()
        self.escala.set_draw_value(False)
        self.escala.set_adjustment(adj)
        self.escala.set_property('value-pos', gtk.POS_RIGHT)
        self.escala.set_size_request(250, 30)
        self.escala.connect("value-changed", self.on_changed)
        self.cont.put(self.escala, 60, 5)
        self.escala.show()
        self.lblsize = gtk.Label(humanize(self.escala.get_value() - \
                                 float(self.inicio)))
        self.lblsize.set_alignment(0, 0.5)
        self.lblsize.set_size_request(100, 30)
        self.lblsize.show()
        self.cont.put(self.lblsize, 320, 5)

        #Tipo de partición
        self.lbl = gtk.Label('Tipo de partición')
        self.lbl.set_alignment(0, 0.5)
        self.lbl.set_size_request(200, 30)
        self.cont.put(self.lbl, 5, 35)
        self.lbl.show()

        self.cmb_tipo = gtk.combo_box_new_text()
        self.cmb_tipo.set_size_request(100, 30)
        self.cont.put(self.cmb_tipo, 145, 35)

        if self.padre.bext == True:
            self.cmb_tipo.append_text(msj.particion.logica)
            self.cmb_tipo.set_sensitive(False)
        else:
            self.cmb_tipo.append_text(msj.particion.primaria)
            # Solo se permite una particion extendida en el disco
            if not self.padre.existe_extendida():
                self.cmb_tipo.append_text(msj.particion.extendida)

        self.cmb_tipo.set_active(False)
        self.cmb_tipo.connect("changed", self.cmb_tipo_on_changed)
        self.cmb_tipo.show()

        #Sistema de Archivos
        self.lbl = gtk.Label('Sistema de Archivos')
        self.lbl.set_alignment(0, 0.5)
        self.lbl.set_size_request(200, 30)
        self.lbl.show()
        self.cont.put(self.lbl, 5, 65)
        self.cmb_fs = gtk.combo_box_new_text()
        self.cmb_fs.set_size_request(100, 30)
        self.cont.put(self.cmb_fs, 145, 65)
        self.cmb_fs.append_text('ext2')
        self.cmb_fs.append_text('ext3')
        self.cmb_fs.append_text('ext4')
        self.cmb_fs.append_text('fat16')
        self.cmb_fs.append_text('fat32')
        self.cmb_fs.append_text('linux-swap')
        self.cmb_fs.append_text('reiserfs')
        self.cmb_fs.append_text('xfs')
        self.cmb_fs.set_active(True)
        self.cmb_fs.connect("changed", self.cmb_fs_on_changed)
        self.cmb_fs.show()

        # Punto de Montaje
        self.lbl = gtk.Label('Punto de Montaje')
        self.lbl.set_alignment(0, 0.5)
        self.lbl.set_size_request(200, 30)
        self.cont.put(self.lbl, 5, 95)
        self.lbl.show()

        self.cmb_montaje = gtk.combo_box_new_text()
        self.cmb_montaje.set_size_request(200, 30)
        self.cont.put(self.cmb_montaje, 145, 95)
        self.agregar('/')
        self.agregar('/boot')
        self.agregar('/home')
        self.agregar('/opt')
        self.agregar('/srv')
        self.agregar('/tmp')
        self.agregar('/usr')
        self.agregar('/usr/local')
        self.agregar('/var')
        self.cmb_montaje.append_text('Ninguno')
        self.cmb_montaje.append_text('Escoger manualmente...')
        self.cmb_montaje.set_active(False)
        self.cmb_montaje.connect("changed", self.cmb_montaje_on_changed)
        self.cmb_montaje.show()

        self.entrada = gtk.Entry()
        self.entrada.set_text('/')
        self.entrada.set_size_request(200, 30)
        self.cont.put(self.entrada, 145, 125)
        self.entrada.connect("changed", self.validar_punto)

        response = self.run()
        self.procesar_respuesta(response)

    def procesar_respuesta(self, response=None):

        if not response:
            return response

        if response == gtk.RESPONSE_OK:
            tipo = get_active_text(self.cmb_tipo)
            formato = get_active_text(self.cmb_fs)
            montaje = get_active_text(self.cmb_montaje)

            if formato == 'linux-swap':
                montaje = ''

            if montaje == 'Escoger manualmente...':
                montaje = self.entrada.get_text().strip()

            # Calculo el tamaño
            inicio = int(self.inicio)
            fin = int(self.escala.get_value())
            tamano = humanize(fin - inicio)

            # Primaria
            if tipo == msj.particion.primaria:
                # Se crea elemento particion primaria y se agrega a la lista
                particion = [self.padre.disco, #Dispositivo
                             tipo, #Tipo
                             formato, #Formato
                             montaje, #Punto de montaje
                             tamano, #Tamaño
                             inicio, #inicio
                             fin]               #fin
                self.padre.agregar_a_lista(particion)

            # Extendida
            elif tipo == msj.particion.extendida:
                # Cambia variable bext a True
                self.padre.bext = True
                # Establece las variables ext_ini y ext_fin
                self.padre.ext_ini = inicio
                self.padre.ext_fin = fin

                # Se crea elemento particion extendida y se agrega a la lista
                particion = [self.padre.disco, #Dispositivo
                             tipo, #Tipo
                             '', #Formato
                             '', #Punto de montaje
                             tamano, #Tamaño
                             inicio, #inicio
                             fin]               #fin
                self.padre.agregar_a_lista(particion)
                # Se crea elemento espacio libre en partición extendida
                particion = ['', #Dispositivo
                             tipo, #Tipo
                             msj.particion.libre, #Formato
                             '', #Punto de montaje
                             tamano, #Tamaño
                             inicio, #inicio
                             fin]                                   #fin
                self.padre.agregar_a_lista(particion, False)

            # Lógica
            elif tipo == msj.particion.logica:
                # Se crea elemento particion lógica y se agrega a la lista
                particion = [self.padre.disco, #Dispositivo
                             tipo, #Tipo
                             formato, #Formato
                             montaje, #Punto de montaje
                             tamano, #Tamaño
                             inicio, #inicio
                             fin]               #fin
                self.padre.agregar_a_lista(particion)
                # Si se llega al final de la particion extendida
                if self.padre.ext_fin == fin:
                    # No se crea elemento espacio libre en partición extendida,
                    # solo cambia variable bext a False
                    self.padre.bext = False
                # Si no
                else:
                    # se calcula el tamaño de la partición libre
                    ext_ini = fin
                    ext_fin = self.padre.ext_fin
                    tamano = humanize(ext_fin - ext_ini)
                    self.padre.ext_ini = ext_ini
                    # Se crea elemento espacio libre en partición extendida
                    particion = ['', #Dispositivo
                                 msj.particion.extendida, #Tipo
                                 msj.particion.libre, #Formato
                                 '', #Punto de montaje
                                 tamano, #Tamaño
                                 ext_ini, #inicio
                                 ext_fin]                                   #fin
                    self.padre.agregar_a_lista(particion, False)

            # Calculamos el tamaño de la partición libre
            # si bext == True entonces se usará ext_fin como fin
            if self.padre.bext == True:
                fin = self.padre.ext_fin

            # Si fin != self.fin entonces 
            if fin != int(floatify(self.fin)):
                # Se calcula el tamaño de la partición libre
                inicio = fin
                fin = int(floatify(self.fin))
                tamano = humanize(fin - inicio)
                # Se crea elemento espacio libre
                libre = ['', #Dispositivo
                         '', #Tipo
                         msj.particion.libre, #Formato
                         '', #Punto de montaje
                         tamano, #Tamaño
                         inicio, #inicio
                         fin]               #fin
                self.padre.agregar_a_lista(libre, False)

            # Se actualiza la tabla
            self.padre.llenar_tabla()

        self.destroy()
        return response

    def on_changed(self, widget=None):
        self.lblsize.set_text(humanize(widget.get_value() - float(self.inicio)))

    def cmb_tipo_on_changed(self, widget=None):
        tipo = get_active_text(self.cmb_tipo)
        if tipo == 'Extendida':
            self.cmb_fs.set_sensitive(False)
            self.cmb_montaje.set_sensitive(False)
        else:
            self.cmb_fs.set_sensitive(True)
            self.cmb_montaje.set_sensitive(True)

    def cmb_fs_on_changed(self, widget=None):
        fs = get_active_text(self.cmb_fs)
        if fs == 'linux-swap':
            self.cmb_montaje.set_sensitive(False)
        else:
            self.cmb_montaje.set_sensitive(True)

    def cmb_montaje_on_changed(self, widget=None):
        montaje = get_active_text(self.cmb_montaje)
        if montaje == 'Escoger manualmente...':
            self.entrada.show()
            self.validar_punto()
        else:
            self.entrada.hide()
            self.set_response_sensitive(gtk.RESPONSE_OK, True)

    def agregar(self, punto):
        '''Filtra los puntos de montaje que ya están siendo usados para no
        agregarlos a la lista del combobox'''

        data = self.padre.lista
        assert isinstance(data, list) or isinstance(data, tuple)

        aparece = False
        for fila in data:
            if fila[TblCol.MONTAJE] == punto:
                aparece = True
        if aparece == False:
            self.cmb_montaje.append_text(punto)

    def validar_punto(self, widget=None):
        '''Valida que el punto de montaje no esté ya asignado a otra
        partición'''

        data = self.padre.lista
        aparece = False
        assert isinstance(data, list) or isinstance(data, tuple)
        for fila in data:
            if fila[TblCol.MONTAJE] == self.entrada.get_text().strip():
                aparece = True
        if aparece == False:
            self.set_response_sensitive(gtk.RESPONSE_OK, True)
        else:
            self.set_response_sensitive(gtk.RESPONSE_OK, False)
