#-*- coding: UTF-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
import clases.general as gen

class Main(gtk.Dialog): 
    inicio = 0
    fin = 0
    def __init__(self, padre):
        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        gtk.Window.set_position(self, gtk.WIN_POS_CENTER_ALWAYS)
        self.set_title("Nueva Partición")
        self.padre = padre
        self.set_size_request(400, 200)
        self.set_resizable(0)
        self.set_border_width(0)
        
        self.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        self.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        self.set_default_response(gtk.RESPONSE_CANCEL)
        
        if self.padre.bext == False:
            self.inicio = gen.kb(self.padre.lista[-1][5])
            self.fin = gen.kb(self.padre.fin)
        else:
            self.inicio = gen.kb(self.padre.ext_ini)
            self.fin = gen.kb(self.padre.ext_fin)
        
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
        self.lblsize = gtk.Label(gen.hum(self.escala.get_value() - \
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
        if padre.bext == True:
            self.cmb_tipo.append_text('Lógica')
            self.cmb_tipo.set_sensitive(False)
        else:
            #if self.padre.primarias < 4:
            self.cmb_tipo.append_text('Primaria')
            self.cmb_tipo.append_text('Extendida')
        self.cmb_tipo.set_active(0)
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
        self.cmb_fs.append_text('linux-swap')
        self.cmb_fs.append_text('reiserfs')
        self.cmb_fs.append_text('fat16')
        self.cmb_fs.append_text('fat32')
        self.cmb_fs.set_active(2)
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
        self.agregar('/tmp')
        self.agregar('/usr')
        self.agregar('/var')
        self.agregar('/srv')
        self.agregar('/opt')
        self.agregar('/usr/local')
        self.cmb_montaje.append_text('Ninguno')
        self.cmb_montaje.append_text('Escoger manualmente')
        self.cmb_montaje.set_active(0)
        self.cmb_montaje.connect("changed", self.cmb_montaje_on_changed)
        self.cmb_montaje.show()

        self.entrada = gtk.Entry()
        self.entrada.set_text('/')
        self.entrada.set_size_request(200, 30)
        self.cont.put(self.entrada, 145, 125)
        self.entrada.connect("changed", self.validar_punto)

        response = self.run()
        
        if response==gtk.RESPONSE_OK:
            tipo = gen.get_active_text(self.cmb_tipo)
            formato = gen.get_active_text(self.cmb_fs)
            montaje = gen.get_active_text(self.cmb_montaje)
            if tipo == 'Extendida':
                formato = 'Ninguno'
                montaje = 'Ninguno'
            if formato == 'linux-swap':
                montaje = 'Ninguno'
            if montaje == 'Escoger manualmente':
                montaje = self.entrada.get_text().strip()
            
            if self.padre.lista[-1][1] == 'Espacio Libre':
                self.padre.lista.pop()
            if len(self.padre.lista)>0:
                if self.padre.lista[-1][1] == 'Espacio Libre Extendida':
                    self.padre.lista.pop()
            
            # Si la partición nueva es Primaria
            if tipo == 'Primaria':
                # Calculo el tamaño
                inicio = int(self.inicio)
                fin = int(self.escala.get_value())
                tamano = gen.hum(fin - inicio)
                # Elimina ultimo elemento de la lista
                #self.padre.lista.pop()
                # Se crea elemento particion primaria y se agrega a la lista
                particion = [self.padre.disco,  #Dispositivo
                             tipo,              #Tipo
                             formato,           #Formato
                             montaje,           #Punto de montaje
                             tamano,            #Tamaño
                             inicio,            #inicio
                             fin]               #fin
                self.padre.lista.append(particion)
                self.padre.primarias = self.padre.primarias + 1
            # Si la partición nueva es Extendida
            elif tipo == 'Extendida':
                # Calculo el tamaño
                inicio = int(self.inicio)
                fin = int(self.escala.get_value())
                tamano = gen.hum(fin - inicio)
                # Cambia variable bext a True
                self.padre.bext = True
                # Establece las variables ext_ini y ext_fin
                self.padre.ext_ini = inicio
                self.padre.ext_fin = fin
                # Elimina ultimo elemento de la lista
                #self.padre.lista.pop()
                # Se crea elemento particion extendida y se agrega a la lista
                particion = [self.padre.disco,  #Dispositivo
                             tipo,              #Tipo
                             '',                #formato,     #Formato
                             montaje,           #Punto de montaje
                             tamano,            #Tamaño
                             inicio,            #inicio
                             fin]               #fin
                self.padre.lista.append(particion)
                # Se crea elemento espacio libre en partición extendida
                particion = ['',#self.padre.disco,                      #Dispositivo
                             'Espacio Libre Extendida',   #Tipo
                             '',#self.get_active_text(self.cmb_fs),     #Formato
                             '',#self.get_active_text(self.cmb_montaje),#Punto de montaje
                             tamano,                                #Tamaño
                             inicio,                                #inicio
                             fin]                                   #fin
                self.padre.lista.append(particion)
                self.padre.primarias = self.padre.primarias + 1
            # Si la partición nueva es Lógica
            elif tipo == 'Lógica':
                # Calculo el tamaño
                inicio = int(self.padre.ext_ini)
                fin = int(self.escala.get_value())
                tamano = gen.hum(fin - inicio)
                # Elimina los dos ultimos elementos de la lista
                #self.padre.lista.pop()
                #self.padre.lista.pop()
                # Se crea elemento particion lógica y se agrega a la lista
                particion = [self.padre.disco,  #Dispositivo
                             tipo,              #Tipo
                             formato,           #Formato
                             montaje,           #Punto de montaje
                             tamano,            #Tamaño
                             inicio,            #inicio
                             fin]               #fin
                self.padre.lista.append(particion)
                # Si self.padre.ext_fin != fin entonces
                if self.padre.ext_fin == fin:
                    # No se crea elemento espacio libre en partición extendida
                    # Cambia variable bext a False
                    self.padre.bext = False
                # Si no
                else:
                    # se calcula el tamaño de la partición libre
                    ext_ini = fin
                    ext_fin = self.padre.ext_fin
                    tamano = gen.hum(ext_fin - ext_ini)
                    self.padre.ext_ini = ext_ini
                    # Se crea elemento espacio libre en partición extendida
                    particion = ['',#self.padre.disco,                      #Dispositivo
                                 'Espacio Libre Extendida',   #Tipo
                                 '',#self.get_active_text(self.cmb_fs),     #Formato
                                 '',#self.get_active_text(self.cmb_montaje),#Punto de montaje
                                 tamano,                                #Tamaño
                                 ext_ini,                                #inicio
                                 ext_fin]                                   #fin
                    self.padre.lista.append(particion)
                    
            # Calculamos el tamaño de la partición libre
            # si bext == True entonces se usará ext_fin como fin
            if self.padre.bext == True: 
                fin = self.padre.ext_fin
            #print 'Inicio:', inicio, 'fin:', fin, "self.fin", int(self.fin)
            # Si fin == self.fin entonces 
            if fin == int(gen.kb(self.padre.fin)):
                pass
                # No se crea elemento espacio libre
                #print "No crea la elemento espacio libre"
            # Si no
            else:
                #print "Crea elemento espacio libre"
                # se calcula el tamaño de la partición libre
                inicio = fin
                fin = int(gen.kb(self.padre.fin))
                tamano = gen.hum(fin - inicio)
                # Se crea elemento espacio libre
                libre = ['',                #Dispositivo
                         'Espacio Libre',   #Tipo
                         '',                #Formato
                         '',                #Punto de montaje
                         tamano,            #Tamaño
                         inicio,            #inicio
                         fin]               #fin
                self.padre.lista.append(libre)
            # Se actualiza la tabla
            self.padre.llenar_tabla(self.padre.lista)
                
        else:
            pass
        
        self.destroy()
        return None

    def on_changed(self, widget=None):
        self.lblsize.set_text(gen.hum(widget.get_value() - float(self.inicio)))
        
    def cmb_tipo_on_changed(self, widget=None):
        pass
    
    def cmb_tipo_on_changed(self, widget=None):
        tipo = gen.get_active_text(self.cmb_tipo)
        if tipo == 'Extendida':
            self.cmb_fs.set_sensitive(False)
            self.cmb_montaje.set_sensitive(False)
        else:
            self.cmb_fs.set_sensitive(True)
            self.cmb_montaje.set_sensitive(True)

    def cmb_fs_on_changed(self, widget=None):
        fs = gen.get_active_text(self.cmb_fs)
        if fs == 'linux-swap':
            self.cmb_montaje.set_sensitive(False)
        else:
            self.cmb_montaje.set_sensitive(True)

    def cmb_montaje_on_changed(self, widget=None):
        montaje = gen.get_active_text(self.cmb_montaje)
        if montaje == 'Escoger manualmente':
            self.entrada.show()
            self.validar_punto()
        else:
            self.entrada.hide()
            self.set_response_sensitive(gtk.RESPONSE_OK, True)
    
    def agregar(self, punto):
        data = self.padre.lista
        aparece = False
        assert isinstance(data, list) or isinstance(data, tuple)
        for fila in data:
            if fila[3] == punto:
                aparece = True
        if aparece == False:
            self.cmb_montaje.append_text(punto)
            
    def validar_punto(self, widget=None):
        data = self.padre.lista
        aparece = False
        assert isinstance(data, list) or isinstance(data, tuple)
        for fila in data:
            if fila[3] == self.entrada.get_text().strip():
                aparece = True
        if aparece == False:
            self.set_response_sensitive(gtk.RESPONSE_OK, True)
        else:
            self.set_response_sensitive(gtk.RESPONSE_OK, False)
