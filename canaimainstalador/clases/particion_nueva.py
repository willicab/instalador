#-*- coding: UTF-8 -*-

import gtk

from canaimainstalador.clases.common import humanize, TblCol, get_next_row, \
    get_row_index, is_extended, has_extended, set_partition
from canaimainstalador.translator import msj

class Main(gtk.Dialog):

    inicio_part = 0
    fin_part = 0

    def __init__(self, padre):
        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        gtk.Window.set_position(self, gtk.WIN_POS_CENTER_ALWAYS)
        self.disco = padre.disco
        self.lista = padre.lista
        self.acciones = padre.acciones
        self.particion_act = padre.fila_selec
        # Toma el inicio_part y fin_part de la particion seleccionada
        self.inicio_part = self.particion_act[TblCol.INICIO]
        self.fin_part = self.particion_act[TblCol.FIN]
        self.num_fila_act = get_row_index(self.lista, self.particion_act)
        self.particion_sig = get_next_row(self.lista, self.particion_act,
                                          self.num_fila_act)

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
        adj = gtk.Adjustment(self.fin_part,
                             self.inicio_part,
                             self.fin_part,
                             1.0,
                             5.0,
                             0.0)
        self.escala = gtk.HScale()
        self.escala.set_digits(0)
        self.escala.set_draw_value(False)
        self.escala.set_adjustment(adj)
        self.escala.set_property('value-pos', gtk.POS_RIGHT)
        self.escala.set_size_request(250, 30)
        self.escala.connect("value-changed", self.on_changed)
        self.cont.put(self.escala, 60, 5)
        self.escala.show()
        self.lblsize = gtk.Label(humanize(self.escala.get_value() - \
                                          self.inicio_part))
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

        if is_extended(self.particion_act):
            self.cmb_tipo.append_text(msj.particion.logica)
            self.cmb_tipo.set_sensitive(False)
        else:
            self.cmb_tipo.append_text(msj.particion.primaria)
            # Solo se permite una particion extendida en el disco
            if not has_extended(self.lista):
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
        self.agregar_p_montaje('/')
        self.agregar_p_montaje('/boot')
        self.agregar_p_montaje('/home')
        self.agregar_p_montaje('/opt')
        self.agregar_p_montaje('/srv')
        self.agregar_p_montaje('/tmp')
        self.agregar_p_montaje('/usr')
        self.agregar_p_montaje('/usr/local')
        self.agregar_p_montaje('/var')
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
            tipo = self.cmb_tipo.get_active_text()
            formato = self.cmb_fs.get_active_text()
            montaje = self.cmb_montaje.get_active_text()
            usado = humanize(0)

            if formato == 'linux-swap':
                montaje = ''

            if montaje == 'Escoger manualmente...':
                montaje = self.entrada.get_text().strip()

            # Calculo el tamaño
            inicio = self.inicio_part
            fin = self.escala.get_value()
            tamano = humanize(fin - inicio)
            libre = tamano

            print "---NUEVA----"
            # Primaria
            if tipo == msj.particion.primaria:
                print "Partición primaria"
                self.crear_particion(tipo, formato, montaje, tamano, usado, \
                                     libre, inicio, fin)
                if fin != self.fin_part:
                    print "Que deja espacio libre"
                    inicio = self.escala.get_value()
                    fin = self.fin_part
                    tamano = humanize(fin - inicio)
                    libre = tamano
                    self.crear_particion(tipo, msj.particion.libre, montaje, \
                                         tamano, usado, libre, inicio + 1, fin)
            # Extendida
            elif tipo == msj.particion.extendida:
                print "Partición Extendida"
                usado = tamano
                libre = humanize(0)
                self.crear_particion(tipo, formato, montaje, tamano, usado, \
                                     libre, inicio, fin)
                print "Crea vacio interno"
                self.crear_particion(tipo, msj.particion.libre, montaje, \
                                     tamano, usado, libre, inicio + 1, fin)
                if fin != self.fin_part:
                    print "Y deja espacio libre"
                    inicio = self.escala.get_value()
                    fin = self.fin_part
                    tamano = humanize(fin - inicio)
                    libre = tamano
                    self.crear_particion(msj.particion.primaria, \
                                         msj.particion.libre, montaje, tamano, \
                                         usado, libre, inicio + 1, fin)
            # Lógica
            elif tipo == msj.particion.logica:
                print "Partición Logica"
                self.crear_particion(tipo, formato, montaje, tamano, usado, \
                                     libre, inicio, fin)
                if fin != self.fin_part:
                    print "Que deja espacio extendido libre"
                    inicio = self.escala.get_value()
                    fin = self.fin_part
                    tamano = humanize(fin - inicio)
                    libre = tamano
                    self.crear_particion(msj.particion.extendida, \
                                         msj.particion.libre, montaje, tamano, \
                                         usado, libre, inicio + 1, fin)
            print "------------"

        self.destroy()
        return response

    def crear_particion(self, tipo, formato, montaje, tamano, usado,
                        libre, inicio, fin):
        disp = self.disco
        crear_accion = True
        formatear = False
        # Si es espacio libre
        if formato == msj.particion.libre:
            crear_accion = False
            pop = False
            disp = ''
            montaje = ''
        # Si NO es espacio libre
        else:
            pop = True
            formatear = True
            if tipo == msj.particion.extendida:
                formato = ''
                montaje = ''

        # Entrada de la particion para la tabla
        particion = [disp, tipo, formato, montaje, tamano, usado, libre, \
                     int(inicio), int(fin), formatear]

        # Crea la acción correspondiente que va ejecutarse
        if crear_accion:
            self.acciones.append(['crear', disp, montaje, inicio, fin, \
                                  formato, tipo])

        self.lista = set_partition(self.lista, self.particion_act, particion, \
                                   pop)

    def on_changed(self, widget=None):
        self.lblsize.set_text(humanize(widget.get_value() - self.inicio_part))

    def cmb_tipo_on_changed(self, widget=None):
        tipo = self.cmb_tipo.get_active_text()
        if tipo == 'Extendida':
            self.cmb_fs.set_sensitive(False)
            self.cmb_montaje.set_sensitive(False)
        else:
            self.cmb_fs.set_sensitive(True)
            self.cmb_montaje.set_sensitive(True)

    def cmb_fs_on_changed(self, widget=None):
        fs = self.cmb_fs.get_active_text()
        if fs == 'linux-swap':
            self.cmb_montaje.set_sensitive(False)
        else:
            self.cmb_montaje.set_sensitive(True)

    def cmb_montaje_on_changed(self, widget=None):
        montaje = self.cmb_montaje.get_active_text()
        if montaje == 'Escoger manualmente...':
            self.entrada.show()
            self.validar_punto()
        else:
            self.entrada.hide()
            self.set_response_sensitive(gtk.RESPONSE_OK, True)

    def agregar_p_montaje(self, punto):
        '''Filtra los puntos de montaje que ya están siendo usados para no
        agregarlos a la lista del combobox'''

        data = self.lista
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

        data = self.lista
        aparece = False
        assert isinstance(data, list) or isinstance(data, tuple)
        for fila in data:
            if fila[TblCol.MONTAJE] == self.entrada.get_text().strip():
                aparece = True
        if aparece == False:
            self.set_response_sensitive(gtk.RESPONSE_OK, True)
        else:
            self.set_response_sensitive(gtk.RESPONSE_OK, False)
