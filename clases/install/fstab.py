#-*- coding: UTF-8 -*-

import os, commands, glob, re

class Main():
    def __init__(self, particiones):
        self.particiones = particiones

    def obtener_particiones(self):
        return glob.glob('/dev/[sh]d[a-z]?*')
    
    def obtener_cdroms(self):
        info = '/proc/sys/dev/cdrom/info'
        cmd = 'cat {0} | grep "drive name:" | sed "s/drive name://g"'.format(info)
        salida = commands.getstatusoutput(cmd)[1].split()

        if salida: return salida
	else: return False
    
    def obtener_fs(self, particion):
        cmd = '/sbin/blkid -p {0}'.format(particion)
        salida = commands.getstatusoutput(cmd)[1].split()
        tid = [i for i, item in enumerate(salida) if re.search('^TYPE=*', item)]
        uid = [i for i, item in enumerate(salida) if re.search('^UUID=*', item)]

        if tid and uid:
            uuid = salida[uid[0]].replace('"','')
            fs = salida[tid[0]].replace('TYPE=', '').replace('"','')
        else:
            uuid = ''
            fs = ''

        return {'uuid' : uuid, 'fs' : fs}
        
    def crear_archivo(self):
        particiones = self.obtener_particiones()
        cdroms = self.obtener_cdroms()
        supported = ['btrfs', 'ext2', 'ext3', 'ext4', 'vfat', 'hfs', 'hfsplus', 'jfs', 'ntfs', 'xfs', 'reiser4', 'reiserfs']
        defaults = 'defaults\t0\t0'
        destination = '/target/etc/fstab'
        content = ''
	content += '#<filesystem>\t<mountpoint>\t<type>\t<options>\t<dump>\t<pass>\n'
        content += '\nproc\t/proc\tproc\tdefaults\t0\t0'

        for part in particiones:
            entrada = self.obtener_fs(part)
            uuid = entrada['uuid']
            fs = entrada['fs']

            cmd = 'udevadm info --query="all" --name="{0}"'.format(part.split('/dev/')[1][:-1])
            cbus = cmd+" | grep 'ID_BUS' | awk -F= '{print $2}'"
            ctype = cmd+" | grep 'ID_TYPE' | awk -F= '{print $2}'"
            dbus = commands.getstatusoutput(cbus)[1].split()
            dtype = commands.getstatusoutput(ctype)[1].split()

            if fs == 'swap' and dbus[0] != 'usb' and dtype[0] == 'disk':
                content += "\n{0}\tnone\tswap\tsw\t0\t0".format(uuid)
                print part,uuid,fs,dbus,dtype
            elif fs and uuid:
                for fstype in supported:
                    if fstype == fs:
                        if self.particiones.has_key(part):
                            mnt = self.particiones[part].split('/target')[1]
                            point = '{0}/'.format(mnt)
                        elif dbus[0] != 'usb' and dtype[0] == 'disk':
                            fldr = '/target/media/{0}'.format(part.split('/dev/')[1])
                            os.system('mkdir -p {0}'.format(fldr))
                            mnt = fldr.split('/target')[1]
                            point = '{0}/'.format(mnt)
                        else:
                            point = ''
                        print part,uuid,fs,dbus,dtype
                if point:
                    content += '\n{0}\t{1}\t{2}\t{3}'.format(uuid, point, fs, defaults)
            else:
                content += '\n# DISABLED: {0}, TYPE: ?, UUID: ?'.format(part)

        for cd in cdroms:
            num = cd[-1:]
            os.system('mkdir -p /target/media/cdrom{0}'.format(num))
            content += '\n/dev/{0}\t/media/cdrom{1}\tudf,iso9660\tuser,noauto\t0\t0'.format(cd, num)

        f = open(destination, 'w')
        f.write(content)
        f.close()

if __name__ == "__main__":
    m = Main({'/dev/sda1':'/target', '/dev/sda2':'/target/home'})
    m.crear_archivo()
