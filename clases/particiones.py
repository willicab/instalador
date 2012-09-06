#-*- coding: UTF-8 -*-

import commands, os, parted, gudev

class Main():
    def __init__(self):
        pass

    def usado(self, particion):
        if os.path.exists(particion):
            commands.getstatusoutput('umount /mnt'.format(particion))
            commands.getstatusoutput('mount {0} /mnt'.format(particion))
            cmd = 'df --sync {0}'.format(particion)
            a, b = commands.getstatusoutput(
                cmd+" | grep '/' | awk '{print $3,$4}'"
                )[1].split()
            commands.getstatusoutput('umount {0}'.format(particion))
        else: a,b = ('0', '0')
        return a+'kB', b+'kB'

    def lista_discos(self):
        '''
            devuelve los discos que están conectados al equipo
        '''
        l = []
        d = gudev.Client(['block'])
        c = d.query_by_subsystem('block')
        for i in c:
            if i.get_devtype() == 'disk':
                l.append(i.get_device_file())
        return l

    def lista_particiones(self, disco):
        '''
            Crea una lista de particiones disponibles en un disco dado
        '''
        particiones = []
        parted = 'parted -s -m {0} unit kB print free'.format(disco)
        parts = commands.getstatusoutput(parted)[1].split('\n')
        total = parts[1].split(':')[1]
        salida = parts[2:]

        for l in salida:
            print l
            l = l.strip(';')
            if len(l.split(':')) == 5:
                l = l+'::'

            num, ini, fin, tam, fs, tipo, flags = l.split(':')
            part = disco+str(num)
            usado = '0kB'
            libre = tam

            if flags == '':
                flags = 'none'

            if fs == '' and num == '1':
                fs = 'extended'
                tipo = 'extended'

            elif fs == 'free' and num == '1':
                num = 0
                part = 0
                tipo = 'free'

            elif fs == '' and num != '1':
                fs = 'unknown'
                tipo = 'unknown'

            elif not os.path.exists(part):
                fs = 'unknown'
                tipo = 'unknown'

            else:
                tipo = 'primary'
                usado, libre = self.usado(part)

            print part, ini, fin, tam, fs, tipo, flags, usado, libre, total, num
            particiones.append(
                [part, ini, fin, tam, fs, tipo, flags, usado, libre, total, num]
                )

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

class Drive(parted.Device):
    """ Wrapper class linked to the parted.Device class and parted.Disk class
    Will allow us to have a central place to perform operations"""
    def __init__(self, path):
        parted.Device.__init__(self, path)
        self.disk = parted.Disk(self)

    def listPartitions(self):
        """ Returns a list of existing partitions in the drive
        (parted.Partition objects)"""
        return self.disk.partitions

if __name__ == "__main__":
    d = Main()
    a = d.lista_discos()
    print a

