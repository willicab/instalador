#-*- coding: UTF-8 -*-
'''Clase que configura las particiones'''
# Autor: William Cabrera
# Fecha: 13/10/2011

# Módulos globales
import gtk, os, threading

# Módulos locales
import clases.particiones
import clases.general as gen
import clases.barra_particiones as barra

class Main(gtk.Fixed):
    disco = ''
    total = ''
    metodo = ''
    discos = []
    particiones = []
    libres = []
    metodos = {}
    cfg = {}
    minimo = gen.h2kb('1GB')
    lbl_info = gtk.Label('')
    cmb_discos = gtk.combo_box_new_text()
    cmb_metodo = gtk.combo_box_new_text()
    barra_part = gtk.DrawingArea()
    part = clases.particiones.Main()

    def __init__(self, parent):
        gtk.Fixed.__init__(self)
        self.par = parent
        self.Iniciar()

    def Iniciar(self):

        # Listar Discos
        self.discos = self.part.lista_discos()
        print 'Se han encontrado los siguientes discos: {0}'.format(self.discos)

        self.lbl1 = gtk.Label('Seleccione el disco donde desea instalar Canaima:')
        self.lbl1.set_size_request(690, 20)
        self.lbl1.set_alignment(0, 0)
        self.put(self.lbl1, 0, 0)

        for d in self.discos:
            self.cmb_discos.append_text(d)
        self.cmb_discos.set_active(0)
        self.cmb_discos.set_size_request(690, 30)
        self.put(self.cmb_discos, 0, 25)
        self.cmb_discos.connect('changed', self.seleccionar_disco)

        self.barra_part = barra.Main(self)
        self.barra_part.set_size_request(690, 100)
        self.put(self.barra_part, 0, 60)

        self.lbl2 = gtk.Label('Seleccione el método de instalación:')
        self.lbl2.set_size_request(690, 20)
        self.lbl2.set_alignment(0, 0)
        self.put(self.lbl2, 0, 165)

        self.cmb_metodo.set_size_request(690, 30)
        self.put(self.cmb_metodo, 0, 190)
        self.cmb_metodo.connect('changed', self.establecer_metodo)

        self.lbl4 = gtk.Label()
        self.lbl4.set_size_request(690, 90)
        self.lbl4.set_alignment(0, 0)
        self.lbl4.set_line_wrap(True)
        self.put(self.lbl4, 0, 225)

        self.show_all()
        self.seleccionar_disco()

    def seleccionar_disco(self, widget=None):
        self.disco = self.cmb_discos.get_active_text()
        print '{0} seleccionado'.format(self.disco)

        self.particiones = self.part.lista_particiones(self.disco)

        if len(self.particiones) == 0:
            MessageBox(self, self.par, self.disco)
        else:
            self.total = self.particiones[0][9]
            try:
                self.barra_part.expose()
            except:
                pass

            self.lista_metodos()
            self.establecer_metodo()
            self.barra_part.show()
            self.cmb_metodo.show()
            self.lbl4.show()

    def lista_metodos(self):
        '''
            Crea una lista de los metodos de instalación disponibles para la
            partición
        '''
        i = 0
        self.metodos = {}
        self.cmb_metodo.get_model().clear()
        total = self.total
        minimo = self.minimo
        tini = self.particiones[0][1]
        tfin = self.particiones[0][2]

        for t in self.particiones:
            ini = t[1]
            fin = t[2]
            if tini > ini: tini = ini
            if tfin < fin: tfin = fin
            if t[5] == 'primary' and t[4] != 'free':
                i += 1

        if total > minimo:
            self.metodos['MANUAL'] = 'Instalar editando particiones manualmente'

            if i < 4:
                for p in self.particiones:
                    tam = p[3]
                    libre = p[8]
                    ini = p[1]
                    fin = p[2]
                    part = p[0]
                    fs = p[5]

                    if fs != 'free' and libre >= minimo:
                        msg = 'Instalar redimensionando {0} para liberar espacio ({1} libres)'
                        met = 'REDIM:{0}:{1}:{2}'.format(part, ini, fin)
                        self.metodos[met] = msg.format(part, gen.hum(libre))

                    if fs == 'free' and tam >= minimo:
                        msg = 'Instalar usando espacio libre disponible ({0})'
                        met = 'LIBRE:{0}:{1}:{2}'.format(part, ini, fin)
                        self.metodos[met] = msg.format(gen.hum(tam))

            met = 'TODO:{0}:{1}:{2}'.format(self.disco, tini, tfin)
            msg = 'Instalar usando todo el disco ({0})'
            self.metodos[met] = msg.format(gen.hum(total))

        else:
            self.metodos['NONE'] = 'El tamaño del disco no es suficiente'

        for l1, l2 in self.metodos.items():
            self.cmb_metodo.append_text(l2)
        self.cmb_metodo.set_active(0)

    def establecer_metodo(self, widget=None):
        m = self.cmb_metodo.get_model()
        a = self.cmb_metodo.get_active()

        if a < 0:
            return None

        self.metodo = [k for k, v in self.metodos.iteritems() if v == m[a][0]][0]

        if self.metodo.split(':')[0] == 'TODO':
            msg = 'Si escoge esta opción tenga en cuenta que se borrarán todos \
los datos en el disco que ha seleccionado, Este borrado no se hará hasta que \
confirme que realmente quiere hacer los cambios.'
            self.ini = self.metodo.split(':')[2]
            self.fin = self.metodo.split(':')[3]
        elif self.metodo.split(':')[0] == 'LIBRE':
            msg = 'Si escoge esta opción se instalará el sistema en la \
partición sin usar que mide {0}'.format(gen.hum(2))
            self.ini = self.metodo.split(':')[2]
            self.fin = self.metodo.split(':')[3]
        elif self.metodo.split(':')[0] == 'REDIM':
            msg = 'Si escoge esta opción se redimensionará la partición {0} \
para realizar la instalación.'.format(self.metodo)
        elif self.metodo == 'MANUAL':
            msg = 'Si escoge esta opción podrá modificar manualmente el disco \
{0}'.format(self.disco)
        elif self.metodo == 'NONE':
            msg = 'Si escoge esta opción se instalará el sistema en la \
partición sin usar que mide {0}'.format(gen.hum(2))
        else:
            pass

        self.lbl4.set_text(msg)

