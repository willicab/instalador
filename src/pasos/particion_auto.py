#-*- coding: UTF-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
import commands
import clases.particiones
import clases.general
import widget

class Main(gtk.Fixed):
    barra = gtk.Image()
    burning = ''#widget.Burning(self)
    part = clases.particiones.Main()
    gen = clases.general
    particion = ''
    libre = []
    minimo = '3GB'
    swap = '1GB'
    libre = '500MB'
    w = []
    cfg = {}
    def __init__(self, particion):
        gtk.Fixed.__init__(self)
        self.particion = particion
        self.cfg['particion'] = particion
        self.cfg['disco'] = particion[:-1]
        self.cfg['num'] = particion[-1:]

        txt_info = "Seleccione el tamaño que desea usar para la instalación"
        self.lbl1 = gtk.Label(txt_info)
        self.lbl1.set_size_request(590, 30)
        self.lbl1.set_justify(gtk.JUSTIFY_CENTER)
        self.put(self.lbl1, 0, 0)
        self.lbl1.show()
        
        self.w = self.img_particion()
        
        p = self.part.lista_particiones(particion[:-1], self.particion)[0]
        self.cfg['ini'] = p[1]
        self.cfg['fin'] = p[2]
        usado = ((self.gen.kb(p[7]) + self.gen.kb(self.libre)) * 590) / int(p[3][:-2])
        minimo = (self.gen.kb(self.minimo) * 590) / int(p[3][:-2])
        self.cur_value = 0
        self.scale = gtk.HScale()
        self.scale.set_range((self.gen.kb(p[7]) + self.gen.kb(self.libre)), int(p[3][:-2]) - self.gen.kb(self.minimo))
        self.scale.set_digits(0)
        self.scale.set_size_request((self.w[3] - self.w[0]), 20)
        self.scale.set_value(self.cur_value)
        self.scale.connect("value-changed", self.on_changed)
        self.scale.set_value(((self.gen.kb(p[7]) + self.gen.kb(self.libre)) + self.gen.kb(self.minimo)) / 2 )
        self.scale.show()
        self.put(self.scale, self.w[0], 120)
        
        self.burning = widget.Burning(self, int(p[3][:-2]), self.gen.kb(p[7]), self.gen.kb(self.minimo), particion)
        self.burning.set_size_request(590, 80)
        self.burning.show()
        self.put(self.burning, 0, 35)
        #vbox.pack_start(self.burning, False, False, 0)

        #self.lbllibre = gtk.Label(txt_info)
        #self.lbllibre.set_size_request(590, 30)
        #self.lbllibre.set_justify(gtk.JUSTIFY_LEFT)
        #self.put(self.lbllibre, 0, 150)
        #self.lbllibre.show()

        button = gtk.RadioButton(None, "Realizar la instalación en una sola partición")
        button.connect("toggled", self.callback, "particion_1")
        button.set_size_request(590, 20)
        button.set_active(True)
        self.put(button, 0, 155)
        button.show()

        button = gtk.RadioButton(button, "Separar la partición /home(Recomendado)")
        button.connect("toggled", self.callback, "particion_2")
        button.set_size_request(590, 20)
        button.set_active(True)
        self.put(button, 0, 180)
        button.show()

        button = gtk.RadioButton(button, "Separar las particiones /home, /usr y /boot")
        button.connect("toggled", self.callback, "particion_3")
        button.set_size_request(590, 20)
        button.set_active(True)
        self.put(button, 0, 205)
        button.show()

    def callback(self, widget, data=None):
        if widget.get_active() == True:
            pass
        print "%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()])

    def on_changed(self, widget=None):
        self.cur_value = widget.get_value()
        self.burning.queue_draw()
        t = '{0}GB'.format(self.gen.redondear(widget.get_value()/1024/1024, 1)) if \
            int(widget.get_value()/1024/1024)>1 else \
            '{0}MB'.format(self.gen.redondear(widget.get_value()/1024, 1))
        #self.lbllibre.set_text('Espacio para NTFS: {0}'.format(t))
        self.cfg['desde'] = int(widget.get_value())
        self.cfg['ext4'] = {'ini': self.cfg['desde'] + self.cfg['ini'], 'fin': self.cfg['fin'] - self.gen.kb(self.swap)}
        self.cfg['swap'] = {'ini': self.cfg['fin'] - 1048576, 'fin': self.cfg['fin']}

    def get_cur_value(self):
        return self.cur_value
        
    def img_particion(self, x=0):
        import Image
        
        particion = self.particion
        w_total = 588
        h_total = 80
        p = self.part.lista_particiones(particion[:-1], self.particion)[0]
        s = p[5].split('(')[0].replace(' ', '_')
        w_usado = ((self.gen.kb(p[7]) + self.gen.kb(self.libre)) * w_total) / self.gen.kb(p[3])
        w_libre = w_total - w_usado
        
        t_min = self.gen.kb(p[3]) - self.gen.kb(self.minimo)
        t_min = (t_min * w_total) / self.gen.kb(p[3])
        if x == 0 : x = w_usado + 1 #(w_usado + t_min) / 2
        x = int(x)
        self.cfg['desde'] = (x * self.gen.kb(p[3])) / w_total
        self.cfg['ini'] = self.gen.kb(p[1])
        self.cfg['fin'] = self.gen.kb(p[2])
        self.cfg['ext4'] = {'ini': self.cfg['desde'] + self.cfg['ini'], 'fin': self.cfg['fin'] - 1048576}
        self.cfg['swap'] = {'ini': self.cfg['fin'] - 1048576, 'fin': self.cfg['fin']}
        
        return [w_usado, w_libre, x - w_usado, t_min, w_total]
        
    def tam(self):
        w_total = 588
        h_total = 80
        p = self.part.lista_particiones(particion[:-1], self.particion)[0]
        s = p[5].split('(')[0].replace(' ', '_')
        im_base = Image.open("data/particion/base.png")
        src_libre = "data/particion/canaima.png"
        src_usado = "data/particion/" + s + "_usado.png"
        w_usado = (self.gen.kb(p[7]) * w_total) / self.gen.kb(p[3])
        w_libre = w_total - w_usado
        
        t_min = self.gen.kb(p[3]) - self.gen.kb(self.minimo)
        t_min = (t_min * w_total) / self.gen.kb(p[3])
        x = (w_usado + t_min) / 2
        
        return {
            'w_total' : w_total,
            'h_total' : h_total,
        }
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
