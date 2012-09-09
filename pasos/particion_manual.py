#-*- coding: UTF-8 -*-

import gtk

import clases.general as gen
import clases.particion_nueva as part_nueva
import clases.tabla_particiones
from clases import particiones

class msj:
    'Clase para administrar los mensajes mostrados al usuario'

    class particion:
        'Mensajes relacionados a las particiones'

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

            return tipo

        @classmethod
        def get_formato(self, formato):
            if formato == 'free':           return self.libre
            if formato == 'extended':     return ''

            return formato

        @classmethod
        def get_dispositivo(self, disp, num):
            if num == -1:       return ''

            return disp

    class gui:
        'Mensajes mostrados en la gui'

        btn_part_nueva = 'Crear Nueva Partición'
        btn_part_eliminar = 'X'
        btn_deshacer = 'Deshacer Acciones'

class Main(gtk.Fixed):

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

        # btn_eliminar
        self.btn_eliminar = gtk.Button(msj.gui.btn_part_eliminar)
        #self.btn_nueva.set_size_request(200, 30)
        self.btn_eliminar.show()
        self.put(self.btn_eliminar, 365, 245)
        self.btn_eliminar.connect("clicked", self.particion_eliminar)

        # btn_nueva
        self.btn_nueva = gtk.Button(msj.gui.btn_part_nueva)
        self.btn_nueva.set_size_request(200, 30)
        self.btn_nueva.show()
        self.put(self.btn_nueva, 0, 245)
        self.btn_nueva.connect("clicked", self.particion_nueva)

        # btn_deshacer
        self.btn_deshacer = gtk.Button(msj.gui.btn_deshacer)
        self.btn_deshacer.set_size_request(160, 30)
        self.btn_deshacer.show()
        self.put(self.btn_deshacer, 205, 245)
        self.btn_deshacer.connect("clicked", self.deshacer)

        # llenar la tabla por primera vez
        self.inicializar(data)

    def inicializar(self, data):
        '''
        Inicializa todas las variables
        '''

        self.data = data

        self.ini = 0             #Inicio de la partición
        self.fin = 0             #Fin de la partición
        self.lista = []          #Lista de las particiones hechas
        self.primarias = 0       #Cuenta la cantidad de particiones primarias
        self.raiz = False

        # Si se crea una partición extendida se usarán las siguientes variables
        self.bext = False        #Si se crea la partición extendida será True
        self.ext_ini = 0         #El inicio de la partición extendida
        self.ext_fin = 0         #El fin de la partición extendida

        self.acciones = []      # Almacena las acciones pendientes a realizar
        self.fila_selec = None  # Ultima fila seleccionada de la tabla


        self.lista = []
        self.disco = data['disco']
        self.ini = data['inicio']
        self.fin = data['fin']

