#-*- coding: UTF-8 -*-

import os
import commands

class Main():
    def __init__(self, particiones):
        self.particiones = particiones 
        self.out = '# <file system>\t<mount point>\t<type>\t<options>\t<dump>\t<pass>\n'
        self.out = self.out + 'proc\t/proc\tproc\tdefaults\t0 0\n'
        self.out = self.out + 'sys\t/sys\tsysfs\tdefaults\t0 0\n'
        
    def obtener_particiones(self):
        salida = commands.getstatusoutput('echo $(ls /dev/[sh]d[a_z]?*)')
        #print 'obtener_particiones: ' + salida
        return salida[1].split()
    
    def obtener_cdroms(self):
        salida = commands.getstatusoutput('echo $(head -3 /proc/sys/dev/cdrom/info | tail -1 | cut -f 3-)')
        lista = salida[1].split()
        print 'obtener_cdroms {0}'.format(salida)
        if salida[0] != 0: return False
        return lista
    
    def obtener_fs(self, particion):
        salida = commands.getstatusoutput("/sbin/blkid {0} | awk '{1}'".format(particion, '{print $2 \" \"$3}'))
        #print 'Salida: ', salida[1]
        if salida[1] == '': return {'uuid' : '', 'fs' : ''}
        uuid = salida[1].split()[0].split('=')
        uuid = "{0}={1}".format(uuid[0], uuid[1][1:-1])
        fs = salida[1].split()[1].split('=')[1][1:-1]
        #print particion.split('/dev/')[1]
        return {'uuid' : uuid, 'fs' : fs}
        
    def crear_archivo(self):
        salida = commands.getstatusoutput('grep rw /proc/cmdline')
        if salida[1] != '':
            defaults = '\tdefaults,noauto\t0\t2'
        else:
            defaults = '\tro,users,noauto\t0\t2'
            
        particiones = self.obtener_particiones()
        
        for particion in particiones:
            dev = particion
            entrada = self.obtener_fs(particion)
            uuid = entrada['uuid']
            fs = entrada['fs']
            
            if fs == 'swap':
                entrada_fs = "{0}\tnone\tswap\tsw\t0 0".format(uuid)
                self.out =  self.out + entrada_fs + '\n'
            elif fs != '' and fs != 'vfat':
                defaults = 'defaults            0 0'
                if fs == 'ntfs':
                    defaults = "defaults,locale=es_VE.UTF-8,auto,users,uid=1000 0\t2"
                    fs = 'ntfs'
                if self.particiones.has_key(particion):
                    print "particiones: {0} {1}".format(particion.split('/target'), particion)
                    mntpoint = '{0}/'.format(self.particiones[particion].split('/target')[1])
                else:
                    mntpoint = '/target/media/{0}'.format(particion.split('/dev/')[1])
                    os.system('mkdir -p {0}'.format(mntpoint))
                    mntpoint = mntpoint.split('/target')[1]
                entry_fs = '{0}\t{1}\t{2}\t{3}'.format(dev, mntpoint, fs, defaults)
                self.out =  self.out + entry_fs + '\n'
        cdroms = self.obtener_cdroms()
        num = 0
        if cdroms != False:
            for cd in cdroms:
                entry = '/dev/{0}\t/media/cdrom{1}\tudf,iso9660\tro,user,noauto\t0 0'.format(cd, num)
                os.system('mkdir -p /target/media/cdrom{0}'.format(num))
                num = num + 1
                self.out =  self.out + entry + '\n'
        print self.out
        os.system('echo {0} > /target/etc/fstab'.format(self.out))
        #archivo = open('/target/etc/fstab', 'w')
        #archivo.write(self.out)
        #archivo.close()

if __name__ == "__main__":
    m = Main({'/dev/sda1':'/target/boot', '/dev/sda5':'/target', '/dev/sda6':'/target/usr', '/dev/sda7':'/target/home'})
    print m.obtener_particiones()
    print m.obtener_fs('/dev/sdb1')
    print m.obtener_cdroms()
    m.crear_archivo()
