# -*- coding: utf-8 -*-
#
# ==============================================================================
# PAQUETE: canaima-instalador
# ARCHIVO: canaimainstalador/translator.py
# COPYRIGHT:
#       (C) 2012 William Abrahan Cabrera Reyes <william@linux.es>
#       (C) 2012 Erick Manuel Birbe Salazar <erickcion@gmail.com>
#       (C) 2012 Luis Alejandro Martínez Faneyth <luis@huntingbears.com.ve>
# LICENCIA: GPL-3
# ==============================================================================
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# COPYING file for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import gtk

from canaimainstalador.clases.common import floatify, humanize, TblCol, \
    is_primary, is_usable, PStatus, is_resizable, is_free, debug_list, is_logic
from canaimainstalador.clases import particion_nueva, particion_redimensionar, \
    particion_eliminar, particion_editar
from canaimainstalador.clases.tabla_particiones import TablaParticiones
from canaimainstalador.translator import msj

class PasoPartManual(gtk.Fixed):

    def __init__(self, data):
        gtk.Fixed.__init__(self)

        self.data = data
        self.disco = self.data['metodo']['disco'][0]

        self.tabla = TablaParticiones()
        #self.tabla.set_doble_click(self.activar_tabla);
        self.tabla.set_seleccionar(self.table_row_selected)

        self.scroll = gtk.ScrolledWindow()
        self.scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        self.scroll.set_size_request(690, 240)
        self.scroll.add(self.tabla)
        self.put(self.scroll, 0, 0)
        self.tabla.show()
        self.scroll.show()

        # btn_nueva
        self.btn_nueva = gtk.Button("Nueva")
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_ADD, 12)
        self.btn_nueva.set_image(image)
        self.btn_nueva.show()
        self.btn_nueva.connect("clicked", self.new_partition)

        # btn_editar
        self.btn_editar = gtk.Button("Editar")
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_EDIT, 12)
        self.btn_editar.set_image(image)
        self.btn_editar.show()
        self.btn_editar.connect("clicked", self.edit_partition)

        # btn_eliminar
        self.btn_eliminar = gtk.Button("Eliminar")
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_REMOVE, 12)
        self.btn_eliminar.set_image(image)
        self.btn_eliminar.show()
        self.btn_eliminar.connect("clicked", self.delete_partition)

        # btn_redimension
        self.btn_redimension = gtk.Button("Redimensionar")
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_INDENT, 12)
        self.btn_redimension.set_image(image)
        self.btn_redimension.show()
        self.btn_redimension.connect("clicked", self.resize_partition)

        # btn_deshacer
        self.btn_deshacer = gtk.Button("Deshacer todo")
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_UNDO, 12)
        self.btn_deshacer.set_image(image)
        self.btn_deshacer.show()
        self.btn_deshacer.connect("clicked", self.undo_all_actions)

        self.botonera1 = gtk.HButtonBox()
        self.botonera1.set_layout(gtk.BUTTONBOX_START)
        self.botonera1.set_homogeneous(False)
        self.botonera1.add(self.btn_nueva)
        self.botonera1.add(self.btn_editar)
        self.botonera1.add(self.btn_redimension)
        self.botonera1.add(self.btn_eliminar)
        self.botonera1.add(self.btn_deshacer)
        self.put(self.botonera1, 0, 245)

        # llenar la tabla por primera vez
        self.initialize(data)

    def initialize(self, data):
        '''
        Inicializa todas las variables
        '''
        self.lista = []         #Lista de las particiones hechas
        self.acciones = []      # Almacena las acciones pendientes a realizar
        self.fila_selec = None  # Ultima fila seleccionada de la tabla
        self.raiz = False

        self.set_buttons_insensitives()

        # Llenar la tabla con el contenido actual del disco
        if self.tabla != None:

            #l_part = Particiones().lista_particiones(self.disco)
            for particion in self.data['particiones']:
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
                       p_ini,
                       p_fin,
                       False, # Formatear
                       PStatus.NORMAL,
                   ]
                self.lista.append(fila)

            self.fill_table()

    def set_buttons_insensitives(self):
        'Bloquea todos los botones de acciones'
        # Llevar los botones a su estado inicial
        self.btn_nueva.set_sensitive(False)
        self.btn_editar.set_sensitive(False)
        self.btn_redimension.set_sensitive(False)
        self.btn_eliminar.set_sensitive(False)


    def table_row_selected(self, fila):
        '''Acciones a tomar cuando una fila de la tabla es seleccionada'''

        # Si no se selecciona una fila valida
        if fila == None:
            print "Nada seleccionado."
            return
        else:
            self.fila_selec = fila

        # BTN_NUEVA
        if is_free(fila):
            # Activar solo si hay menos de 4 particiones primarias
            if is_primary(fila) and self.count_primary() < 4:
                self.btn_nueva.set_sensitive(True)
            # o si la part. libre es logica
            elif is_logic(fila) and self.count_logical() < 11:
                self.btn_nueva.set_sensitive(True)
            else:
                self.btn_nueva.set_sensitive(False)
        else:
            self.btn_nueva.set_sensitive(False)

        # BTN_USAR
        if is_usable(self.fila_selec):
            self.btn_editar.set_sensitive(True)
        else:
            self.btn_editar.set_sensitive(False)

        #BTN_REDIMENSION
        # Si la particion NO es libre
        # si el filesystem tiene redimensionador
        # y no se ha marcado la aprticion para usarla
        # y si hay espacio para redimensionar dentro de la particion
        if fila[TblCol.FORMATO] != msj.particion.libre \
        and is_resizable(fila[TblCol.FORMATO]) \
        and fila[TblCol.ESTADO] != PStatus.USED \
        and floatify(fila[TblCol.TAMANO]) > floatify(fila[TblCol.USADO]):
            self.btn_redimension.set_sensitive(True)
        else:
            self.btn_redimension.set_sensitive(False)

        # BTN_ELIMINAR
        # Solo se pueden eliminar particiones, no los espacios libres
        #TODO: Eliminar part. extendidas (necesita verificar part. logicas)
        if not is_free(fila):
            self.btn_eliminar.set_sensitive(True)
        else:
            self.btn_eliminar.set_sensitive(False)

    def count_primary(self):
        '''Cuenta la cantidad de particiones primarias. Las particiones
        extendidas cuentan como primarias'''
        total = 0
        for fila in self.lista:
            if is_primary(fila) and not is_free(fila):
                total = total + 1
        return total

    def count_logical(self):
        '''Cuenta la cantidad de particiones logicas que no sean vacias'''
        total = 0
        for fila in self.lista:
            if is_logic(fila) and not is_free(fila):
                total = total + 1
        return total

    def fill_table(self):
        '''Llena la tabla con las particiones existentes en el disco'''

        self.order_list()

        # Limpia previamente la tabla para inicializar su llenado
        self.tabla.liststore.clear()
        self.tabla.get_selection().unselect_all()

        # LLena la tabla con los datos
        for fila in self.lista:
            self.tabla.agregar_fila(fila)

            # Verifica si hay punto de montaje raiz "/"
            if fila[TblCol.MONTAJE] == '/':
                self.raiz = True
        if len(self.acciones) > 0:
            self.btn_deshacer.set_sensitive(True)
        else:
            self.btn_deshacer.set_sensitive(False)

    def order_list(self):
        'Ordena la lista por el inicio de la particion (metodo burbuja)'
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

    def delete_partition(self, widget):
        self.set_buttons_insensitives()
        w_elim = particion_eliminar.Main(self.lista, self.fila_selec, \
                                         self.acciones)
        self.lista = w_elim.lista
        self.acciones = w_elim.acciones
        self.fill_table()
        print "---ACCIONES---"
        print debug_list(self.acciones)
        print "--------------"

    def resize_partition(self, widget):
        self.set_buttons_insensitives()
        widget.set_sensitive(False)
        w_redim = particion_redimensionar.Main(self.disco, self.lista, self.fila_selec, \
                                               self.acciones)
        self.acciones = w_redim.acciones
        self.lista = w_redim.lista
        self.fill_table()
        print "---ACCIONES---"
        print debug_list(self.acciones)
        print "--------------"

    def new_partition(self, widget):
        self.set_buttons_insensitives()
        widget.set_sensitive(False)
        w_nueva = particion_nueva.Main(self)
        # Se actualiza la tabla
        self.lista = w_nueva.lista
        self.acciones = w_nueva.acciones
        self.acciones
        self.fill_table()
        print "---ACCIONES---"
        print debug_list(self.acciones)
        print "--------------"

    def edit_partition(self, widget):
        self.set_buttons_insensitives()
        widget.set_sensitive(False)
        w_usar = particion_editar.Main(self.lista, self.fila_selec, self.acciones)
        self.lista = w_usar.lista
        self.acciones = w_usar.acciones
        self.fill_table()
        print "---ACCIONES---"
        print debug_list(self.acciones)
        print "--------------"

    def undo_all_actions(self, widget=None):
        self.initialize(self.data)
        print "---ACCIONES---"
        print debug_list(self.acciones)
        print "--------------"

