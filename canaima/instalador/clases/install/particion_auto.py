#-*- coding: UTF-8 -*-

import os
import commands
import clases.particiones
import clases.general as gen

class Main():
    root_p2 = '20GB'
    root_p3 = '3GB'
    usr = '18GB'
    boot = '256MB'
    part = clases.particiones.Main()
    particiones_montadas = {}
    particiones_montadas2 = {}

    def __init__(self, cfg, parent):
        self.particion = cfg['particion']
        self.disco = self.particion[:-1]
        self.num = self.particion[-1:]
        self.ini = cfg['inicio']
        self.fin = cfg['fin']
        self.nuevo_fin = cfg['nuevo_fin']
        self.total = int(gen.kb(self.fin)) - int(gen.kb(self.nuevo_fin))
        self.root_p2 = gen.hum(gen.part_root1(self.self.total))
        self.root_p3 = gen.hum(gen.part_root2(self.self.total))
        self.usr = gen.hum(gen.part_root1(self.self.total))
        self.swap = cfg['swap']
        self.fs = cfg['fs']
        self.par = parent

    def hay_swap(self):
        particiones = self.part.lista_particiones(self.disco)
        for p in particiones:
            if p[5].find('swap') != -1 : return True
        return False
        
    def particion_1(self):
        particion_boot = ''
        ini = int(gen.kb(self.ini))        # Inicio de la partición
        fin = int(gen.kb(self.fin))        # Fin de la partición
        swap = self.swap            # existe o no una partición swap en el disco
        fs = self.fs                       # Sistema de Archivos de la partición
        particion = self.particion         # Ruta de la partición
        disco = self.disco                 # Ruta del disco
        num = self.num                     # número de la partición
        ram = int(gen.ram())               # Cantidad de Ram
        ini_win = int(ini)                 # Inicio de la partición con windows
        fin_win = int(self.nuevo_fin)      # Fin de la partición con windows
        ini_root = fin_win + ini_win + 32  # Inicio de la particion Root
        if swap == True:               # Si existe una partición Swap
            fin_root = fin                 # Fin de la partición Root
        else:                          # Si no existe una partición Swap
            swap = (ram * 2) if ram < 1048576 else ram #tamaño de la swap
            ini_ext = fin - swap           # Inicio de la partición Extendida
            fin_ext  = fin                 # Fin de la partición Extendida
            ini_swap = ini_ext + 32        # Inicio de la partición Swap
            fin_swap = fin_ext             # Fin de la partición Swap
            fin_root = ini_ext             # Fin de la partición Root
            swap = False
        self.par.accion('Desmontando dispositivo')
        os.system('umount -l {0}'.format(self.particion) )
        self.par.accion('redimensionando partición {0}'.format(self.particion))
        if fs == 'ntfs': # Redimensiono la particion si es NTFS
            cmd = 'echo y | ntfsresize -P --force {0} -s {1}k'.\
                format(particion, fin_win)
            commands.getstatusoutput(cmd)
            cmd = 'parted -s {0} rm {1}'.format(disco, num)
            commands.getstatusoutput(cmd)
            cmd = 'parted -s {0} mkpart primary NTFS {1}k {2}k'.\
                format(disco, ini_win, fin_win + ini_win)
            commands.getstatusoutput(cmd)
        elif fs == 'fat32': # Redimensiono la partición si es FAT32
            cmd = 'parted -s {0} resize {1} {2}k {3}k'.\
                format(disco, num, ini_win, fin_win + ini_win)
            commands.getstatusoutput(cmd)
        self.par.accion('Creando Particiones')
        self.part.particionar(disco, 'primary', 'ext4', ini_root, fin_root)
        if swap == False:
            self.part.particionar(disco, 'extended', '', ini_ext, fin_ext)
            self.part.particionar(disco, 'logical', 'linux-swap', ini_swap,\
                fin_swap)

        p = self.part.lista_particiones(disco)
        for s in p: 
        # vuelvo a listar las particiones para buscar el nombre de cada
        # particion creada
            l = [s[1][:-2], \
                str(int(float(s[1][:-2].replace(',', '.'))) + 1), \
                str(int(float(s[1][:-2].replace(',', '.'))) - 1)]

            if str(ini_root) in l:
                self.par.accion('Formateando partición {0} como ext4'. \
                    format(s[0]))
                os.system('mkfs.ext4 {0}'.format(s[0]))
                self.particiones_montadas[s[0]] = '/target'
                self.particiones_montadas2[s[0]] = '/target'
                particion_boot=s[0]

            if swap == False:
                if str(ini_swap) in l:
                    self.par.accion('Formateando partición {0} como swap'. \
                        format(s[0]))
                    os.system('mkswap {0}'.format(s[0]))
                    os.system('swapon {0}'.format(s[0]))
        gen.montar(self.particiones_montadas)
        return [self.particiones_montadas2, particion_boot]

    def particion_2(self):
        particion_boot = ''
        ini = int(gen.kb(self.ini))        # Inicio de la partición
        fin = int(gen.kb(self.fin))        # Fin de la partición
        swap = self.swap            # existe o no una partición swap en el disco
        fs = self.fs                       # Sistema de Archivos de la partición
        particion = self.particion         # Ruta de la partición
        disco = self.disco                 # Ruta del disco
        num = self.num                     # número de la partición
        ram = int(gen.ram())               # Cantidad de Ram
        ini_win = int(ini)                 # Inicio de la partición con windows
        fin_win = int(self.nuevo_fin)      # Fin de la partición con windows
        ini_root = fin_win + ini_win + 32  # Inicio de la particion Root
        fin_root = ini_root + int(gen.kb(self.root_p2))#Fin de la partición Root
        ini_ext = fin_root + 32
        fin_ext = fin
        ini_home = ini_ext + 32
        if swap == True:                # Si existe una partición Swap
            fin_home = fin_ext             # Fin de la partición Home
        else:                           # Si no existe una partición Swap
            swap = (ram * 2) if ram < 1048576 else ram #tamaño de la swap
            fin_home = fin_ext - swap      # Fin de la partición Home
            ini_swap = fin_home + 32       # Inicio de la partición Swap
            fin_swap = fin_ext             # Fin de la partición Swap
            swap = False
        self.par.accion('Desmontando dispositivo')
        cmd = 'umount {0}'.format(self.particion) 
        print cmd, commands.getstatusoutput(cmd)
        self.par.accion('redimensionando partición {0}'.format(self.particion))
        if fs == 'ntfs': # Redimensiono la particion si es NTFS
            cmd = 'echo y | ntfsresize -P --force {0} -s {1}k'.\
                format(particion, fin_win)
            commands.getstatusoutput(cmd)
            cmd = 'parted -s {0} rm {1}'.format(disco, num)
            commands.getstatusoutput(cmd)
            cmd = 'parted -s {0} mkpart primary NTFS {1}k {2}k'.\
                format(disco, ini_win, fin_win + ini_win)
            commands.getstatusoutput(cmd)
        elif fs == 'fat32': # Redimensiono la partición si es FAT32
            cmd = 'parted -s {0} resize {1} {2}k {3}k'.\
                format(disco, num, ini_win, fin_win + ini_win)
            commands.getstatusoutput(cmd)

        self.par.accion('Creando Particiones')
        self.part.particionar(disco, 'primary', 'ext4', ini_root, fin_root)
        self.part.particionar(disco, 'extended', '', ini_ext, fin_ext)
        self.part.particionar(disco, 'logical', 'ext4', ini_home, fin_home)
        if swap == False:
            self.part.particionar(disco, 'logical', 'linux-swap', ini_swap,\
                fin_swap)
            
        p = self.part.lista_particiones(disco)
        for s in p: 
        # vuelvo a listar las particiones para buscar el nombre de cada
        # particion creada
            l = [s[1][:-2], \
                str(int(float(s[1][:-2].replace(',', '.'))) + 1), \
                str(int(float(s[1][:-2].replace(',', '.'))) - 1)]

            if str(ini_root) in l:
                self.par.accion('Formateando partición {0} como ext4'. \
                    format(s[0]))
                os.system('mkfs.ext4 {0}'.format(s[0]))
                self.particiones_montadas[s[0]] = '/target'
                self.particiones_montadas2[s[0]] = '/target'
                particion_boot=s[0]

            if str(ini_home) in l:
                self.par.accion('Formateando partición {0} como ext4'. \
                    format(s[0]))
                os.system('mkfs.ext4 {0}'.format(s[0]))
                self.particiones_montadas[s[0]] = '/target/home'
                self.particiones_montadas2[s[0]] = '/target/home'

            if swap == False:
                if str(ini_swap) in l:
                    self.par.accion('Formateando partición {0} como swap'. \
                        format(s[0]))
                    os.system('mkswap {0}'.format(s[0]))
                    os.system('swapon {0}'.format(s[0]))
        gen.montar(self.particiones_montadas)
        return [self.particiones_montadas2, particion_boot]

    def particion_3(self):
        particion_boot = ''
        ini = int(gen.kb(self.ini))        # Inicio de la partición
        fin = int(gen.kb(self.fin))        # Fin de la partición
        swap = self.swap            # existe o no una partición swap en el disco
        fs = self.fs                       # Sistema de Archivos de la partición
        particion = self.particion         # Ruta de la partición
        disco = self.disco                 # Ruta del disco
        num = self.num                     # número de la partición
        ram = int(gen.ram())               # Cantidad de Ram
        ini_win = int(ini)                 # Inicio de la partición con windows
        fin_win = int(self.nuevo_fin)      # Fin de la partición con windows
        ini_boot = fin_win + ini_win + 32  # Inicio de la particion Root
        fin_boot = ini_boot + int(gen.kb(self.boot))
        ini_ext = fin_boot + 32
        fin_ext = fin
        ini_root = ini_ext + 32
        fin_root = ini_root + int(gen.kb(self.root_p3))
        ini_usr = fin_root + 32
        fin_usr = ini_usr + int(gen.kb(self.usr))
        ini_home = fin_usr + 32
        if swap == True:                # Si existe una partición Swap
            fin_home = fin_ext             # Fin de la partición Home
        else:                           # Si no existe una partición Swap
            swap = (ram * 2) if ram < 1048576 else ram #tamaño de la swap
            fin_home = fin_ext - swap      # Fin de la partición Home
            ini_swap = fin_home + 32       # Inicio de la partición Swap
            fin_swap = fin_ext             # Fin de la partición Swap
            swap = False
        self.par.accion('Desmontando dispositivo')
        cmd = 'umount {0}'.format(self.particion) 
        print cmd, commands.getstatusoutput(cmd)
        self.par.accion('redimensionando partición {0}'.format(self.particion))
        if fs == 'ntfs': # Redimensiono la particion si es NTFS
            cmd = 'echo y | ntfsresize -P --force {0} -s {1}k'.\
                format(particion, fin_win)
            commands.getstatusoutput(cmd)
            cmd = 'parted -s {0} rm {1}'.format(disco, num)
            commands.getstatusoutput(cmd)
            cmd = 'parted -s {0} mkpart primary NTFS {1}k {2}k'.\
                format(disco, ini_win, fin_win + ini_win)
            commands.getstatusoutput(cmd)
        elif fs == 'fat32': # Redimensiono la partición si es FAT32
            cmd = 'parted -s {0} resize {1} {2}k {3}k'.\
                format(disco, num, ini_win, fin_win + ini_win)
            commands.getstatusoutput(cmd)
        self.par.accion('Creando Particiones')

        self.part.particionar(disco, 'primary', 'ext4', ini_boot, fin_boot)
        self.part.particionar(disco, 'extended', '', ini_ext, fin_ext)
        self.part.particionar(disco, 'logical', 'ext4', ini_root, fin_root)
        self.part.particionar(disco, 'logical', 'ext4', ini_usr, fin_usr)
        self.part.particionar(disco, 'logical', 'ext4', ini_home, fin_home)
        
        if swap == False:
            self.part.particionar(disco, 'logical', 'linux-swap', ini_swap,\
                fin_swap)
        
        p = self.part.lista_particiones(disco)
        for s in p: 
        # vuelvo a listar las particiones para buscar el nombre de cada
        # particion creada
            l = [s[1][:-2], \
                str(int(float(s[1][:-2].replace(',', '.'))) + 1), \
                str(int(float(s[1][:-2].replace(',', '.'))) - 1)]

            if str(ini_root) in l:
                self.par.accion('Formateando partición {0} como ext4'. \
                    format(s[0]))
                os.system('mkfs.ext4 {0}'.format(s[0]))
                self.particiones_montadas[s[0]] = '/target'
                self.particiones_montadas2[s[0]] = '/target'

            if str(ini_home) in l:
                self.par.accion('Formateando partición {0} como ext4'. \
                    format(s[0]))
                os.system('mkfs.ext4 {0}'.format(s[0]))
                self.particiones_montadas[s[0]] = '/target/home'
                self.particiones_montadas2[s[0]] = '/target/home'

            if str(ini_usr) in l:
                self.par.accion('Formateando partición {0} como ext4'. \
                    format(s[0]))
                os.system('mkfs.ext4 {0}'.format(s[0]))
                self.particiones_montadas[s[0]] = '/target/usr'
                self.particiones_montadas2[s[0]] = '/target/usr'
            
            if str(ini_boot) in l:
                self.par.accion('Formateando partición {0} como ext2'. \
                    format(s[0]))
                os.system('mkfs.ext2 {0}'.format(s[0]))
                self.particiones_montadas[s[0]] = '/target/boot'
                self.particiones_montadas2[s[0]] = '/target/boot'
                particion_boot=s[0]

            if swap == False:
                if str(ini_swap) in l:
                    self.par.accion('Formateando partición {0} como swap'. \
                        format(s[0]))
                    os.system('mkswap {0}'.format(s[0]))
                    os.system('swapon {0}'.format(s[0]))
        gen.montar(self.particiones_montadas)
        return [self.particiones_montadas2, particion_boot]

