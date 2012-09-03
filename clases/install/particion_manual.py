#-*- coding: UTF-8 -*-

import os
import commands
import clases.particiones
import clases.general as gen

class Main():
    part = clases.particiones.Main()
    particiones_montadas = {}
    particiones_montadas2 = {}
    boot = False
    def __init__(self, cfg, parent):
        self.cfg = cfg
        self.metodo = cfg['metodo']
        self.tipo = cfg['tipo']
        self.lista = cfg['lista_manual']
        if (self.metodo == 'todo' or self.metodo == 'vacio') and \
           self.tipo == 'particion_4':
            self.disco = cfg['disco']
        else:
            self.particion = cfg['particion']
            self.disco = self.particion[:-1]
            self.num = int(self.particion[-1:])
            self.ini = int(gen.kb(cfg['inicio']))
            self.fin = int(gen.kb(cfg['fin']))

            print 'Disco: ', cfg['disco']
            if cfg['metodo'] != 'todo' and cfg['metodo'] != 'vacio' :
                self.nuevo_fin = int(gen.kb(cfg['nuevo_fin']))
            print self.nuevo_fin, cfg['nuevo_fin']
            self.fs = cfg['fs']

    def auto(self):
        self.redimensionar(self.particion,
                           self.ini,
                           self.nuevo_fin,
                           self.disco,
                           self.num,
                           self.fs)
        salida = self.particionar()
        return salida

    def todo(self, vacio):
        p = self.part.lista_particiones(self.disco)
        self.ini = 1049                          # Inicio de la partición
        if self.cfg['fin'][-2:] != 'kB':
            self.cfg['fin'] = self.cfg['fin'] + 'kB'
        self.fin = int(float(gen.kb(self.cfg['fin'])))
        gen.desmontar(self.disco)
        if vacio == False:
            for s in p:
                num = s[10]
                if s[4].find('swap') > -1:
                    cmd = 'swapoff '.format(s[0])
                    print cmd, commands.getstatusoutput(cmd)
                    cmd = 'parted -s {0} rm {1}'.format(self.disco, num)
                    print cmd, commands.getstatusoutput(cmd)
                if num != '':
                    cmd = 'parted -s {0} rm {1}'.format(self.disco, num)
                    print cmd, commands.getstatusoutput(cmd)
        salida = self.particionar()
        return salida

    def redimensionar(self, particion, ini_win, fin_win, disco, num, fs):
        os.system('umount -l {0}'.format(particion))
        if fs == 'ntfs': # Redimensiono la particion si es NTFS
            cmd = 'echo y | ntfsresize -P --force {0} -s {1}k'.\
                format(particion, fin_win - ini_win)
            print cmd, commands.getstatusoutput(cmd)
            cmd = 'parted -s {0} rm {1}'.format(disco, num)
            print cmd, commands.getstatusoutput(cmd)
            cmd = 'parted -s {0} mkpart primary NTFS {1}k {2}k'.\
                format(disco, ini_win, fin_win)
            print cmd, commands.getstatusoutput(cmd)
        elif fs == 'fat32': # Redimensiono la partición si es FAT32 o EXT3
            cmd = 'parted -s {0} resize {1} {2}k {3}k'.\
                format(disco, num, ini_win, fin_win)

            print cmd, commands.getstatusoutput(cmd)
            #commands.getstatusoutput(cmd)

    def particionar(self):
        particion = []
        for fila in self.lista:
            suma = 0
            disco = fila[0]
            if fila[1] == 'Primaria':
                tipo = 'primary'
                particion.append([fila[2], fila[5], fila[3]])
            if fila[1] == 'Lógica':
                tipo = 'logical'
                suma = 32
                particion.append([fila[2], fila[5] + 32, fila[3]])
            if fila[1] == 'Extendida':
                tipo = 'extended'
            inicio = fila[5] + suma
            cmd = 'parted -s {0} mkpart {1} {2} {3}k {4}k'.\
                   format(fila[0],
                          tipo,
                          fila[2],
                          fila[5] + suma,
                          fila[6]
                   )
            print cmd, commands.getstatusoutput(cmd)
        particiones = self.part.lista_particiones(disco)
        for inicios in particiones:
        # vuelvo a listar las particiones para buscar el nombre de cada
        # particion creada
            inicio = [inicios[1][:-2] , \
                str(int(float(inicios[1][:-2].replace(',', '.'))) + 1), \
                str(int(float(inicios[1][:-2].replace(',', '.'))) - 1)]
            for part in particion:
                cmd = ''
                if str(part[1]) in inicio:
                    if part[0] == 'ext4':
                        cmd = 'mkfs.ext4 '
                        if part[2] != 'Ninguno':
                            self.particiones_montadas[inicios[0]] = '/target/' + part[2]
                            self.particiones_montadas2[inicios[0]] = '/target/' + part[2]
                    elif part[0] == 'ext3':
                        cmd = 'mkfs.ext3 '
                        if part[2] != 'Ninguno':
                            self.particiones_montadas[inicios[0]] = '/target/' + part[2]
                            self.particiones_montadas2[inicios[0]] = '/target/' + part[2]
                    elif part[0] == 'ext2':
                        cmd = 'mkfs.ext2 '
                        if part[2] != 'Ninguno':
                            self.particiones_montadas[inicios[0]] = '/target/' + part[2]
                            self.particiones_montadas2[inicios[0]] = '/target/' + part[2]
                    elif part[0] == 'linux-swap':
                        cmd = 'mkswap '
                        os.system('swapon {0}'.format(inicios[0]))
                    elif part[0] == 'reiserfs':
                        cmd = 'echo y | mkreiserfs '
                        if part[2] != 'Ninguno':
                            self.particiones_montadas[inicios[0]] = '/target/' + part[2]
                            self.particiones_montadas2[inicios[0]] = '/target/' + part[2]
                    elif part[0] == 'fat16':
                        cmd = 'mkfs.vfat -F 16 '
                        if part[2] != 'Ninguno':
                            self.particiones_montadas[inicios[0]] = '/target/' + part[2]
                            self.particiones_montadas2[inicios[0]] = '/target/' + part[2]
                    elif part[0] == 'fat32':
                        cmd = 'mkfs.vfat -F 32 '
                        if part[2] != 'Ninguno':
                            self.particiones_montadas[inicios[0]] = '/target/' + part[2]
                            self.particiones_montadas2[inicios[0]] = '/target/' + part[2]

                    cmd = cmd + str(inicios[0])
                    print '---', cmd, commands.getstatusoutput(cmd)
                    commands.getstatusoutput(cmd)
                    if part[2] == '/boot' or (part[2] == '/' and self.boot == False):
                        self.boot = inicios[0]
        gen.montar(self.particiones_montadas)
        return [self.particiones_montadas2, self.boot]
