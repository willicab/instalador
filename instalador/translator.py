#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from gettext import gettext as _

MAIN_ROOT_ERROR_MSG = _('Canaima Instalador debe ser ejecutado con permisos de superusuario.')
MAIN_ROOT_ERROR_TITLE = _('Error de permisología')

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
