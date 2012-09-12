#-*- coding: UTF-8 -*-

import gtk

from canaimainstalador.clases.common import floatify, humanize
import canaimainstalador.clases.particion_nueva as part_nueva
from canaimainstalador.clases.tabla_particiones import TablaParticiones
from canaimainstalador.clases.particiones import Particiones
from canaimainstalador.translator import msj

class PasoPartManual(gtk.Fixed):

    def __init__(self, data):
        gtk.Fixed.__init__(self)

        self.tabla = TablaParticiones()
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

            l_part = Particiones().lista_particiones(self.disco)
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
                       humanize(floatify(p_tam)),
                       floatify(p_ini),
                       floatify(p_fin)
                   ]
                self.lista.append(fila)

            self.llenar_tabla()

    def seleccionar_fila(self, fila):
        '''Acciones a tomar cuando una fila de la tabla es seleccionada'''

        self.fila_selec = fila

        # Es particion extendida?
        if fila[1] == msj.particion.extendida:
            self.bext = True
        else:
            self.bext = False

        # BTN_NUEVA
        if fila[2] == msj.particion.libre:
            # Activar solo si hay menos de 4 particiones primarias
            if self.contar_primarias() < 4:
                self.btn_nueva.set_sensitive(True)
            # o si la part. libre pertenece a una part. extendida
            elif fila[1] == msj.particion.extendida:
                self.btn_nueva.set_sensitive(True)
        else:
            self.btn_nueva.set_sensitive(False)

        # Solo se pueden eliminar particiones, no espacios libres
        # BTN_ELIMINAR
        if fila[2] != msj.particion.libre:
            self.btn_eliminar.set_sensitive(True)
        else:
            self.btn_eliminar.set_sensitive(False)

    def contar_primarias(self):
        '''Cuenta la cantidad de particiones primarias. Las particiones
        extendidas cuentan como primarias'''
        total = 0
        for fila in self.lista:
            # Los espacios libres no se cuentan
            if fila[2] == msj.particion.libre:
                continue
            # Si es una particion extendida
            if fila[1] == msj.particion.extendida:
                total = total + 1
            # Si la particion es primaria
            elif fila[1] == msj.particion.primaria:
                total = total + 1

        return total

    def existe_extendida(self):
        'Determina si existe por lo menos una particion extandida'
        for fila in self.lista:
            if fila[1] == msj.particion.extendida:
                return True
        return False


    def llenar_tabla(self):
        '''Llena la tabla con las particiones existentes en el disco'''

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
        'Ordena la lista por el inicio de la particion'
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


    def agregar_a_lista(self, fila, pop=True):
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

                    if pop: temp.pop()
                    temp.append(fila)
                    agregado = True

            elif not agregado:
                if pop: temp.pop()
                temp.append(fila)

            i = i + 1
        self.lista = temp

    #TODO: Implementar
    def particion_eliminar(self, widget=None):

        widget.set_sensitive(False)

        fila_accion = (
                        'eliminar',
                        self.tabla.ultima_fila_seleccionada
                     )
        print fila_accion

        self.acciones.append(fila_accion)


    def particion_nueva(self, widget=None):
        widget.set_sensitive(False)
        part_nueva.Main(self)

    def deshacer(self, widget=None):
        self.inicializar(self.data)

