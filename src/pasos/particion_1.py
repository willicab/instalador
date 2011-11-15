#-*- coding: UTF-8 -*-
'''Clase que configura las particiones'''
# Autor: William Cabrera
# Fecha: 13/10/2011

import pygtk
pygtk.require('2.0')
import gtk
import os
import layouts
import commands
#import parted

class Particion(gtk.Fixed):
    discos = ''
    partitions = {}
    cmb_discos = gtk.combo_box_new_text()
    cmb_dev = gtk.combo_box_new_text()
    barra = gtk.Image()
    lbl_info = gtk.Label('')
    minimo = 5368709120 # Espacio mínimo, en bytes
    disk_total = 0
    def __init__(self):
        gtk.Fixed.__init__(self)
        #self.disks = self.get_disks()
        
        txt_info = "Escoja el disco donde quiere instalar el sistema:"
        self.lbl1 = gtk.Label(txt_info)
        self.lbl1.set_size_request(-1, 30)
        self.lbl1.set_justify(gtk.JUSTIFY_CENTER)
        self.put(self.lbl1, 0, 0)
        self.lbl1.show()
        
        # Listar Discos
        self.discos = self.lista_discos()
        #self.cmb_dev = gtk.combo_box_new_text()
        for disco in self.discos:
            print disco
            self.cmb_discos.append_text(str(disco['description']) + ' (' + disco['logical name'] + ')')
        self.cmb_discos.set_active(0)
        self.set_disk()
        self.cmb_discos.connect("changed", self.set_disk)
        self.cmb_discos.set_size_request(280, 30)
        self.put(self.cmb_discos, 310, 0)
        self.cmb_discos.show()

        #self.barra = gtk.Image()
        #self.barra.set_from_file('data/particion/base_mod.png')
        self.barra.set_size_request(590, 80)
        self.put(self.barra, 0, 35)
        self.barra.show()

        txt_info = "Escoja el método de instalación:"
        self.lbl1 = gtk.Label(txt_info)
        self.lbl1.set_size_request(-1, 30)
        self.lbl1.set_justify(gtk.JUSTIFY_CENTER)
        self.put(self.lbl1, 0, 120)
        self.lbl1.show()

        #self.cmb_dev = gtk.combo_box_new_text()
        #for l1, l2 in layouts.list_layouts.items():
            #self.cmb_dist.append_text(l1)
        self.cmb_dev.set_size_request(380, 30)
        self.put(self.cmb_dev, 210, 120)
        self.cmb_dev.show()

        self.frm_info = gtk.Frame('Información')
        self.frm_info.set_size_request(590, 120)
        self.frm_info.show()
        self.put(self.frm_info, 0, 155)
        #self.lbl_info = gtk.Label('Info')
        self.frm_info.add(self.lbl_info)
        self.lbl_info.show()

    def get_disks(self):
        '''
            devuelve los discos que están conectados al equipo
        '''
        leer = False
        i = -1
        disks = []
        opt = {}
        a = commands.getstatusoutput("lshw -class disk")[1].split('\n')
        for disk in a:
            if disk[2:] == "*-disk":
                if i >= 0: 
                    disks.append(opt)
                    opt = {}
                i = i + 1
                leer = True
                continue
            if disk[2:9] == "*-cdrom":
                leer = False
                continue
            if leer == True:
                disk = disk[7:].split(': ')
                opt[disk[0]] = disk[1]
        disks.append(opt)
        self.img_partitions
        return disks

    def get_partitions(self):
        '''
            devuelve las particiones de un disco dado
        '''
        fdisk_output = commands.getoutput("fdisk -l {0}".format(self.discos))
        result = {}
        parts = []
        for line in fdisk_output.split("\n"):
            if line.endswith('cylinders'):
                #print 'Cilindros: ' + str(line.split(',')[2].split(' ')[1])
                cylinders = int(line.split(',')[2].split(' ')[1])
                #print cylinders
            if line.endswith('bytes') and line.startswith('Disk'):
                #print 'Cilindros: ' + str(line.split(',')[2].split(' ')[1])
                self.discos_total = int(line.split(',')[1].split(' ')[1])
                #print total
            if not line.startswith("/"): continue
            parts = line.split()
            #self.discos_total = int(parts[3].rstrip("+"))
            inf = {}
            if self.is_mounted(parts[0]) == False: self.mount(parts[0])
            part = self.espacios(parts[0])
            #print self.discos_total, int(part[1])
            if parts[1] == "*":
                inf['bootable'] = True
                del parts[1]
            else:
                inf['bootable'] = False
            #print int(part[1]), int(parts[3].rstrip("+"))
            inf['blocks'] = int(part[1])
            inf['cylinders'] = int(cylinders)           # Total de cilindros
            inf['used'] = int(part[2])                  # Bloques Usados
            inf['free'] = int(part[3])                  # Bloques Libres
            inf['perc'] = int(part[4].strip('%'))       # Porcentaje Usado
            inf['path'] = str(parts[0])                 # Ruta del dispositivo
            inf['start'] = int(parts[1])                # Inicio
            inf['end'] = int(parts[2])                  # Fin
            inf['cilindros'] = int(parts[3].rstrip("+"))# Cilindros totales
            inf['partition_id'] = int(parts[4], 16)     # ID de la partición
            inf['partition_id_string'] = " ".join(parts[5:])
            result[parts[0]] = inf
            #print result
        return result
        
    def set_disk(self, widget=None):
        self.discos = self.discos[self.cmb_discos.get_active()]['logical name']
        self.partitions = self.get_partitions()
        self.img_partitions()
        self.list_install()
        self.listar_particiones(self.discos)
        
    def img_partitions(self):
        '''
            Crea una imagen representativa de las particiones
        '''
        import Image
        i = 0
        #im = []
        im_base = Image.open("data/particion/base.png")
        bar = ['amarillo', 'azul', 'rojo', 'verde', 'cyan']
        langs = self.partitions.keys()
        langs.sort()
        for part in langs:
            mypart = self.partitions[part]
            #for line in mount_output.split("\n"):
            #    print cmd, line, (self.partitions[part]['end'] - self.partitions[part]['start'])
            w_total = 590
            # Saco el procentaje que tiene la partición del total
            perc = float((mypart['end'] - mypart['start']) * 100) / mypart['cylinders']
            # Saco el Ancho que debe tener la imagen
            w = self.redondear(float((perc * w_total) / 100))
            # Saco la posición en X que dbe tener la imagen
            x = self.redondear(float(w_total * mypart['start']) / mypart['cylinders'])
            if w == 0: w = 1
            # Busco la imagen de la partición correspondiente
            # TODO:la imagen debe corresponder al tipo de partición
            src = "data/particion/" + bar[i] + ".png"
            src_used = "data/particion/" + bar[i] + "_used.png"
            #src_borde = "data/particion/borde.png"
            
            #img_borde = Image.open(src_borde).resize((w, 80))
            #box_borde = (0, 0, w, 80)
            #region_borde = img_borde.crop(box_borde)
            
            w_used = (mypart['used'] * w) / mypart['blocks']
            #print w_used
            img_used = Image.open(src_used).resize((w_used, 80))
            box_used = (0, 0, w_used, 80)
            region_used = img_used.crop(box_used)
            
            im_total = Image.open(src).resize((w, 80))
            box = (0, 0, w, 80)
            region = im_total.crop(box)
            region.paste(region_used, box_used)
            #region.paste(region_borde, box_borde)
            box = (x, 0, w + x, 80)
            im_base.paste(region, box)
            i = i + 1
        #print '----------------------------------------------------------------'
        im_base.save('data/particion/base_mod.png')
        self.barra.set_from_file('data/particion/base_mod.png')
        
    def is_mounted(self, dev):
        #self.partitions[part]['path']
        cmd = "mount | grep {0}".format(dev)
        mount_output = commands.getoutput(cmd)
        return True if len(mount_output) > 0 else False
        
    def mount(self, dev):
        fold = dev.split('/')[1]
        cmd = "mkdir /tmp/{0} & mount {1} /tmp/{0}".format(fold, dev)
        mount_output = commands.getoutput(cmd)
        
    def espacios(self, dev):
        cmd = "df {0}".format(dev)
        espacios_output = commands.getoutput(cmd)
        #print '-- ESPACIOS INIT {0}--------------------------------'.format(dev)
        #print espacios_output.split('\n')[1].split(None, 5)
        #print '-- ESPACIOS END {0}---------------------------------'.format(dev)
        return espacios_output.split('\n')[1].split(None, 5)

    def redondear(self, w, dec=0):
        if dec == 0:
            return int(w) + 1 if int(str(w).split('.')[1][0]) >= 5 else int(w)
        else:
            return str(w).split('.')[0] + '.' + str(w).split('.')[1][0:dec]
    def list_install(self):
        self.lbl_info.set_text('{0} - {1} - {2}'.format(int(self.minimo / 1073741824), self.discos_total, self.minimo))
        self.cmb_dev.get_model().clear()
        if self.discos_total <= self.minimo:
            self.lbl_info.set_text('{0} - {1} - {2}\nEste disco no tiene suficiente espacio para realizar la instalación de Canaima GNU/Linux,\npor favor, seleccione un disco con una capacidad mínima de {0} GB' \
            .format(int(self.minimo / 1073741824), self.discos_total, self.minimo))
            return
        i = 0
        action = {}
        if self.is_mounted(self.discos) == False: self.mount(self.discos)
        langs = self.partitions.keys()
        #print len(self.partitions)
        langs.sort()
        action['0-all'] = 'Usar todo el disco (Recomendado)'
        for parts in langs:
            mypart = self.partitions[parts]
            part = self.espacios(mypart['path'])
            print part[1], part[2], int(part[1]) - int(part[2]), part[3]
            libre = float((int(part[1]) - int(part[2])) * 1024)
            if (libre) >= self.minimo:
                action[str(i) + mypart['path']] = \
                'Instalar en {0} ({1} GB de espacio libre)'. \
                format(mypart['path'], self.redondear((libre / 1073741824), 2))
                i = i + 1
        a = action.keys()
        a.sort()
        for x in a:
            self.cmb_dev.append_text(action[x])
        self.cmb_dev.set_active(0)
        
        
        
        
        
        
        
        
    ############################################################################
    def lista_discos(self):
        '''
            devuelve los discos que están conectados al equipo
        '''
        leer = False
        i = -1
        disks = []
        opt = {}
        a = commands.getstatusoutput("lshw -class disk")[1].split('\n')
        for disk in a:
            if disk[2:] == "*-disk":
                if i >= 0: 
                    disks.append(opt)
                    opt = {}
                i = i + 1
                leer = True
                continue
            if disk[2:9] == "*-cdrom":
                leer = False
                continue
            if leer == True:
                disk = disk[7:].split(': ')
                opt[disk[0]] = disk[1]
        disks.append(opt)
        self.img_partitions
        return disks
        
    def listar_particiones(self, disco):
        cmd = "parted {0} print free".format(disco)
        salida = commands.getstatusoutput().split('\n')
        print salida
        
        
        
        
        
        
        