class MessageBox(gtk.MessageDialog):
    def __init__(self, padre, parent, disco):
        self.padre = padre
        self.disco = disco
        msg = "El disco {0} necesita una tabla de particiones para la \
instalación. El tipo de tabla de particiones recomendada es msdos.\n\n \
Si presiona cancelar no podrá usar este disco para realizar la \
instalación.".format(self.disco)
        gtk.MessageDialog.__init__(self, parent, gtk.DIALOG_MODAL | \
                                   gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_INFO, gtk.BUTTONS_OK_CANCEL,
                                   msg)
        self.connect('response', self._handle_clicked)
        #self.add_button("Cancelar", gtk.RESPONSE_CANCEL)
        #self.set_default_response(gtk.RESPONSE_OK)
        self.set_title("Disco {0} sin tabla de particiones".format(self.disco))
        #self.set_size_request(400, 200)
        #self.set_resizable(0)
        #self.set_border_width(0)
        # Contenedor General
        self.cont = gtk.Fixed()
        self.cont.show()
        self.vbox.pack_start(self.cont)

        #Sistema de Archivos
        self.hbox = gtk.HBox()
        self.vbox.pack_start(self.hbox)
        self.lbl = gtk.Label('Tipo de tabla de particiones: ')
        self.lbl.set_alignment(0, 0.5)
        self.lbl.show()
        self.hbox.pack_start(self.lbl, False)
        self.cmb_label = gtk.combo_box_new_text()
        self.cmb_label.set_size_request(100, 30)
        self.hbox.pack_start(self.cmb_label)
        self.cmb_label.append_text('msdos (recomendada)')
        self.cmb_label.append_text('aix')
        self.cmb_label.append_text('amiga')
        self.cmb_label.append_text('bsd')
        self.cmb_label.append_text('dvh')
        self.cmb_label.append_text('gpt')
        self.cmb_label.append_text('mac')
        self.cmb_label.append_text('pc98')
        self.cmb_label.append_text('sun')
        self.cmb_label.append_text('loop')
        self.cmb_label.set_active(0)
        self.cmb_label.show()

        self.show_all()
        #self.run()
        #self.destroy()
    def _handle_clicked(self, *args):
        # -5 = OK
        # -6 = CANCEL
        if args[1] == -5:
            cmd = 'parted {0} mklabel {1}'.format(self.disco,
                      gen.get_active_text(self.cmb_label).split(' ')[0])
            os.system(cmd)
            print cmd
            self.padre.seleccionar_disco()
            self.padre.barra_part.show()
            self.padre.cmb_metodo.show()
            self.padre.lbl_info.show()

        else:
            self.padre.barra_part.hide()
            self.padre.cmb_metodo.hide()
            self.padre.lbl_info.hide()
        self.destroy()

        #self.connect('response', self.handle_clicked)

        #def handle_clicked(self, widget=None):
        #    self.destroy()

class ThreadGenerator(threading.Thread):
    def __init__(self, reference, function, params,
                    gtk=False, window=False, event=False):
        threading.Thread.__init__(self)
        self._gtk = gtk
        self._window = window
        self._function = function
        self._params = params
        self._event = event
        self.start()

    def run(self):
        if self._gtk:
            gtk.gdk.threads_enter()

        if self._event:
            self._event.wait()

        self._function(**self._params)

        if self._gtk:
            gtk.gdk.threads_leave()

        if self._window:
            self._window.hide()
