#-*- coding: UTF-8 -*-

import gtk

import clases.general as gen
import clases.particiones
import clases.particion_nueva as part_nueva
import clases.tabla_particiones
from clases import particiones

class msj:
    class particion:
        libre = 'Espacio Libre'
        primaria = 'Primaria'
        extendida = 'Extendida'
        logica = 'Lógica'
        extendida_libre = 'Espacio Libre Extendida'

        @classmethod
        def get_tipo(self, tipo):
            if tipo == 'free':      return self.libre
            if tipo == 'primary':   return self.primaria
            if tipo == 'extended':  return self.extendida
            if tipo == 'logical':   return self.logica

        @classmethod
        def get_formato(self, formato):
            if formato == 'free':           return ''
            elif formato == 'extended':     return ''
            else:                           return formato

        @classmethod
        def get_dispositivo(self, disp):
            print "disp=", disp
            if disp == 0:       return ''
            else:               return disp

    class gui:
        btn_part_nueva = 'Crear Nueva Partición'
        btn_part_eliminar = 'X'
        btn_deshacer = 'Deshacer Acción'

class Main(gtk.Fixed):
    part = clases.particiones.Main()
    ini = 0             #Inicio de la partición
    fin = 0             #Fin de la partición
    lista = []          #Lista de las particiones hechas
    primarias = 0       #Cuenta la cantidad de particiones primarias
    raiz = False
    tabla = None
    # Si se crea una partición extendida se usarán las siguientes variables
    bext = False        #Si se crea la partición extendida será True
    ext_ini = 0         #El inicio de la partición extendida
    ext_fin = 0         #El fin de la partición extendida

    acciones = {}

    def iniciar(self, data):
        '''
        Inicia el llenado de la tabla
        '''

        self.data = data
        self.lista = []
        self.disco = data['disco'] if data['disco'] != '' \
                     else data['particion'][:-1]

        if data['metodo'] != 'todo' and data['metodo'] != 'vacio':
            self.ini = data['nuevo_fin']
        else:
            self.ini = 1049                            # Inicio de la partición

        if str(data['fin'])[-2:] != 'kB':
            data['fin'] = str(data['fin']) + 'kB'

        self.fin = int(float(gen.kb(gen.hum(data['fin']))))

        if str(data['fin'])[-2:] != 'kB':
            data['fin'] = str(data['fin']) + 'kB'

        self.fin = data['fin']

        if self.tabla != None:

            l_part = particiones.Main().lista_particiones(self.disco)
            for particion in l_part:
                p_disp = particion[0]
                p_ini = particion[1]
                p_fin = particion[2]
                p_tam = particion[3]
                p_format = particion[4]
                p_tipo = particion[5]

                fila = [
                       msj.particion.get_dispositivo(p_disp),
                       msj.particion.get_tipo(p_tipo),
                       msj.particion.get_formato(p_format),
                       '', # Punto de montaje
                       gen.hum(gen.kb(p_tam)),
                       gen.kb(p_ini),
                       gen.kb(p_fin)
                   ]
                self.lista.append(fila)

            self.llenar_tabla(self.lista)

    def __init__(self, data):
        gtk.Fixed.__init__(self)

        self.tabla = clases.tabla_particiones.TablaParticiones()
        #self.tabla.set_doble_click(self.activar_tabla);
        self.tabla.set_seleccionar(self.seleccionar_fila)

        self.scroll = gtk.ScrolledWindow()
        self.scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        self.scroll.set_size_request(690, 240)
        self.scroll.add(self.tabla)
        self.put(self.scroll, 0, 0)
        self.tabla.show()
        self.scroll.show()

        self.btn_eliminar = gtk.Button("X")
        self.btn_eliminar.set_sensitive(False)
        #self.btn_nueva.set_size_request(200, 30)
        self.btn_eliminar.show()
        self.put(self.btn_eliminar, 365, 245)
        self.btn_eliminar.connect("clicked", self.particion_eliminar)

        self.btn_nueva = gtk.Button(msj.gui.btn_part_nueva)
        self.btn_nueva.set_size_request(200, 30)
        self.btn_nueva.show()
        self.put(self.btn_nueva, 0, 245)
        self.btn_nueva.connect("clicked", self.particion_nueva)

        self.btn_deshacer = gtk.Button(msj.gui.btn_deshacer)
        self.btn_deshacer.set_size_request(160, 30)
        self.btn_deshacer.show()
        self.put(self.btn_deshacer, 205, 245)
        self.btn_deshacer.connect("clicked", self.deshacer)

        self.iniciar(data)

    def seleccionar_fila(self, fila):
        '''Acciones a tomar cuando una fila de la tabla es seleccionada'''

        # Solo se pueden eliminar particiones, no espacios libres
        if fila[1] != msj.particion.libre and fila[1] != \
        msj.particion.extendida_libre:
            self.btn_eliminar.set_sensitive(True)
        else:
            self.btn_eliminar.set_sensitive(False)


    def llenar_tabla(self, data=None):
        '''Llena la tabla con las particiones existentes en el disco'''
        assert isinstance(data, list) or isinstance(data, tuple)

        # Limpia previamente la tabla para iniciar su llenado
        self.tabla.liststore.clear()

        # Contabiliza las particiones primarias para evitar que sean mayor a 4
        for p in self.part.lista_particiones(self.disco):
            if p[4] == 'primary':
                self.primarias = self.primarias + 1

        # LLena la tabla con los datos de "data"
        for fila in data:
            self.tabla.agregar_fila(fila)

            # Validaciones
            if fila[3] == '/':
                self.raiz = True
            if fila[1] == msj.particion.primaria or fila[1] == \
            msj.particion.extendida:
                self.primarias = self.primarias + 1

        #=======================================================================
        # # Desactiva el boton deshacer si en el disco hay sólo un espacio libre
        # if len(data) == 1 and fila[1] == msj.particion.libre:
        #   self.btn_deshacer.set_sensitive(False)
        # else:
        #   self.btn_deshacer.set_sensitive(True)
        #=======================================================================

        if self.bext == False and self.primarias == 4:
            # impide crear una nueva particion si hay 4 primarias y 0 extendidas
            self.btn_nueva.set_sensitive(False)
        elif fila[1] != msj.particion.libre and fila[1] != \
        msj.particion.extendida_libre:
            # impide crear una nueva particion si no hay espacios libres
            self.btn_nueva.set_sensitive(False)
        else:
            # Permite crear una particion nueva
            self.btn_nueva.set_sensitive(True)

    #TODO: Implementar
    def particion_eliminar(self, widget=None):
        print 'Eliminar partición:', self.tabla.ultima_fila_seleccionada[0]

    def particion_nueva(self, widget=None):
        part_nueva.Main(self)

    def deshacer(self, widget=None):
        if self.lista[0][1] == msj.particion.libre:
            return False
        if self.lista[-1][1] == msj.particion.libre:
            self.lista.pop()
        if self.lista[-1][1] == msj.particion.extendida_libre:
            self.lista.pop()
        if self.lista[-1][1] == msj.particion.logica:
            self.bext = True
        else:
            self.bext = False

        tipo = self.lista[-1][1]
        fin = self.lista[-1][6]

        self.lista.pop()

        if tipo == msj.particion.extendida:
            inicio = self.ext_ini
            fin = self.ext_fin
        elif tipo == msj.particion.logica and self.bext == True:
            if self.lista[-1][1] == msj.particion.extendida:
                inicio = self.lista[-1][5]
            else:
                inicio = self.lista[-1][6]
            fin = self.ext_fin
        elif tipo == msj.particion.primaria:
            try:
                inicio = self.lista[-1][6]
            except:
                inicio = gen.kb(self.ini)
            fin = gen.kb(self.fin)

        if self.bext == True:
            tamano = gen.hum(fin - inicio)
            particion = [self.disco, #Dispositivo
                         msj.particion.extendida_libre, #Formato
                         '', #Tipo
                         '', #Punto de montaje
                         tamano, #Tamaño
                         inicio, #inicio
                         fin]                       #fin
            self.lista.append(particion)


        if fin != self.fin:
            try:
                inicio = self.lista[-1][6]
            except:
                inicio = gen.kb(self.ini)
            fin = gen.kb(self.fin)
            tamano = gen.hum(fin - inicio)
            particion = [self.disco, #Dispositivo
                         msj.particion.libre, #Formato
                         '', #Tipo
                         '', #Punto de montaje
                         tamano, #Tamaño
                         inicio, #inicio
                         fin]               #fin
            self.lista.append(particion)

        self.llenar_tabla(self.lista)

