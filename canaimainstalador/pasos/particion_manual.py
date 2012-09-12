#-*- coding: UTF-8 -*-

import gtk

from canaimainstalador.clases.common import floatify, humanize, TblCol
from canaimainstalador.clases import particion_nueva
from canaimainstalador.clases.tabla_particiones import TablaParticiones
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

        # btn_nueva
        self.btn_nueva = gtk.Button("Nueva")
        self.btn_nueva.show()
        self.btn_nueva.connect("clicked", self.particion_nueva)

        # btn_eliminar
        self.btn_eliminar = gtk.Button("Eliminar")
        self.btn_eliminar.show()
        self.btn_eliminar.connect("clicked", self.particion_eliminar)


        # btn_redimension
        self.btn_redimension = gtk.Button("Redimensionar")
        self.btn_redimension.show()
        self.btn_redimension.connect("clicked", self.particion_redimensionar)

        # btn_deshacer
        self.btn_deshacer = gtk.Button("Deshacer todo")
        self.btn_deshacer.show()
        self.btn_deshacer.connect("clicked", self.deshacer)

        self.botonera1 = gtk.HButtonBox()
        self.botonera1.set_layout(gtk.BUTTONBOX_START)
        self.botonera1.set_homogeneous(False)
        self.botonera1.add(self.btn_nueva)
        self.botonera1.add(self.btn_redimension)
        self.botonera1.add(self.btn_eliminar)
        self.botonera1.add(self.btn_deshacer)
        self.put(self.botonera1, 0, 245)

        # llenar la tabla por primera vez
        self.inicializar(data)

    def inicializar(self, data):
        '''
        Inicializa todas las variables
        '''

        self.data = data
        self.disco = data['disco']
        self.particiones = data['particiones']

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

        # Llevar los botones a su estado inicial
        self.btn_nueva.set_sensitive(False)
        self.btn_redimension.set_sensitive(False)
        self.btn_eliminar.set_sensitive(False)

        # Llenar la tabla con el contenido actual del disco
        if self.tabla != None:

            #l_part = Particiones().lista_particiones(self.disco)
            for particion in self.particiones:
                p_disp = particion[0]
                p_ini = particion[1]
                p_fin = particion[2]
                p_tam = particion[3]
                p_format = particion[4]
                p_tipo = particion[5]
                p_usado = particion[7]
                p_libre = particion[8]
                p_num = particion[10]

                fila = [
                       msj.particion.get_dispositivo(p_disp, p_num),
                       msj.particion.get_tipo(p_tipo),
                       msj.particion.get_formato(p_format),
                       '', # Punto de montaje
                       humanize(floatify(p_tam)),
                       humanize(p_usado),
                       humanize(p_libre),
                       floatify(p_ini),
                       floatify(p_fin)
                   ]
                self.lista.append(fila)

            self.llenar_tabla()

    def seleccionar_fila(self, fila):
        '''Acciones a tomar cuando una fila de la tabla es seleccionada'''

        self.fila_selec = fila

        # Es particion extendida?
        if fila[TblCol.TIPO] == msj.particion.extendida:
            self.bext = True
        else:
            self.bext = False

        # BTN_NUEVA
        if fila[TblCol.FORMATO] == msj.particion.libre:
            # Activar solo si hay menos de 4 particiones primarias
            if self.contar_primarias() < 4:
                self.btn_nueva.set_sensitive(True)
            # o si la part. libre pertenece a una part. extendida
            elif fila[TblCol.TIPO] == msj.particion.extendida:
                self.btn_nueva.set_sensitive(True)
        else:
            self.btn_nueva.set_sensitive(False)

        #BTN_REDIMENSION
        print floatify(fila[TblCol.TAMANO])
        if floatify(fila[TblCol.TAMANO]) > floatify(fila[TblCol.USADO]):
            self.btn_redimension.set_sensitive(True)
        else:
            self.btn_redimension.set_sensitive(False)

        # BTN_ELIMINAR
        # Solo se pueden eliminar particiones, no espacios libres
        if fila[TblCol.FORMATO] != msj.particion.libre:
            self.btn_eliminar.set_sensitive(True)
        else:
            self.btn_eliminar.set_sensitive(False)

    def contar_primarias(self):
        '''Cuenta la cantidad de particiones primarias. Las particiones
        extendidas cuentan como primarias'''
        total = 0
        for fila in self.lista:
            # Los espacios libres no se cuentan
            if fila[TblCol.FORMATO] == msj.particion.libre:
                continue
            # Si es una particion extendida
            if fila[TblCol.TIPO] == msj.particion.extendida:
                total = total + 1
            # Si la particion es primaria
            elif fila[TblCol.TIPO] == msj.particion.primaria:
                total = total + 1

        return total

    def existe_extendida(self):
        'Determina si existe por lo menos una particion extandida'
        for fila in self.lista:
            if fila[TblCol.TIPO] == msj.particion.extendida:
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
            if fila[TblCol.MONTAJE] == '/':
                self.raiz = True

            # Cuenta las particiones primarias
            if fila[TblCol.TIPO] == msj.particion.primaria or fila[TblCol.TIPO] == \
            msj.particion.extendida:
                self.primarias = self.primarias + 1

    def ordenar_lista(self):
        'Ordena la lista por el inicio de la particion'
        tamano = len(self.lista)
        for i in range(tamano):
            i = i # Solo para quitar el warning (unused variable)
            for k in range(tamano - 1):
                ini = self.lista[k][TblCol.INICIO]
                ini_sig = self.lista[k + 1][TblCol.INICIO]
                if ini > ini_sig:
                    f_temp = self.lista[k]
                    self.lista[k] = self.lista[k + 1]
                    self.lista[k + 1] = f_temp


    def agregar_a_lista(self, fila, pop=True):
        '''Agrega una nueva particion a la lista en el sitio adecuado segun su
        inicio'''

        i = 0
        temp = []
        inicio = fila[TblCol.INICIO]
        agregado = False

        for f in self.lista:
            temp.append(f)

            if len(self.lista) > i + 1 and not agregado:
                ini_anterior = f[TblCol.INICIO]
                ini_siguiente = self.lista[i + 1][TblCol.INICIO]
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

    #TODO: Implementar
    def particion_redimensionar(self, widget=None):
        widget.set_sensitive(False)


    def particion_nueva(self, widget=None):
        widget.set_sensitive(False)
        particion_nueva.Main(self)

    def deshacer(self, widget=None):
        self.inicializar(self.data)

