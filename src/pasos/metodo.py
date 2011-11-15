#-*- coding: UTF-8 -*-
'''Clase que configura las particiones'''
# Autor: William Cabrera
# Fecha: 13/10/2011

import pygtk
pygtk.require('2.0')
import gtk
import commands
import clases.particiones

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
    barra = gtk.Image()
    minimo = '3GB'
    part = clases.particiones.Main()
    
    def __init__(self):
        gtk.Fixed.__init__(self)
        
        self.discos = self.part.lista_discos()
        
        txt_info = "Escoja el disco donde quiere instalar el sistema:"
        self.lbl1 = gtk.Label(txt_info)
        self.lbl1.set_size_request(-1, 30)
        self.lbl1.set_justify(gtk.JUSTIFY_CENTER)
        self.put(self.lbl1, 0, 0)
        self.lbl1.show()
        
        # Listar Discos
        # print self.discos
        for disco in self.discos:
            self.cmb_discos.append_text(str(disco['description']) + \
            ' (' + disco['logical name'] + ')')
        self.cmb_discos.set_active(0)
        self.seleccionar_disco()
        self.cmb_discos.connect("changed", self.seleccionar_disco)
        self.cmb_discos.set_size_request(280, 30)
        self.put(self.cmb_discos, 310, 0)
        self.cmb_discos.show()
        
        self.barra.set_size_request(590, 84)
        self.put(self.barra, 0, 35)
        self.barra.show()
        
        txt_info = "Escoja el método de instalación:"
        self.lbl1 = gtk.Label(txt_info)
        self.lbl1.set_size_request(-1, 30)
        self.lbl1.set_justify(gtk.JUSTIFY_CENTER)
        self.put(self.lbl1, 0, 125)
        self.lbl1.show()

        self.cmb_metodo.set_size_request(380, 30)
        self.put(self.cmb_metodo, 210, 125)
        self.cmb_metodo.show()
        
        self.frm_info = gtk.Frame('Información')
        self.frm_info.set_size_request(590, 120)
        self.frm_info.show()
        self.put(self.frm_info, 0, 155)
        #self.lbl_info = gtk.Label('Info')
        self.frm_info.add(self.lbl_info)
        self.lbl_info.show()

            
    def kb(self, num):
        unidad = num[-2:]
        num = num[:-2].replace(',', '.')
        num = int(float(num))
        if unidad == 'GB': return num * 1048576 # Gb a Kb
        if unidad == 'MB': return num * 1024    # Mb a Kb
        if unidad == 'kB': return num           # Kb a Kb
        return num / 1024                       # Bytes a Kb
        
    def redondear(self, w, dec=0):
        if dec == 0:
            return int(w) + 1 if int(str(w).split('.')[1][0]) >= 5 else int(w)
        else:
            return str(w).split('.')[0] + '.' + str(w).split('.')[1][0:dec]

    def lista_metodos(self):
        '''
            Crea una lista de los metodos de instalación disponibles para la
            partición
        '''
        self.metodos = {}
        self.cmb_metodo.get_model().clear()
        for p in self.particiones:
            if (self.kb(p[8])) >= (self.kb(self.minimo)):
                msg = 'Instalar Canaima en {0} ({1} libres)'
                self.metodos[p[0]] = msg.format(p[0], p[8])
        self.metodos['todo'] = ('Usar todo el disco duro')
        self.metodos['manual'] = ('Particionado Manual')
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
        self.metodo = metodo
        
    def seleccionar_disco(self, widget=None):   
        self.disco = self.discos[self.cmb_discos.get_active()]['logical name']
        self.total = self.discos[self.cmb_discos.get_active()]['size']. \
            split('(')[1][:-1]
        self.particiones = self.part.lista_particiones(self.disco)
        self.crear_imagen()
        self.lista_metodos()
        self.establecer_metodo()
        
    def crear_imagen(self):
        '''
            Crea una imagen representativa de las particiones
        '''
        import Image
        
        w_total = 588
        h_total = 80
        
        total = float(self.kb(self.total))
        im_base = Image.open("data/particion/base.png")
        for p in self.particiones:
            w = self.redondear((float(self.kb(p[3])) * w_total) / (total))
            if w < 3: w = 3
            x = self.redondear((float(self.kb(p[1])) * w_total) / float(total))
            s = p[5].split('(')[0].replace(' ', '_')
            # print 'tipo', s
            src = "data/particion/" + s + ".png"
            src_usado = "data/particion/" + s + "_usado.png"

            if p[5].find('swap') == -1 and p[5].find('Free') == -1:
                w_usado = (self.kb(p[7]) * w) / self.kb(p[3])
                img_usado = Image.open(src_usado).resize((w_usado, 80))
                box_usado = (0, 0, w_usado, 80)
                region_usado = img_usado.crop(box_usado)

            im_total = Image.open(src).resize((w - 2, 80))
            box = (0, 0, w - 2, 80)
            region = im_total.crop(box)
            if p[5].find('swap') == -1 and p[5].find('Free') == -1:
                region.paste(region_usado, box_usado)

            box = (x + 2, 2, w + x, 82)
            im_base.paste(region, box)
            
        im_base.save('data/particion/base_mod.png')
        self.barra.set_from_file('data/particion/base_mod.png')
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