#===============================================================================
#        if data['metodo'] != 'todo' and data['metodo'] != 'vacio':
#            self.ini = data['nuevo_fin']
#        else:
#            self.ini = 1049                            # Inicio de la partición
# 
#        if str(data['fin'])[-2:] != 'kB':
#            data['fin'] = str(data['fin']) + 'kB'
# 
#        self.fin = int(float(gen.kb(gen.hum(data['fin']))))
# 
#        if str(data['fin'])[-2:] != 'kB':
#            data['fin'] = str(data['fin']) + 'kB'
#===============================================================================

        # Llevar los botones a su estado inicial
        self.btn_eliminar.set_sensitive(False)
        self.btn_nueva.set_sensitive(False)

        # Llenar la tabla con el contenido actual del disco
        if self.tabla != None:

            l_part = particiones.Main().lista_particiones(self.disco)
            for particion in l_part:
                p_disp = particion[0]
                p_ini = particion[1]
                p_fin = particion[2]
                p_tam = particion[3]
                p_format = particion[4]
                p_tipo = particion[5]
                p_num = particion[10]

                fila = [
                       msj.particion.get_dispositivo(p_disp, p_num),
                       msj.particion.get_tipo(p_tipo),
                       msj.particion.get_formato(p_format),
                       '', # Punto de montaje
                       gen.hum(gen.kb(p_tam)),
                       gen.kb(p_ini),
                       gen.kb(p_fin)
                   ]
                self.lista.append(fila)

            self.llenar_tabla(self.lista)

    def seleccionar_fila(self, fila):
        '''Acciones a tomar cuando una fila de la tabla es seleccionada'''

        self.fila_selec = fila

        #TODO: Impedir crear nuevas si hay mas de 4 primarias y 0 extendidas
        # BTN_NUEVA
        if fila[2] == msj.particion.libre or fila[2] == \
        msj.particion.extendida_libre:
            self.btn_nueva.set_sensitive(True)
        else:
            self.btn_nueva.set_sensitive(False)

        # Solo se pueden eliminar particiones, no espacios libres
        # BTN_ELIMINAR
        if fila[2] != msj.particion.libre and fila[2] != \
        msj.particion.extendida_libre:
            self.btn_eliminar.set_sensitive(True)
        else:
            self.btn_eliminar.set_sensitive(False)


    def llenar_tabla(self, data=None):
        '''Llena la tabla con las particiones existentes en el disco'''
        assert isinstance(data, list) or isinstance(data, tuple)

        # Limpia previamente la tabla para inicializar su llenado
        self.tabla.liststore.clear()

        # LLena la tabla con los datos de "data"
        for fila in data:
            self.tabla.agregar_fila(fila)

            # Verifica si hay punto de montaje raiz "/"
            if fila[3] == '/':
                self.raiz = True

            # Cuenta las particiones primarias
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

        #=======================================================================
        # if self.bext == False and self.primarias == 4:
        #    # impide crear una nueva particion si hay 4 primarias y 0 extendidas
        #    self.btn_nueva.set_sensitive(False)
        # elif fila[1] != msj.particion.libre and fila[1] != \
        # msj.particion.extendida_libre:
        #    # impide crear una nueva particion si no hay espacios libres
        #    self.btn_nueva.set_sensitive(False)
        # else:
        #    # Permite crear una particion nueva
        #    self.btn_nueva.set_sensitive(True)
        #=======================================================================

    def agregar_a_lista(self, fila):
        '''Agrega una nueva particion a la lista en el sitio adecuado segun su
        inicio'''

        i = 0
        temp = []
        inicio = fila[5]
        agregado = False

        for f in self.lista:
            temp.append(f)

            if len(self.lista) > i + 1 and not agregado:
                ini_anterior = f[5]
                ini_siguiente = self.lista[i + 1][5]
                if inicio >= ini_anterior and inicio < ini_siguiente:
                    temp.pop()
                    temp.append(fila)
                    agregado = True
            elif not agregado:
                temp.pop()
                temp.append(fila)

            i = i + 1
        self.lista = temp

    #TODO: Implementar
    def particion_eliminar(self, widget=None):

        fila_accion = (
                        'eliminar',
                        self.tabla.ultima_fila_seleccionada
                     )
        print fila_accion

        self.acciones.append(fila_accion)


    def particion_nueva(self, widget=None):
        part_nueva.Main(self)

    def deshacer(self, widget=None):
#===============================================================================
#        if self.lista[0][1] == msj.particion.libre:
#            return False
#        if self.lista[-1][1] == msj.particion.libre:
#            self.lista.pop()
#        if self.lista[-1][1] == msj.particion.extendida_libre:
#            self.lista.pop()
#        if self.lista[-1][1] == msj.particion.logica:
#            self.bext = True
#        else:
#            self.bext = False
# 
#        tipo = self.lista[-1][1]
#        fin = self.lista[-1][6]
# 
#        self.lista.pop()
# 
#        if tipo == msj.particion.extendida:
#            inicio = self.ext_ini
#            fin = self.ext_fin
#        elif tipo == msj.particion.logica and self.bext == True:
#            if self.lista[-1][1] == msj.particion.extendida:
#                inicio = self.lista[-1][5]
#            else:
#                inicio = self.lista[-1][6]
#            fin = self.ext_fin
#        elif tipo == msj.particion.primaria:
#            try:
#                inicio = self.lista[-1][6]
#            except:
#                inicio = gen.kb(self.ini)
#            fin = gen.kb(self.fin)
# 
#        if self.bext == True:
#            tamano = gen.hum(fin - inicio)
#            particion = [self.disco, #Dispositivo
#                         msj.particion.extendida_libre, #Formato
#                         '', #Tipo
#                         '', #Punto de montaje
#                         tamano, #Tamaño
#                         inicio, #inicio
#                         fin]                       #fin
#            self.lista.append(particion)
# 
# 
#        if fin != self.fin:
#            try:
#                inicio = self.lista[-1][6]
#            except:
#                inicio = gen.kb(self.ini)
#            fin = gen.kb(self.fin)
#            tamano = gen.hum(fin - inicio)
#            particion = [self.disco, #Dispositivo
#                         msj.particion.libre, #Formato
#                         '', #Tipo
#                         '', #Punto de montaje
#                         tamano, #Tamaño
#                         inicio, #inicio
#                         fin]               #fin
#            self.lista.append(particion)
#===============================================================================

        self.inicializar(self.data)

