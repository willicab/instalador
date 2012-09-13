#-*- coding: UTF-8 -*-
'''
Created on 13/09/2012

@author: Erick Birbe <erickcion@gmail.com>
'''
import gtk
from canaimainstalador.clases.common import humanize

class Main(gtk.Dialog):

    def __init__(self, dispositivo, inicio, fin, usado):
        print type(dispositivo), type(inicio), type(fin), type(usado)
        self.dispositivo = dispositivo
        self.inicio = inicio
        self.fin = fin
        self.usado = usado

        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        gtk.Window.set_position(self, gtk.WIN_POS_CENTER_ALWAYS)

        self.set_title("Redimensionar Partición")
        self.set_size_request(400, 200)
        self.set_resizable(0)

        self.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        self.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        self.set_default_response(gtk.RESPONSE_CANCEL)

        self.escala = gtk.HScale()
        self.escala.set_draw_value(False)
        adj = gtk.Adjustment(self.get_minimo(),
                            self.inicio,
                            self.fin,
                            1.0,
                            5.0,
                            0.0)
        adj.connect("value-changed", self.adj_value_changed)
        self.escala.set_adjustment(adj)
        self.escala.show()

        self.lbl_dispositivo = gtk.Label("Partición '%s'" % self.dispositivo)
        self.lbl_dispositivo.show()

        self.lbl_usado = gtk.Label('Usado')
        self.lbl_usado_num = gtk.Label(humanize(self.get_minimo()))
        self.vb_usado = gtk.VBox()
        self.vb_usado.add(self.lbl_usado)
        self.vb_usado.add(self.lbl_usado_num)
        self.vb_usado.show_all()

        self.lbl_sin_usar = gtk.Label('Sin Usar')
        self.lbl_sin_usar_num = gtk.Label(humanize(self.get_sin_usar()))
        self.vb_sin_usar = gtk.VBox()
        self.vb_sin_usar.add(self.lbl_sin_usar)
        self.vb_sin_usar.add(self.lbl_sin_usar_num)
        self.vb_sin_usar.show_all()

        self.lbl_libre = gtk.Label('Liberado')
        self.lbl_libre_num = gtk.Label(humanize(self.get_libre()))
        self.vb_libre = gtk.VBox()
        self.vb_libre.add(self.lbl_libre)
        self.vb_libre.add(self.lbl_libre_num)
        self.vb_libre.show_all()

        self.hb_leyenda = gtk.HBox()
        self.hb_leyenda.add(self.vb_usado)
        self.hb_leyenda.add(self.vb_sin_usar)
        self.hb_leyenda.add(self.vb_libre)
        self.hb_leyenda.show_all()

        self.cont = gtk.VBox()
        self.cont.add(self.lbl_dispositivo)
        self.cont.add(self.hb_leyenda)
        self.cont.add(self.escala)
        self.cont.show()

        self.vbox.pack_start(self.cont)

        self.procesar_respuesta(self.run())

    def get_tamano(self):
        if self.fin < self.inicio:
            raise Exception("El inicio fín de la partición es menor al inicio.")
        return self.fin - self.inicio
    def get_minimo(self):
        return self.inicio + self.usado
    def get_maximo(self):
        return self.fin
    def get_sin_usar(self):
        return self.escala.get_value() - self.get_minimo()
    def get_libre(self):
        return self.fin - self.escala.get_value()

    def adj_value_changed(self, adjustment):
        if adjustment.value <= self.get_minimo():
            adjustment.set_value(self.get_minimo())
        self.lbl_sin_usar_num.set_text(humanize(self.get_sin_usar()))
        self.lbl_libre_num.set_text(humanize(self.get_libre()))

    def procesar_respuesta(self, response=None):

        if not response:
            return response

        if response == gtk.RESPONSE_OK:
            pass
        else:
            pass

        self.destroy()
        return response

if __name__ == "__main__":
    d = Main('/dev/sdz1', 1024 * 1024, 1024 * 1024 * 2, 1024 * 512)
