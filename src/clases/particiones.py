#-*- coding: UTF-8 -*-

import commands
import os

class Main():
    def __init__(self):
        pass
    
    def lista_discos(self):
        '''
            devuelve los discos que están conectados al equipo
        '''
        leer = False
        i = -1
        discos = []
        opt = {}
        a = commands.getstatusoutput("lshw -class disco")[1].split('\n')
        for disco in a:
            if disco[2:] == "*-disco":
                if i >= 0: 
                    discos.append(opt)
                    opt = {}
                i = i + 1
                leer = True
                continue
            if disco[2:9] == "*-cdrom":
                leer = False
                continue
            if leer == True:
                disco = disco[7:].split(': ')
                opt[disco[0]] = disco[1]
        discos.append(opt)
        #print discos
        return discos

    def usado(self, particion):
        commands.getstatusoutput("mount {0} /tmp".format(particion))
        a = commands.getstatusoutput("df -h /tmp")
        a = a[1].split('\n')[1].split()
        commands.getstatusoutput("umount /tmp")
        return [a[2] + 'B', a[3] + 'B']

    def lista_discos(self):
        '''
            devuelve los discos que están conectados al equipo
        '''
        leer = False
        i = -1
        discos = []
        opt = {}
        a = commands.getstatusoutput("lshw -class disk")[1].split('\n')
        for disco in a:
            if disco[2:] == "*-disk":
                if i >= 0: 
                    discos.append(opt)
                    opt = {}
                i = i + 1
                leer = True
                continue
            if disco[2:9] == "*-cdrom":
                leer = False
                continue
            if leer == True:
                disco = disco[7:].split(': ')
                opt[disco[0]] = disco[1]
        discos.append(opt)
        return discos

    def lista_particiones(self, disco, p=''):
        '''
            Crea una lista de particiones disponibles en un disco dado, incluyendo
        '''
        particiones = []
        libres = []
        Leer = False
        cmd = "parted {0} unit kB print free".format(disco)
        salida = commands.getstatusoutput(cmd)
        salida = salida[1].split('\n')
        for a in salida:
            if Leer == True:
                num = a[Number:Start].strip().replace(',', '.')    # número de la partición
                ini = a[Start:End].strip().replace(',', '.')   # inicio
                fin = a[End:Size].strip().replace(',', '.')  # fin
                tam = a[Size:Type].strip().replace(',', '.')  # tamaño
                tipo = a[Type:File].strip().replace(',', '.') # tipo de partición
                #print 'tipo', tipo
                #if tipo == '' : tipo = 'none'
                fs = a[File:Flags].strip().replace(',', '.')   # sistema de archivos de la partición
                if fs == '' : fs = 'none'
                flags = a[Flags:].strip().replace(',', '.')  # banderas
                part = disco + num      # partición
                # Espacios usado y libre
                # print tipo
                
                if fs.find('swap') == -1 and num != '' and tipo != 'extended':
                    usado, libre = self.usado(part) 
                else:
                    usado, libre = '0kB', tam
                if tipo != 'extended' and ini != '':
                    if p != '':
                        if p == part: particiones.append([part, ini, fin, \
                            tam, tipo, fs, flags, usado, libre])
                    else:
                        particiones.append([part, ini, fin, \
                            tam, tipo, fs, flags, usado, libre])
            if a.startswith('Number'):
                Number = a.find('Number')
                Start = a.find('Start')
                End = a.find('End')
                Size = a.find('Size')
                Type = a.find('Type')
                File = a.find('File')
                Flags = a.find('Flags')
                Leer = True
        return particiones
