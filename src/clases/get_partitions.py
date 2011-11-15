#-*- coding: UTF-8 -*-
import os
from collections import namedtuple

disk_ntuple = namedtuple('partition',  'device mountpoint fstype')
usage_ntuple = namedtuple('usage',  'total used free percent')
SUFIJOS = {1000: ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],
            1024: ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']}

def disk_partitions(all=False):
    """Return all mountd partitions as a nameduple.
    If all == False return phyisical partitions only.
    """
    phydevs = []
    f = open("/proc/filesystems", "r")
    for line in f:
        if not line.startswith("nodev"):
            phydevs.append(line.strip())

    retlist = []
    f = open('/etc/mtab', "r")
    for line in f:
        if not all and line.startswith('none'):
            continue
        fields = line.split()
        device = fields[0]
        mountpoint = fields[1]
        fstype = fields[2]
        if not all and fstype not in phydevs:
            continue
        if device == 'none':
            device = ''
        ntuple = disk_ntuple(device, mountpoint, fstype)
        retlist.append(ntuple)
    return retlist

def medida_aproximada(medida, un_kilobyte_es_1024_bytes=True):
    '''Convierte el tamaño de un fichero a formato legible por humanos.

    Argumentos por nombre:
    medida -- tamaño del fichero en bytes
    un_kilobyte_es_1024_bytes -- si es True (por defecto), usar múltiplos
                                 de 1024; si es False, usar múltiplos de 1000

    Devuelve: cadena

    '''
    if medida < 0:
        raise ValueError('el número debe ser no-negativo')

    multiplo = 1024 if un_kilobyte_es_1024_bytes else 1000
    for sufijo in SUFIJOS[multiplo]:
        medida /= multiplo
        if medida < multiplo:
            return '{0:.1f} {1}'.format(medida, sufijo)

    raise ValueError('número demasiado grande')

def disk_usage(path):
    """Return disk usage associated with path."""
    try:
        st = os.statvfs(path)
    except:
        print str(path) + 'No se encuentra'
        return  usage_ntuple(0, 0, 0, 0)
    free = (st.f_bavail * st.f_frsize)
    total = (st.f_blocks * st.f_frsize)
    used = (st.f_blocks - st.f_bfree) * st.f_frsize
    try:
        percent = ret = (float(used) / total) * 100
    except ZeroDivisionError:
        percent = 0
    # NB: the percentage is -5% than what shown by df due to
    # reserved blocks that we are currently not considering:
    # http://goo.gl/sWGbH
    return usage_ntuple(medida_aproximada(total), medida_aproximada(used), medida_aproximada(free), round(percent, 1))

if __name__ == '__main__':
    for part in disk_partitions():
        print part
        print "    %s\n" % str(disk_usage(part.mountpoint))


