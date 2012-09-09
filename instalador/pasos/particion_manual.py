#-*- coding: UTF-8 -*-

import gtk

import instalador.clases.general as gen
import instalador.clases.particion_nueva as part_nueva
import instalador.clases.tabla_particiones
from instalador.clases import particiones

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

        self.tabla = instalador.clases.tabla_particiones.TablaParticiones()
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

            self.llenar_tabla()

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


    def llenar_tabla(self):
        '''Llena la tabla con las particiones existentes en el disco'''

        # Ordena la lista por inicio de la particion
        self.ordenar_lista()

        # Limpia previamente la tabla para inicializar su llenado
        self.tabla.liststore.clear()

        # LLena la tabla con los datos
        for fila in self.lista:
            self.tabla.agregar_fila(fila)

            # Verifica si hay punto de montaje raiz "/"
            if fila[3] == '/':
                self.raiz = True

            # Cuenta las particiones primarias
            if fila[1] == msj.particion.primaria or fila[1] == \
            msj.particion.extendida:
                self.primarias = self.primarias + 1

    def ordenar_lista(self):
        tamano = len(self.lista)
        for i in range(tamano):
            i = i # Solo para quitar el warning (unused variable)
            for k in range(tamano - 1):
                ini = self.lista[k][5]
                ini_sig = self.lista[k + 1][5]
                if ini > ini_sig:
                    f_temp = self.lista[k]
                    self.lista[k] = self.lista[k + 1]
                    self.lista[k + 1] = f_temp


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

        self.inicializar(self.data)

