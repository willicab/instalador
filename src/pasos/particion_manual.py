#-*- coding: UTF-8 -*-

import pygtk
pygtk.require('2.0')
import gtk

import clases.general as gen
import clases.particiones
import clases.barra_manual as barra
import clases.particion_nueva as part_nueva
import clases.tabla_particiones

class Main(gtk.Fixed):
    part = clases.particiones.Main()
    ini = 0             #Inicio de la partición
    fin = 0             #Fin de la partición
    lista = []          #Lista de las particiones hechas
    primarias = 0       #Cuenta la cantidad de particiones primarias
    # Si se crea una partición extendida se usarán las siguientes variables
    bext = False        #Si se crea la partición extendida será True
    ext_ini = 0         #El inicio de la partición extendida
    ext_fin = 0         #El fin de la partición extendida
    def __init__(self, data):
        gtk.Fixed.__init__(self)
        data = data[0]
        self.disco = data['disco'] if data['disco'] != '' \
                     else data['particion'][:-1]
        
        if data['metodo'] != 'todo' and data['metodo'] != 'vacio' :
            self.ini = data['nuevo_fin']
        else:
            self.ini = 1049                          # Inicio de la partición
        if data['fin'][-2:] != 'kB':
            data['fin'] = data['fin'] + 'kB'
        self.fin = data['fin']
        print data['metodo'], self.ini, self.fin
        
        for p in self.part.lista_particiones(self.disco):
            print p[4]
            if p[4] == 'primary':
                self.primarias = self.primarias + 1
        
        self.tabla = clases.tabla_particiones.TablaParticiones()
        #self.tabla.set_doble_click(self.activar_tabla);
        #self.tabla.set_seleccionar(self.seleccionar_tabla)
        
        self.scroll = gtk.ScrolledWindow()
        self.scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        self.scroll.set_size_request(590, 240)
        self.scroll.add(self.tabla)
        self.put(self.scroll, 0, 0)
        self.tabla.show()
        self.scroll.show()

        self.btn_nueva = gtk.Button("Crear Nueva Partición")
        self.btn_nueva.set_size_request(200, 30)
        self.btn_nueva.show()
        self.put(self.btn_nueva, 0, 245)
        self.btn_nueva.connect("clicked", self.particion_nueva)

        self.btn_deshacer = gtk.Button("Deshacer Accion")
        self.btn_deshacer.set_size_request(160, 30)
        self.btn_deshacer.show()
        self.put(self.btn_deshacer, 205, 245)
        self.btn_deshacer.connect("clicked", self.deshacer)
        
        tamano = gen.hum(gen.kb(self.fin) - gen.kb(self.ini))
        inicio = gen.kb(self.ini)
        fin = gen.kb(self.fin)
        libre = [self.disco,          #Dispositivo
                 'Espacio Libre', #Tipo
                 '',                        #Formato
                 '',                        #Punto de montaje
                 tamano,                    #Tamaño
                 inicio,                    #inicio
                 fin]                       #fin
        self.lista.append(libre)

        self.llenar_tabla(self.lista)

    def llenar_tabla(self, data=None):
        self.tabla.liststore.clear()
        assert isinstance(data, list) or isinstance(data, tuple)
        for fila in data:
            self.tabla.agregar_fila(fila)
        print fila
        if len(data) == 1 and fila[1] == 'Espacio Libre':
            self.btn_deshacer.set_sensitive(False)
        else:
            self.btn_deshacer.set_sensitive(True)
        if self.bext == False  and self.primarias == 4:
            self.btn_nueva.set_sensitive(False)
        elif fila[1] != 'Espacio Libre' and fila[1] != 'Espacio Libre Extendida':
            self.btn_nueva.set_sensitive(False)
        else:
            self.btn_nueva.set_sensitive(True)
        
        #print self.primarias

    def particion_nueva(self, widget=None):
        win = part_nueva.Main(self)

    def deshacer(self, widget=None):
        
        if self.lista[-1][1] == 'Espacio Libre':
            self.lista.pop() # Elimino la particion libre, de existir
        if len(self.lista)>0:
            if self.lista[-1][1] == 'Espacio Libre Extendida':
                self.lista.pop() # Elimino la particion libre extendida, de existir
            self.bext = False
            self.lista.pop()
            if len(self.lista)>0:
                if self.lista[-1][1] == 'Extendida' or self.lista[-1][1] == 'Lógica':
                    self.bext = True
                    print "estableciendo bext a true"
        #print self.lista[-1][1]
        if self.lista[-1][1] == 'Primaria' or self.lista[-1][1] == 'Extendida':
            self.primarias = self.primarias - 1
        #print self.bext, self.lista
        #Si bext = True entonces
        if self.bext == True:
            # calculo el tamaño de la particion libre extendida
            inicio = int(self.lista[-1][-1])
            fin = int(self.ext_fin)
            print "Inicio-Fin:", inicio, fin
            tamano = gen.hum(fin - inicio)
            if inicio != fin or self.lista[-1][1] == 'Extendida':
                particion = [self.disco,        #Dispositivo
                             'Espacio Libre Extendida',#Formato
                             '',                #Tipo
                             '',                #Punto de montaje
                             tamano,                #Tamaño
                             inicio,            #inicio
                             fin]               #fin
                self.lista.append(particion)
                print "Creado Espacio Libre Extendida"
        
        # calculo el tamaño de la particion libre
        if len(self.lista)==0:
            inicio = int(gen.kb(self.ini))
        else:
            inicio = int(self.lista[-1][-1])
        fin = int(gen.kb(self.fin))
        tamano = gen.hum(fin - inicio)
        if inicio != fin:
            particion = [self.disco,        #Dispositivo
                         'Espacio Libre',   #Formato
                         '',                #Tipo
                         '',                #Punto de montaje
                         tamano,                #Tamaño
                         inicio,            #inicio
                         fin]               #fin
            self.lista.append(particion)
            print "Creado Espacio Libre"
        
        self.llenar_tabla(self.lista)
        print "cantidad de elementos: ", len(self.lista), self.lista
