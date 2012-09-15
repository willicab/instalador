#-*- coding: UTF-8 -*-
'''
Created on 13/09/2012

@author: Erick Birbe <erickcion@gmail.com>
'''
import gtk
from canaimainstalador.clases.common import humanize, TblCol, floatify
from canaimainstalador.translator import msj

class Main(gtk.Dialog):

    def __init__(self, lista, fila, acciones):
        self.lista = lista
        self.acciones = acciones
        self.num_fila_act = self._get_num_fila_act(fila)
        self.dispositivo = fila[TblCol.DISPOSITIVO]
        self.inicio = fila[TblCol.INICIO]
        self.fin = fila[TblCol.FIN]
        self.usado = floatify(fila[TblCol.USADO])

        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        gtk.Window.set_position(self, gtk.WIN_POS_CENTER_ALWAYS)

        self.set_title("Redimensionar Partición")
        self.set_size_request(400, 200)
        self.set_resizable(0)

        self.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        self.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        self.set_response_sensitive(gtk.RESPONSE_OK, False)
        self.set_default_response(gtk.RESPONSE_CANCEL)

        self.escala = gtk.HScale()
        self.escala.set_draw_value(False)
        adj = gtk.Adjustment(self.fin,
                            self.inicio,
                            self.get_maximo(),
                            1.0,
                            5.0,
                            0.0)
        adj.connect("value-changed", self.adj_value_changed)
        self.escala.set_adjustment(adj)
        self.escala.show()

        self.lbl_dispositivo = gtk.Label("Partición '%s'" % self.dispositivo)
        self.lbl_dispositivo.show()

        self.lbl_tamano = gtk.Label('Tamaño')
        self.lbl_tamano_num = gtk.Label(humanize(self.get_tamano()))
        self.vb_tamano = gtk.VBox()
        self.vb_tamano.add(self.lbl_tamano)
        self.vb_tamano.add(self.lbl_tamano_num)
        self.vb_tamano.show_all()

        self.lbl_usado = gtk.Label('Usado')
        self.lbl_usado_num = gtk.Label(humanize(self.usado))
        self.vb_usado = gtk.VBox()
        self.vb_usado.add(self.lbl_usado)
        self.vb_usado.add(self.lbl_usado_num)
        self.vb_usado.show_all()

        self.lbl_libre = gtk.Label('Libre')
        self.lbl_libre_num = gtk.Label(humanize(self.get_libre()))
        self.vb_libre = gtk.VBox()
        self.vb_libre.add(self.lbl_libre)
        self.vb_libre.add(self.lbl_libre_num)
        self.vb_libre.show_all()

        self.lbl_sin_particion = gtk.Label('Sin Particionar')
        self.lbl_sin_particion_num = gtk.Label(humanize(self.get_sin_particion()))
        self.vb_sin_particion = gtk.VBox()
        self.vb_sin_particion.add(self.lbl_sin_particion)
        self.vb_sin_particion.add(self.lbl_sin_particion_num)
        self.vb_sin_particion.show_all()

        self.hb_leyenda = gtk.HBox()
        self.hb_leyenda.add(self.vb_tamano)
        self.hb_leyenda.add(self.vb_usado)
        self.hb_leyenda.add(self.vb_libre)
        self.hb_leyenda.add(self.vb_sin_particion)
        self.hb_leyenda.show_all()

        self.cont = gtk.VBox()
        self.cont.add(self.lbl_dispositivo)
        self.cont.add(self.hb_leyenda)
        self.cont.add(self.escala)
        self.cont.show()

        self.vbox.pack_start(self.cont)

        self.procesar_respuesta(self.run())

    def get_tamano(self):
        return self.escala.get_value() - self.inicio
    def get_minimo(self):
        'El tamaño minimo al que se puede redimensionar la partición'
        return self.inicio + self.usado
    def get_maximo(self):
        'El tamaño maximo al que se puede redimensionar la partición'
        return self.fin + self.get_espacio_sin_particionar()
    def get_libre(self):
        'Retorna el espacio libre de la partición'
        return self.escala.get_value() - self.get_minimo()
    def get_sin_particion(self):
        'Retorna el espacio sin particionar que va quedando'
        return self.get_maximo() - self.escala.get_value()
    def _get_num_fila_act(self, fila):
        '''Obtiene el numero de la fila seleccionada en la tabla.
        Este metodo deberia usarse solo una vez para darle el valor a la \
        propiedad self.num_fila_act'''
        for i in range(len(self.lista)):
            if fila == tuple(self.lista[i]):
                return i
        return None
    def hay_fila_siguiente(self):
        'Verifica si la lista contiene una fila siguiente'
        if  self.num_fila_act < len(self.lista) - 1:
            return True
        else:
            return False
    def get_fila_siguiente(self):
        '''Retorna la fila siguiente si existe y se trata de un espacio libre,
        sino retorna None'''
        if self.hay_fila_siguiente():
            fila_actual = self.lista[self.num_fila_act]
            fila_siguiente = self.lista[self.num_fila_act + 1]
            # Si la particion es del mismo tipo (Extendida o Primaria)
            # Y se trata de un espacio libre
            if fila_actual[TblCol.TIPO] == fila_siguiente[TblCol.TIPO] \
            and fila_siguiente[TblCol.FORMATO] == msj.particion.libre:
                return fila_siguiente
        return None
    def get_espacio_sin_particionar(self):
        'Retona la cantidad de espacio libre que hay luego de la particion'
        fila_siguiente = self.get_fila_siguiente()
        if fila_siguiente != None:
            return fila_siguiente[TblCol.FIN] - fila_siguiente[TblCol.INICIO]
        else:
            return 0
    def adj_value_changed(self, adjustment):
        'Acciones a tomar cuando se mueve el valor de la escala'
        # Activa el boton de aceptar sólo si se ha modificado el valor
        if adjustment.value == self.fin:
            self.set_response_sensitive(gtk.RESPONSE_OK, False)
        else:
            self.set_response_sensitive(gtk.RESPONSE_OK, True)
        # No reducir menos del espacio usado
        if adjustment.value <= self.get_minimo():
            adjustment.set_value(self.get_minimo())
        # Actualizar los textos con los valores
        self.lbl_tamano_num.set_text(humanize(self.get_tamano()))
        self.lbl_libre_num.set_text(humanize(self.get_libre()))
        self.lbl_sin_particion_num.set_text(humanize(self.get_sin_particion()))

    def procesar_respuesta(self, response=None):

        if not response:
            return response

        part_actual = self.lista[self.num_fila_act]
        part_sig = self.get_fila_siguiente()

        if response == gtk.RESPONSE_OK:

            part_actual[TblCol.FIN] = self.escala.get_value()
            # Calculamos el nuevo tamaño y espacio libre
            part_actual[TblCol.TAMANO] = humanize(self.get_tamano())
            part_actual[TblCol.LIBRE] = humanize(self.get_libre())

            # Si dejamos espacio libre
            if part_actual[TblCol.FIN] < self.get_maximo():
                # Si hay particion libre siguiente, solo modificamos algunos 
                # valores
                if part_sig:
                    part_sig[TblCol.INICIO] = part_actual[TblCol.FIN] + 1
                    tamano = humanize(
                                part_sig[TblCol.FIN] - part_sig[TblCol.INICIO])
                    part_sig[TblCol.TAMANO] = tamano
                    part_sig[TblCol.LIBRE] = tamano
                    self.lista[self.num_fila_act + 1] = part_sig
                # Si no hay particion siguiente, tenemos que crear toda la fila
                else:
                    part_sig = list(range(len(part_actual)))
                    part_sig[TblCol.DISPOSITIVO] = ''
                    part_sig[TblCol.TIPO] = part_actual[TblCol.TIPO]
                    part_sig[TblCol.FORMATO] = msj.particion.libre
                    part_sig[TblCol.MONTAJE] = ''
                    part_sig[TblCol.TAMANO] = humanize(self.get_sin_particion())
                    part_sig[TblCol.USADO] = humanize(0)
                    part_sig[TblCol.LIBRE] = humanize(self.get_sin_particion())
                    part_sig[TblCol.INICIO] = part_actual[TblCol.FIN] + 1
                    part_sig[TblCol.FIN] = self.get_maximo()
                    tmp = []
                    for i in range(len(self.lista)):
                        if i == self.num_fila_act:
                            tmp.append(part_actual)
                            tmp.append(part_sig)
                        else:
                            tmp.append(self.lista[i])
                    self.lista = tmp

            # Sino dejamos espacio libre
            elif part_sig:
                self.lista.remove(part_sig)

            self.acciones.append([
                                  'redimensionar',
                                  part_actual[TblCol.DISPOSITIVO],
                                  part_actual[TblCol.MONTAJE],
                                  part_actual[TblCol.INICIO],
                                  part_actual[TblCol.FIN],
                                  part_actual[TblCol.FORMATO],
                                  part_actual[TblCol.TIPO]
                                  ])
        self.destroy()
        return response

if __name__ == "__main__":
    d = Main('/dev/sdz1', 1024 * 1024, 1024 * 1024 * 2, 1024 * 512)
