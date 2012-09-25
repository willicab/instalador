#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import commands, os, parted, _ped, hashlib, random, subprocess

from canaimainstalador.config import *
from canaimainstalador.common import ProcessGenerator

class Particiones():
    def __init__(self):
        pass

    def nueva_tabla_particiones(self, drive, t):
        dev = parted.Device(drive)
        new = parted.freshDisk(dev, t)
        try:
            new.commit()
        except _ped.IOException as x:
            print x

    def lista_discos(self):
        '''
            devuelve los discos que están conectados al equipo
        '''
        l = []
        dev = parted.getAllDevices()
        for d in dev:
            l.append(d.path)
        return sorted(l)

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

        return sorted(p, key = lambda particiones: particiones[1])

    def crear_particion(self, drive, start, end, fs, partype):
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
        s_sec = start * 1024 / dev.sectorSize
        e_sec = end * 1024 / dev.sectorSize
        m_sec = ((e_sec - s_sec) / 2) + s_sec

        if partype == 'primary' or partype == 0:
            partype = _ped.PARTITION_NORMAL
        elif partype == 'logical' or partype == 1:
            partype = _ped.PARTITION_LOGICAL
        elif partype == 'extended' or partype == 2:
            partype = _ped.PARTITION_EXTENDED
        else:
            return False

        geometry = parted.Geometry(device = dev, start = s_sec, end = e_sec)
        constraint = parted.Constraint(exactGeom = geometry)
        partition = parted.Partition(disk = disk, type = partype, geometry = geometry)

        if disk.addPartition(partition = partition, constraint = constraint) \
            and disk.commit():
            if partype != _ped.PARTITION_EXTENDED:
                if fs in FSPROGS:
                    p = ProcessGenerator(
                        FSPROGS[fs][0].format(disk.getPartitionBySector(m_sec).path)
                        )
            return True
        else:
            return False

    def borrar_particion(self, part):
        '''
        Argumentos:
        - disco: el disco donde se realizará la partición. Ej: /dev/sda
        - tipo: el tipo de partición a realizar {primary, extended, logical}
        - formato: el formato que usará la partición {ext2, ext4, linux-swap,fat32, ntfs}
        - inicio: donde comenzará la partición, en kB
        - fin: donde terminará la partición, en kB
        '''
        dev = parted.Device(part[:-1])
        disk = parted.Disk(dev)
        partition = disk.getPartitionByPath(part)

        if partition and \
            disk.deletePartition(partition = partition) and \
            disk.commit():
            return True
        else:
            return False

    def redimensionar_particion(self, part, newend):
        '''
        Argumentos:
        - disco: el disco donde se realizará la partición. Ej: /dev/sda
        - tipo: el tipo de partición a realizar {primary, extended, logical}
        - formato: el formato que usará la partición {ext2, ext4, linux-swap,fat32, ntfs}
        - inicio: donde comenzará la partición, en kB
        - fin: donde terminará la partición, en kB
        '''
        drive = part[:-1]
        dev = parted.Device(drive)
        disk = parted.Disk(dev)
        partition = disk.getPartitionByPath(part)
        fs = partition.fileSystem.type
        partype = partition.type
        currstart = partition.geometry.start * dev.sectorSize / 1024
        currend = partition.geometry.end * dev.sectorSize / 1024
        newsize = str(int((newend - currstart)))+'K'

        if newend > currend:
            # Redimensionar primero la partición y luego el sistema de archivos
            if self.borrar_particion(part = part):
                if fs == 'linux-swap(v1)':
                    if self.crear_particion(
                        drive = drive, start = currstart, end = newend,
                        fs = 'swap', partype = partype
                        ):
                        return True
                else:
                    if self.crear_particion(
                        drive = drive, start = currstart, end = newend,
                        fs = None, partype = partype
                        ):
                        if FSPROGS[fs][1] != '':
                            if fs == 'btrfs':
                                p = ProcessGenerator('umount /mnt')
                                p = ProcessGenerator('mount {0} /mnt'.format(part))
                                p = ProcessGenerator(FSPROGS[fs][1].format(newsize, part))
                                p = ProcessGenerator('umount /mnt')
                            else:
                                p = ProcessGenerator(FSPROGS[fs][1].format(newsize, part))
                            return True
                        else:
                            return False
        elif newend < currend:
            # Redimensionar primero el sistema de archivos y luego la partición
            if fs == 'linux-swap(v1)':
                if self.borrar_particion(part = part):
                    if self.crear_particion(
                        drive = drive, start = currstart, end = newend,
                        fs = 'swap', partype = partype
                        ):
                        return True
            else:
                if FSPROGS[fs][1] != '':
                    if fs == 'btrfs':
                        p = ProcessGenerator('umount /mnt')
                        p = ProcessGenerator('mount {0} /mnt'.format(part))
                        p = ProcessGenerator(FSPROGS[fs][1].format(newsize, part))
                        p = ProcessGenerator('umount /mnt')
                    else:
                        p = ProcessGenerator(FSPROGS[fs][1].format(newsize, part))

                    if self.borrar_particion(part = part):
                        if self.crear_particion(
                            drive = drive, start = currstart, end = newend,
                            fs = None, partype = partype
                            ):
                            return True
                else:
                    return False

        elif newend == currend:
            return True

