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
    minimo = '1GB'
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

        for d in self.discos:
            self.cmb_discos.append_text(d)

        self.cmb_discos.connect("changed", self.seleccionar_disco)
        self.cmb_discos.set_size_request(280, 30)
        self.put(self.cmb_discos, 310, 0)
        self.cmb_discos.show()

        txt_info = "Escoja el disco donde quiere instalar el sistema:"
        self.lbl1 = gtk.Label(txt_info)
        self.lbl1.set_size_request(-1, 30)
        self.lbl1.set_justify(gtk.JUSTIFY_CENTER)
        self.put(self.lbl1, 0, 0)
        self.lbl1.show()

        self.barra_part = barra.Main(self)
        self.barra_part.set_size_request(590, 84)
        self.put(self.barra_part, 0, 35)
        self.barra_part.show()

        txt_info = "Escoja el método de instalación:"
        self.lbl1 = gtk.Label(txt_info)
        self.lbl1.set_size_request(-1, 30)
        self.lbl1.set_justify(gtk.JUSTIFY_CENTER)
        self.put(self.lbl1, 0, 125)
        self.lbl1.show()

        self.cmb_metodo.set_size_request(380, 30)
        self.put(self.cmb_metodo, 210, 125)
        self.cmb_metodo.connect("changed", self.establecer_metodo)
        self.cmb_metodo.show()

        txt_info = "Información:"
        self.lbl1 = gtk.Label(txt_info)
        self.lbl1.set_size_request(590, 30)
        self.lbl1.set_alignment(0, 0)
        self.put(self.lbl1, 0, 165)
        self.lbl1.show()

        self.lbl_info = gtk.Label('Info')
        self.lbl_info.set_size_request(590, 90)
        self.lbl_info.set_alignment(0, 0)
        self.put(self.lbl_info, 0, 185)
        self.lbl_info.show()
        self.establecer_metodo()

    def lista_metodos(self):
        '''
            Crea una lista de los metodos de instalación disponibles para la
            partición
        '''
        self.metodos = {}
        self.cmb_metodo.get_model().clear()
        i = 0
        for p in self.particiones:
            if (gen.h2kb(p[8])) >= (gen.h2kb(self.minimo)) and (p[5] == 'ntfs'
                or p[5] == 'fat32'):
                msg = 'Instalar Canaima en {0} ({1} libres)'
                self.metodos[p[0]] = msg.format(p[0], p[8])
            total_part = gen.h2kb(p[2]) - gen.h2kb(p[1])
            if (total_part) >= gen.h2kb(self.minimo) \
                and p[5] == 'Free Space':
                msg = 'Instalar Canaima en espacio sin particionar ({0} libres)'
                self.metodos['vacio-{0}-{1}'.format(p[1], p[2])] = msg.format(gen.hum(total_part))
                i += 1
        self.metodos['todo'] = ('Usar todo el disco duro')
        #self.metodos['manual'] = ('Particionado Manual')
        for l1, l2 in self.metodos.items():
            self.cmb_metodo.append_text(l2)
        self.cmb_metodo.set_active(0)
        self.cmb_metodo.connect("changed", self.establecer_metodo)

    def establecer_metodo(self, widget=None):
        m = self.cmb_metodo.get_model()
        a = self.cmb_metodo.get_active()
        if a < 0:
            return None
        metodo = [k for k, v in self.metodos.iteritems() if v == m[a][0]][0]
        self.cfg['metodo'] = metodo
        self.metodo = metodo
        if self.metodo == 'todo' or self.metodo == 'vacio':
            msg = 'Si escoge esta opción tenga en cuenta que se borrarán todos '
            msg = msg + 'los datos en el disco que ha\nseleccionado, Este '
            msg = msg + 'borrado no se hará hasta que confirme que realmente '
            msg = msg + 'quiere hacer los\ncambios.'
        elif self.metodo[0:5] == 'vacio':
            self.ini = gen.h2kb(self.metodo.split('-')[1])
            self.fin = gen.h2kb(self.metodo.split('-')[2])
            msg = 'Si escoge esta opción se instalará el sistema en la '
            msg = msg + 'partición sin usar que mide {0}'
            msg = msg.format(gen.hum(self.fin - self.ini))
        else:
            msg = 'Si escoge esta opción se redimensionará la partición '
            msg = msg + '{0} para realizar la instalación.'.format(self.metodo)
        self.lbl_info.set_text(msg)

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

            self.cfg['particion'] = self.particiones[0]
            self.cfg['disco'] = self.disco
            self.lista_metodos()
            self.establecer_metodo()
            self.barra_part.show()
            self.cmb_metodo.show()
            self.lbl_info.show()

class MessageBox(gtk.MessageDialog):
    def __init__(self, padre, parent, disco):
        self.padre = padre
        self.disco = disco
        msg = "El disco {0} necesita una tabla de particiones para\n"
        msg = msg + "la instalación. El tipo de tabla de particiones\n"
        msg = msg + "recomendada es msdos.\n\nSí presiona cancelar no\n"
        msg = msg + "podrá usar este disco para realizar la instalación."
        msg = msg.format(self.disco)
        gtk.MessageDialog.__init__(self, parent, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, gtk.BUTTONS_OK_CANCEL, msg)
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
            cmd = 'parted {0} mklabel {1}'.format(self.disco, gen.get_active_text(self.cmb_label).split(' ')[0])
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
