#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import commands, os, parted, gudev, hashlib

class Particiones():
    def __init__(self):
        pass

    def lista_discos(self):
        '''
            devuelve los discos que están conectados al equipo
        '''
        l = []
        d = gudev.Client(['block'])
        c = d.query_by_subsystem('block')
        for i in c:
            _type = i.get_devtype()
            _bus = i.get_property('ID_BUS')
            _name = i.get_device_file()
            if _type == 'disk':
                if _bus == 'ata' or _bus == 'usb' or _bus == 'memstick':
                    try:
                        e = Drive(_name)
                    except Exception as x:
                        e = False
                    if e:
                        l.append(_name)
        return sorted(l)

    def usado(self, particion):
        if os.path.exists(particion):
            salida = commands.getstatusoutput('mount {0} /mnt'.format(particion))
            s = os.statvfs('/mnt')
            used = float(((s.f_blocks - s.f_bfree) * s.f_frsize) / 1024)
            salida = commands.getstatusoutput('umount {0}'.format(particion))
        else:
            used = 'unknown'
        return used

    def lista_particiones(self, disco):
        '''
            Crea una lista de particiones disponibles en un disco dado
        '''
        l = []
        p = []
        d = Drive(disco)
        sectorsize = d.sectorSize
        total = float(d.getSize(unit='KB'))

        for j in d.disk.partitions: l.append(j)
        for w in d.disk.getFreeSpacePartitions(): l.append(w)

        for i in l:
            code = i.type
            part = i.path
            ini = float(i.geometry.start * sectorsize / 1024)
            fin = float(i.geometry.end * sectorsize / 1024)
            tam = float(i.geometry.length * sectorsize / 1024)
            num = int(i.number)
            preusado = self.usado(part)
            usado = tam
            libre = float(0)

            if num != -1:
                if i.fileSystem != None:
                    if code != 2:
                        fs = i.fileSystem.type
                        usado = self.usado(part)
                        libre = tam - usado
                        if fs == 'linux-swap(v1)':
                            fs = 'swap'
                            usado = tam
                            libre = float(0)
                else:
                    if code == 2:
                        fs = 'extended'
                    else:
                        fs = 'unknown'
                flags = i.getFlagsAsString()
            else:
                fs = 'free'
                libre = tam
                usado = float(0)
                flags = ''

            if not flags:
                flags = 'none'

            if libre < 0 or usado == 'unknown':
                libre = float(0)
                usado = tam

            if code == 0 or code == 4:
                tipo = 'primary'
            elif code == 1 or code == 5:
                tipo = 'logical'
            elif code == 2:
                tipo = 'extended'

            p.append(
                [part, ini, fin, tam, fs, tipo, flags, usado, libre, total, num]
                )

        return sorted(p, key=lambda particiones: particiones[1])

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

class Drive(parted.Device):
    def __init__(self, path):
        parted.Device.__init__(self, path)
        self.disk = parted.Disk(self)


