#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import commands, os, parted, _ped

from canaimainstalador.config import *

class Particiones():
    def __init__(self):
        pass

    def lista_discos(self):
        '''
            devuelve los discos que están conectados al equipo
        '''
        l = []
        dev = parted.getAllDevices()
        for d in dev:
            l.append(d.path)
        return sorted(l)

    def usado(self, particion):
        if os.path.exists(particion):
            salida = commands.getstatusoutput('umount /mnt')
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

        try:
            dev = parted.Device(disco)
            disk = parted.Disk(dev)
        except _ped.DiskLabelException as x:
            return p

        sectorsize = dev.sectorSize
        total = float(dev.getSize(unit='KB'))

        for j in disk.partitions: l.append(j)
        for w in disk.getFreeSpacePartitions(): l.append(w)

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

    def crear_particion(self, drive, start, end, fs, ptype):
        '''
        Argumentos:
        - disco: el disco donde se realizará la partición. Ej: /dev/sda
        - tipo: el tipo de partición a realizar {primary, extended, logical}
        - formato: el formato que usará la partición {ext2, ext4, linux-swap,fat32, ntfs}
        - inicio: donde comenzará la partición, en kB
        - fin: donde terminará la partición, en kB
        '''
        dev = parted.Device(drive)
        disk = parted.Disk(dev)
        partlist = self.lista_particiones(drive)
        geometry = parted.Geometry(device = dev, start = start, end = end)
        partition = parted.Partition(disk = disk, type = ptype, geometry = geometry)
        constraint = parted.Constraint(exactGeom = geometry)
        disk.addPartition(partition = partition, constraint = constraint)

        if disk.commit():
            for p in partlist:
                if p[1] == start:
                    part = p[0]
                    cmd = '{0} {1}'.format(FSPROGS[fs][0], part)
                    process = subprocess.Popen(
                        cmd, shell = True, stdout = subprocess.PIPE,
                        stderr = subprocess.STDOUT
                        )
            return part
        else:
            return False

    def borrar_particion(self, drive, partnum):
        '''
        Argumentos:
        - disco: el disco donde se realizará la partición. Ej: /dev/sda
        - tipo: el tipo de partición a realizar {primary, extended, logical}
        - formato: el formato que usará la partición {ext2, ext4, linux-swap,fat32, ntfs}
        - inicio: donde comenzará la partición, en kB
        - fin: donde terminará la partición, en kB
        '''
        dev = parted.Device(drive)
        disk = parted.Disk(dev)
        disk.deletePartition(partition = drive+partnum)
        if disk.commit():
            return True
        else:
            return False

    def redimensionar_particion(self, drive, partnum):
        '''
        Argumentos:
        - disco: el disco donde se realizará la partición. Ej: /dev/sda
        - tipo: el tipo de partición a realizar {primary, extended, logical}
        - formato: el formato que usará la partición {ext2, ext4, linux-swap,fat32, ntfs}
        - inicio: donde comenzará la partición, en kB
        - fin: donde terminará la partición, en kB
        '''
        dev = parted.Device(drive)
        disk = parted.Disk(dev)
        disk.deletePartition(partition = drive+partnum)
        if disk.commit():
            return True
        else:
            return False

    def nueva_tabla_particiones(self, drive, t):
        dev = parted.Device(drive)
        new = parted.freshDisk(dev, t)
        try:
            new.commit()
        except _ped.IOException as x:
            print x

