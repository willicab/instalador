#-*- coding: UTF-8 -*-
'''Clase que configura las particiones'''
# Autor: William Cabrera
# Fecha: 13/10/2011

import pygtk
pygtk.require('2.0')
import gtk
#import commands
import clases.particiones
import clases.general as gen
import clases.barra_particiones as barra
import threading
#import mensaje

class Main(gtk.Fixed):
    disco = ''
    total = ''
    metodo = ''
    discos = []
    particiones = []
    libres = []
    metodos = {}
    lbl_info = gtk.Label('')
    cmb_discos = gtk.combo_box_new_text()
    cmb_metodo = gtk.combo_box_new_text()
    barra_part = gtk.DrawingArea()
    minimo = '5GB'
    part = clases.particiones.Main()
    cfg = {}
    def __init__(self, parent):
        gtk.Fixed.__init__(self)
        self.par = parent

        self.img_distribucion = gtk.Image() 
        self.img_distribucion.set_size_request(590, 240)
        self.put(self.img_distribucion, 0, 20)
        self.img_distribucion.set_from_file('data/buscar-discos.png')
        self.img_distribucion.show()

        thread = threading.Thread(target=self.Iniciar, args=())
        thread.start()
        
    def Iniciar(self):
        self.par.mostrar_barra()
        self.par.info_barra('Buscando discos en el computador')
        self.discos = self.part.lista_discos()

        txt_info = "Escoja el disco donde quiere instalar el sistema:"
        self.lbl1 = gtk.Label(txt_info)
        self.lbl1.set_size_request(-1, 30)
        self.lbl1.set_justify(gtk.JUSTIFY_CENTER)
        self.put(self.lbl1, 0, 0)
        self.lbl1.show()
        
        # Listar Discos
        for disco in self.discos:
            try:
                self.cmb_discos.append_text('{0} ({1})'.format( \
                    disco['description'], \
                    disco['size'].split('(')[1][:-1]
                ))
            except:
                pass
        self.cmb_discos.set_active(0)
        self.seleccionar_disco()
        self.cmb_discos.connect("changed", self.seleccionar_disco)
        self.cmb_discos.set_size_request(280, 30)
        self.put(self.cmb_discos, 310, 0)
        self.cmb_discos.show()
        
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

        self.par.ocultar_barra()
        self.img_distribucion.hide()
    
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
        if self.metodo[0:5] == 'vacio':
            self.ini = gen.h2kb(self.metodo.split('-')[1])
            self.fin = gen.h2kb(self.metodo.split('-')[2])
            msg = 'Si escoge esta opción se instalará el sistema en la '
            msg = msg + 'partición sin usar que mide {0}'
            msg = msg.format(gen.hum(self.fin - self.ini))
        else:
            msg = 'Si escoge esta opción se redimensionará la partición {0} '
            msg = msg + 'para realizar la instalación.'.format(self.metodo)
        self.lbl_info.set_text(msg)

    def seleccionar_disco(self, widget=None):   
        self.disco = self.discos[self.cmb_discos.get_active()]['logical name']
        #print self.disco
        self.particiones = self.part.lista_particiones(self.disco)
        self.total = self.particiones[0][9]
        try:
            self.barra_part.expose()
        except:
            pass
        self.cfg['particion'] = self.particiones[0]
        self.cfg['disco'] = self.disco
        self.lista_metodos()
        self.establecer_metodo()

