#-*- coding: UTF-8 -*-

import commands

class Main():
    def __init__(self):
        pass

    def usado(self, particion):
        commands.getstatusoutput('umount /mnt'.format(particion))
        commands.getstatusoutput('mount {0} /mnt'.format(particion))
        cmd = 'df --sync {0}'.format(particion)
        a, b = commands.getstatusoutput(
            cmd+" | grep '/' | awk '{print $3,$4}'"
            )[1].split()
        commands.getstatusoutput('umount {0}'.format(particion))
        return a+'kB', b+'kB'

    def lista_discos(self):
        '''
            devuelve los discos que están conectados al equipo
        '''
        discos = []
        devices = commands.getstatusoutput('ls -1 /sys/block/')[1].split('\n')
        for dev in devices:
            discos.append('/dev/'+dev)
        return discos

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
            l = l.strip(';')
            if len(l.split(':')) == 5:
                l = l+'::'

            num, ini, fin, tam, fs, tipo, flags = l.split(':')
            part = disco+str(num)
            usado = '0kB'
            libre = tam

            if fs.find('swap') != -1:
                fs = 'swap'

            if flags == '':
                flags = 'none'

            if fs == 'free':
                num = 0
                part = 0
                tipo = 'free'
            elif fs == '':
                tipo = 'extended'
                fs = 'extended'
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

if __name__ == "__main__":
    print "Iniciado..."
    obj = Main()
    print obj.lista_discos()

    for part in obj.lista_particiones('/dev/sda'):
        print part

    print "Finalizado."

