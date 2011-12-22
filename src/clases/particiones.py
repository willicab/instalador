#-*- coding: UTF-8 -*-

import commands
import os

class Main():
    def __init__(self):
        pass

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
            if disco[2:9] == "*-cdrom" or disco.find('*-disk:') == 2:
                leer = False
                continue
            if leer == True:
                disco = disco[7:].split(': ')
                #print disco
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
        #print cmd, salida
        salida = salida[1].split('\n')
        for a in salida:
            if a.find('Disk') == 0:
                total = a.split(':')[1][1:]
            if Leer == True:
                num = a[Number:Start].strip().replace(',', '.')    # número de la partición
                ini = a[Start:End].strip().replace(',', '.')   # inicio
                fin = a[End:Size].strip().replace(',', '.')  # fin
                tam = a[Size:Type].strip().replace(',', '.')  # tamaño
                tipo = a[Type:File].strip().replace(',', '.') # tipo de partición
                fs = a[File:Flags].strip().replace(',', '.')   # sistema de archivos de la partición
                if fs == '' : fs = 'none'
                flags = a[Flags:].strip().replace(',', '.')  # banderas
                part = disco + num      # partición
                # Espacios usado y libre
                
                if fs.find('swap') == -1 and num != '' and tipo != 'extended':
                    usado, libre = self.usado(part) 
                else:
                    usado, libre = '0kB', tam
                if ini != '': # and tipo != 'extended':
                    if p != '':
                        if p == part: particiones.append([
                            part,   #0
                            ini,    #1
                            fin,    #2
                            tam,    #3
                            tipo,   #4
                            fs,     #5
                            flags,  #6
                            usado,  #7
                            libre,  #8
                            total,  #9
                            num,    #10
                            ])
                    else:
                        particiones.append([
                            part,   #0
                            ini,    #1
                            fin,    #2
                            tam,    #3
                            tipo,   #4
                            fs,     #5
                            flags,  #6
                            usado,  #7
                            libre,  #8
                            total,  #9
                            num,    #10
                            ])
                #print part, ini, fin, tam, tipo, fs, flags, usado, libre, total, num
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
    
    def particionar(self, disco, tipo, formato, inicio, fin):
        '''
            Argumentos:
            - disco: el disco donde se realizará la partición. Ej: /dev/sda
            - tipo: el tipo de partición a realizar {primary, extended, logical}
            - formato: el formato que usará la partición {ext2, ext4, linux-swap
            ,fat32, ntfs}
            - inicio: donde comenzará la partición, en kB
            - fin: donde terminará la partición, en kB
        '''
        cmd = 'echo y | parted -s {0} mkpart {1} {2} {3}k {4}k'. \
        format(disco, tipo, formato, inicio, fin)
        salida = commands.getstatusoutput(cmd)
        return salida[0]
