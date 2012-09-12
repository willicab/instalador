#-*- coding: UTF-8 -*-

import os, commands

from  canaimainstalador.clases.particiones import Particiones
import canaimainstalador.clases.common as gen
import canaimainstalador.clases.install.particion_manual as particion_manual

class Main():
    #root_p2 = '20GB'
    #root_p3 = '3GB'
    #usr = '18GB'
    boot = '256MB'
    part = Particiones()
    particiones_montadas = {}
    particiones_montadas2 = {}

    def __init__(self, cfg, parent, vacio=False):
        self.cfg = cfg
        self.disco = cfg['disco']
        self.par = parent
        self.lista = self.part.lista_particiones(self.disco)
        self.root_p2 = gen.hum(gen.part_root1(self.lista[0][9]))
        self.root_p3 = gen.hum(gen.part_root2(self.lista[0][9]))
        self.usr = gen.hum(gen.part_root1(self.lista[0][9]))
        self.vacio = vacio
        try:
            self.ini = cfg['inicio']
        except:
            self.ini = 0
        try:
            self.fin = cfg['fin']
        except:
            self.fin = 0


    def particion_1(self):
        particion_boot = ''
        self.par.accion('Eliminando Particiones')
        gen.desmontar(self.disco)     # Desmonta todas las particiones del disco
        p = self.part.lista_particiones(self.disco)
        if self.vacio == False:
            for s in p:
                num = s[10]
                if s[4].find('swap') > -1:
                    cmd = 'swapoff '.format(s[0])
                    print cmd, commands.getstatusoutput(cmd)
                if num != '':
                    cmd = 'parted -s {0} rm {1}'.format(self.disco, num)
                    print cmd, commands.getstatusoutput(cmd)
            ini = 1049                      # Inicio de la partición
            fin = gen.kb(p[0][9])           # Fin de la partición
        else:
            ini = float(self.ini)           # Inicio de la partición
            fin = float(self.fin)           # Fin de la partición
        disco = self.disco                  # Ruta del disco
        ram = int(gen.ram())                # Cantidad de Ram
        swap = (ram * 2) if ram < 1048576 else ram #tamaño de la swap
        fin_ext = int(fin)                 # Fin de la partición Extendida
        ini_ext = fin_ext - swap            # Inicio de la partición Extendida
        ini_swap = ini_ext + 32             # Inicio de la partición Swap
        fin_swap = fin_ext                  # Fin de la partición Swap
        ini_root = int(ini)                 # Inicio de la particion Root
        fin_root = ini_ext                  # Fin de la partición Root

        self.par.accion('Creando Particiones')
        self.part.particionar(disco, 'primary', 'ext4', ini_root, fin_root)
        self.part.particionar(disco, 'extended', '', ini_ext, fin_ext)
        self.part.particionar(disco, 'logical', 'linux-swap', ini_swap, fin_swap)

        p = self.part.lista_particiones(self.disco)
        for s in p:
        # vuelvo a listar las particiones para buscar el nombre de cada
        # particion creada
            l = [str(int(float(s[1][:-2].replace(',', '.'))) + 0), \
                str(int(float(s[1][:-2].replace(',', '.'))) + 1), \
                str(int(float(s[1][:-2].replace(',', '.'))) - 1)]

            if str(ini_root) in l:
                self.par.accion('Formateando partición {0} (/) como ext4'\
                .format(s[0]))
                os.system('mkfs.ext4 {0}'.format(s[0]))
                self.particiones_montadas[s[0]] = '/target'
                self.particiones_montadas2[s[0]] = '/target'
                os.system("parted {0} toggle {1} boot".format(s[0][:-1], s[0][-1:]))
                particion_boot = s[0]

            if str(ini_swap) in l:
                self.par.accion('Formateando partición {0} como swap'\
                .format(s[0]))
                os.system('mkswap {0}'.format(s[0]))
                os.system('swapon {0}'.format(s[0]))
        gen.montar(self.particiones_montadas)
        return [self.particiones_montadas2, particion_boot]

    def particion_2(self):
        particion_boot = ''
        self.par.accion('Eliminando Particiones')
        gen.desmontar(self.disco)  # Desmonta todas las particiones del disco
        p = self.part.lista_particiones(self.disco)
        if self.vacio == False:
            ini = 1049                          # Inicio de la partición
            fin = gen.kb(p[0][9])               # Fin de la partición
            for s in p:
                num = s[10]
                if s[4].find('swap') > -1:
                    cmd = 'swapoff '.format(s[0])
                    print cmd, commands.getstatusoutput(cmd)
                if num != '':
                    cmd = 'parted -s {0} rm {1}'.format(self.disco, num)
                    print cmd, commands.getstatusoutput(cmd)
        else:
            ini = float(self.ini)             # Inicio de la partición
            fin = float(self.fin)             # Fin de la partición
        disco = self.disco                    # Ruta del disco
        ram = int(gen.ram())                  # Cantidad de Ram
        swap = (ram * 2) if ram < 1048576 else ram #tamaño de la swap
        ini_root = int(ini)                   # Inicio de la particion Root
        fin_root = ini_root + int(gen.kb(self.root_p2))#Fin de la partición Root
        ini_ext = (int(fin_root) + 32)        # Inicio de la partición Extendida
        fin_ext = (int(fin))                 # Fin de la partición Extendida
        ini_home = ini_ext + 32               # Inicio de la partición Home
        fin_home = fin_ext - swap             # Fin de la partición Home
        ini_swap = fin_ext - swap + 32        # Inicio de la partición Swap
        fin_swap = fin_ext                    # Fin de la partición Swap

        self.par.accion('Creando Particiones')
        self.part.particionar(disco, 'primary', 'ext4', ini_root, fin_root)
        self.part.particionar(disco, 'extended', '', ini_ext, fin_ext)
        self.part.particionar(disco, 'logical', 'ext4', ini_home, fin_home)
        self.part.particionar(disco, 'logical', 'linux-swap', ini_swap, fin_swap)

        p = self.part.lista_particiones(disco)
        for s in p:
        # vuelvo a listar las particiones para buscar el nombre de cada
        # particion creada
            l = [str(int(float(s[1][:-2].replace(',', '.'))) + 0), \
                str(int(float(s[1][:-2].replace(',', '.'))) + 1), \
                str(int(float(s[1][:-2].replace(',', '.'))) - 1)]

            if str(ini_root) in l:
                self.par.accion('Formateando partición {0} como ext4'\
                .format(s[0]))
                os.system('mkfs.ext4 {0}'.format(s[0]))
                self.particiones_montadas[s[0]] = '/target'
                self.particiones_montadas2[s[0]] = '/target'
                os.system("parted {0} toggle {1} boot".format(s[0][:-1], s[0][-1:]))
                particion_boot = s[0]

            if str(ini_home) in l:
                self.par.accion('Formateando partición {0} como ext4'\
                .format(s[0]))
                os.system('mkfs.ext4 {0}'.format(s[0]))
                self.particiones_montadas[s[0]] = '/target/home'
                self.particiones_montadas2[s[0]] = '/target/home'

            if str(ini_swap) in l:
                self.par.accion('Formateando partición {0} como swap'\
                .format(s[0]))
                os.system('mkswap {0}'.format(s[0]))
                os.system('swapon {0}'.format(s[0]))
        gen.montar(self.particiones_montadas)
        return [self.particiones_montadas2, particion_boot]

    def particion_3(self):
        particion_boot = ''
        self.par.accion('Eliminando Particiones')
        gen.desmontar(self.disco)  # Desmonta todas las particiones del disco
        p = self.part.lista_particiones(self.disco)
        if self.vacio == False:
            ini = 1049                          # Inicio de la partición
            fin = gen.kb(p[0][9])               # Fin de la partición
            for s in p:
                num = s[10]
                if s[4].find('swap') > -1:
                    cmd = 'swapoff '.format(s[0])
                    print cmd, commands.getstatusoutput(cmd)
                if num != '':
                    cmd = 'parted -s {0} rm {1}'.format(self.disco, num)
                    print cmd, commands.getstatusoutput(cmd)
        else:
            ini = float(self.ini)           # Inicio de la partición
            fin = float(self.fin)           # Fin de la partición
        disco = self.disco                  # Ruta del disco
        ram = int(gen.ram())                # Cantidad de Ram
        swap = (ram * 2) if ram < 1048576 else ram #tamaño de la swap
        ini_boot = int(ini)                 # Inicio de la particion Boot
        fin_boot = int(ini_boot + gen.kb(self.boot)) # Fin de la particion Boot
        ini_ext = int(fin_boot) + 32        # Inicio de la partición Extendida
        fin_ext = int(fin)                 # Fin de la partición Extendida
        ini_root = int(ini_ext + 32)        # Inicio de la particion Root
        fin_root = int(ini_root + int(gen.kb(self.root_p3)))# Fin de la Root
        ini_usr = int(fin_root + 32)        # Inicio de la partición Usr
        fin_usr = int(ini_usr + gen.kb(self.usr)) # Fin de la partición Usr
        ini_home = int(fin_usr + 32)        # Inicio de la partición Home
        fin_home = int(fin_ext - swap)      # Fin de la partición Home
        ini_swap = int(fin_ext - swap + 32) # Inicio de la partición Swap
        fin_swap = int(fin_ext)             # Fin de la partición Swap

        self.par.accion('Creando Particiones')
        self.part.particionar(disco, 'primary', 'ext2', ini_boot, fin_boot)
        self.part.particionar(disco, 'extended', '', ini_ext, fin_ext)
        self.part.particionar(disco, 'logical', 'ext4', ini_usr, fin_usr)
        self.part.particionar(disco, 'logical', 'ext4', ini_root, fin_root)
        self.part.particionar(disco, 'logical', 'ext4', ini_home, fin_home)
        self.part.particionar(disco, 'logical', 'linux-swap', ini_swap, fin_swap)

        p = self.part.lista_particiones(disco)
        for s in p:
        # vuelvo a listar las particiones para buscar el nombre de cada
        # particion creada
            l = [str(int(float(s[1][:-2].replace(',', '.'))) + 0), \
                str(int(float(s[1][:-2].replace(',', '.'))) + 1), \
                str(int(float(s[1][:-2].replace(',', '.'))) - 1)]

            if str((ini_boot)) in l:
                self.par.accion('Formateando partición {0} (/boot) como ext2'\
                .format(s[0]))
                os.system('mkfs.ext2 {0}'.format(s[0]))
                self.particiones_montadas[s[0]] = '/target/boot'
                self.particiones_montadas2[s[0]] = '/target/boot'
                os.system("parted {0} toggle {1} boot".format(s[0][:-1], s[0][-1:]))
                particion_boot = s[0]

            if str((ini_root)) in l:
                self.par.accion('Formateando partición {0} (/) como ext4'\
                .format(s[0]))
                os.system('mkfs.ext4 {0}'.format(s[0]))
                self.particiones_montadas[s[0]] = '/target'
                self.particiones_montadas2[s[0]] = '/target'

            if str((ini_usr)) in l:
                self.par.accion('Formateando partición {0} (/usr) como ext4'\
                .format(s[0]))
                os.system('mkfs.ext4 {0}'.format(s[0]))
                self.particiones_montadas[s[0]] = '/target/usr'
                self.particiones_montadas2[s[0]] = '/target/usr'

            if str((ini_home)) in l:
                self.par.accion('Formateando partición {0} (/home) como ext4'\
                .format(s[0]))
                os.system('mkfs.ext4 {0}'.format(s[0]))
                self.particiones_montadas[s[0]] = '/target/home'
                self.particiones_montadas2[s[0]] = '/target/home'

            if str((ini_swap)) in l:
                self.par.accion('Formateando partición {0} como swap'\
                .format(s[0]))
                os.system('mkswap {0}'.format(s[0]))
                os.system('swapon {0}'.format(s[0]))
        gen.montar(self.particiones_montadas)

        return [self.particiones_montadas2, particion_boot]

    def particion_4(self):
        self.part_manual = particion_manual.Main(self.cfg, self.par)
        salida = self.part_manual.todo(self.vacio)
        return salida

