#-*- coding: UTF-8 -*-

import gtk

import clases.general as gen
import clases.particiones
import clases.particion_nueva as part_nueva
import clases.tabla_particiones
from clases import particiones

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

        #TODO: Revisar el por qué de esta sentencia, no asigna ni modifica nada
        float(gen.kb(gen.hum(data['fin']))),
        int(float(gen.kb(gen.hum(data['fin']))))

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
                       p_disp,
                       p_tipo + '',
                       p_format + '',
                       '', # Punto de montaje
                       gen.hum(gen.kb(p_tam)),
                       gen.kb(p_ini),
                       gen.kb(p_fin)
                   ]
                self.lista.append(fila)

            self.llenar_tabla(self.lista)

    def __init__(self, data):
        gtk.Fixed.__init__(self)
        self.iniciar(data)

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

    def llenar_tabla(self, data=None):
        if self.data['metodo'] == 'todo':
            self.primarias = 0
        else:
            for p in self.part.lista_particiones(self.disco):
                if p[4] == 'primary':
                    self.primarias = self.primarias + 1
        self.tabla.liststore.clear()
        assert isinstance(data, list) or isinstance(data, tuple)
        for fila in data:
            self.tabla.agregar_fila(fila)
            if fila[3] == '/':
                self.raiz = True
            if fila[1] == 'Primaria' or fila[1] == 'Extendida':
                self.primarias = self.primarias + 1
        print 'Particiones Primarias: ' + str(self.primarias)
        if len(data) == 1 and fila[1] == 'Espacio Libre':
            self.btn_deshacer.set_sensitive(False)
        else:
            self.btn_deshacer.set_sensitive(True)
        if self.bext == False and self.primarias == 4:
            self.btn_nueva.set_sensitive(False)
        elif fila[1] != 'Espacio Libre' and fila[1] != 'Espacio Libre Extendida':
            self.btn_nueva.set_sensitive(False)
        else:
            self.btn_nueva.set_sensitive(True)

    def particion_nueva(self, widget=None):
        part_nueva.Main(self)

    def deshacer(self, widget=None):
        if self.lista[0][1] == 'Espacio Libre':
            return False
        if self.lista[-1][1] == 'Espacio Libre':
            self.lista.pop()
        if self.lista[-1][1] == 'Espacio Libre Extendida':
            self.lista.pop()
        if self.lista[-1][1] == 'Lógica':
            self.bext = True
        else:
            self.bext = False

        tipo = self.lista[-1][1]
        fin = self.lista[-1][6]

        self.lista.pop()

        if tipo == 'Extendida':
            inicio = self.ext_ini
            fin = self.ext_fin
        elif tipo == 'Lógica' and self.bext == True:
            if self.lista[-1][1] == 'Extendida':
                inicio = self.lista[-1][5]
            else:
                inicio = self.lista[-1][6]
            fin = self.ext_fin
        elif tipo == 'Primaria':
            try:
                inicio = self.lista[-1][6]
            except:
                inicio = gen.kb(self.ini)
            fin = gen.kb(self.fin)

        if self.bext == True:
            tamano = gen.hum(fin - inicio)
            particion = [self.disco, #Dispositivo
                         'Espacio Libre Extendida', #Formato
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
                         'Espacio Libre', #Formato
                         '', #Tipo
                         '', #Punto de montaje
                         tamano, #Tamaño
                         inicio, #inicio
                         fin]               #fin
            self.lista.append(particion)

        self.llenar_tabla(self.lista)

