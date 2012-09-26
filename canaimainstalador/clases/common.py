#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import commands, re, subprocess, math, cairo, gtk, hashlib, random, urllib2, os

from canaimainstalador.translator import msj

def espacio_usado(particion):
    if os.path.exists(particion):
        ProcessGenerator('umount /mnt')
        ProcessGenerator('mount {0} /mnt'.format(particion))
        s = os.statvfs('/mnt')
        used = float(((s.f_blocks - s.f_bfree) * s.f_frsize) / 1024)
        ProcessGenerator('umount /mnt')
    else:
        used = 'unknown'
    return used

def assisted_mount(bind, plist):
    if bind:
        bindcmd = '-o bind'
    else:
        bindcmd = ''

    for p, m, fs in plist:
        if fs:
            fscmd = '-t {0}'.format(fs)
        else:
            fscmd = ''

        ProcessGenerator('mount {0} {1} {2} {3}'.format(bindcmd, fscmd, p, m))

def preseed_debconf_values(mnt, debconflist):
    ProcessGenerator('rm -rf {0}/tmp/debconf'.format(mnt))

    for debconf in debconflist:
        ProcessGenerator('chroot {0} echo "{1}" >> /tmp/debconf'.format(mnt, debconf))

    ProcessGenerator('chroot {0} debconf-set-selections < /tmp/debconf'.format(mnt))
    ProcessGenerator('rm -rf {0}/tmp/debconf'.format(mnt))

def instalar_paquetes(mnt, dest, plist):
    for loc, name in plist:
        ProcessGenerator('mkdir -p {0}'.format(mnt+dest))
        ProcessGenerator('cp {0}/{1}*.deb {2}'.format(loc, name, mnt+dest+'/'))
        ProcessGenerator('chroot {0} dpkg -i {1}/{2}*.deb'.format(mnt, dest, name))
        ProcessGenerator('rm -rf {0}'.format(mnt+dest))

def desinstalar_paquetes(mnt, plist):
    for name in plist:
        ProcessGenerator('chroot {0} aptitude purge {1}'.format(mnt, name))

def reconfigurar_paquetes(mnt, plist):
    for name in plist:
        ProcessGenerator('chroot {0} dpkg-reconfigure {1}'.format(mnt, name))

def crear_etc_network_interfaces(mnt, cfg):
    content = ''
    destination = mnt + cfg
    interdir = '/sys/class/net/'
    interlist = next(os.walk(interdir))[1]

    for i in interlist:
        if i == 'lo':
            content += '\nauto lo'
            content += '\niface lo inet loopback\n'
        elif re.sub('\d', '', i) == 'eth':
            content += '\nallow-hotplug {0}'.format(i)
            content += '\niface {0} inet dhcp\n'.format(i)

    f = open(destination, 'w')
    f.write(content)
    f.close()

def crear_etc_hostname(mnt, cfg, maq):
    f = open(mnt + cfg, 'w')
    f.write(maq + '\n')
    f.close()

def crear_etc_hosts(mnt, cfg, maq):
    content = '127.0.0.1\t\t{0}\t\tlocalhost\n'.format(maq)
    content += '::1\t\tlocalhost\t\tip6-localhost ip6-loopback\n'
    content += 'fe00::0\t\tip6-localnet\n'
    content += 'ff00::0\t\tip6-mcastprefix\n'
    content += 'ff02::1\t\tip6-allnodes\n'
    content += 'ff02::2\t\tip6-allrouters\n'
    content += 'ff02::3\t\tip6-allhosts'

    f = open(mnt + cfg, 'w')
    f.write(content)
    f.close()

def crear_etc_default_keyboard(mnt, cfg, key):
    pattern = "^XKBLAYOUT=*"
    re_obj = re.compile(pattern)
    new_value = "XKBLAYOUT=\"" + key + "\"\n"

    file_path = mnt + cfg
    infile = open(file_path, "r")
    string = ''

    # Busca el valor del pattern
    is_match = False
    for line in infile:
        match = re_obj.search(line)
        if match :
            is_match = True
            string += new_value
        else:
            string += line
    infile.close()

    # Si no encuentra el pattern lo agrega al final con el valor asignado
    if not is_match:
        string += new_value

    # Escribe el archivo modificado
    outfile = open(file_path, "w")
    outfile.write(string)
    outfile.close()

def crear_etc_fstab(mnt, cfg, mountlist, cdroms):
    defaults = 'defaults\t0\t0'
    content = '#<filesystem>\t<mountpoint>\t<type>\t<options>\t<dump>\t<pass>\n'
    content += '\nproc\t/proc\tproc\t{0}'.format(defaults)

    for part, point, fs in mountlist:
        uuid = get_uuid(part)

        if fs == 'swap':
            content += "\n{0}\tnone\tswap\tsw\t0\t0".format(uuid)
        else:
            content += '\n{0}\t{1}\t{2}\t{3}'.format(uuid, point, fs, defaults)
            ProcessGenerator('mkdir -p {0}'.format(mnt+point))

    for cd in cdroms:
        num = cd[-1:]
        content += '\n/dev/{0}\t/media/cdrom{1}\tudf,iso9660\tuser,noauto\t0\t0'.format(cd, num)
        ProcessGenerator('mkdir -p {0}'.format(mnt+'/media/cdrom'+num))

    f = open(mnt+cfg, 'w')
    f.write(content)
    f.close()

def lista_cdroms():
    info = '/proc/sys/dev/cdrom/info'
    cmd = 'cat {0}| grep "drive name:" | sed "s/drive name://g"'.format(info)
    salida = commands.getstatusoutput(cmd)[1].split()

    if salida:
        return salida
    else:
        return False

def get_uuid(particion):
    cmd = '/sbin/blkid -p {0}'.format(particion)
    salida = commands.getstatusoutput(cmd)[1].split()
    uid = [i for i, item in enumerate(salida) if re.search('^UUID=*', item)]

    if uid:
        return salida[uid[0]].replace('"', '')
    else:
        return False

# Orden de las columnas en la tabla de particiones
class TblCol:
    DISPOSITIVO = 0
    TIPO = 1
    FORMATO = 2
    MONTAJE = 3
    TAMANO = 4
    USADO = 5
    LIBRE = 6
    INICIO = 7
    FIN = 8
    FORMATEAR = 9
    ESTADO = 10

def givemeswap():
    r = ram()
    if r >= float(1024 * 1024):
        return r
    else:
        return r * 2

class HeadRequest(urllib2.Request):
    def get_method(self):
        return "HEAD"

def draw_rounded(cr, area, radius):
    x1, y1, x2, y2 = area
    cr.arc(x1 + radius, y1 + radius, radius, 2 * (math.pi / 2), 3 * (math.pi / 2))
    cr.arc(x2 - radius, y1 + radius, radius, 3 * (math.pi / 2), 4 * (math.pi / 2))
    cr.arc(x2 - radius, y2 - radius, radius, 0 * (math.pi / 2), 1 * (math.pi / 2))
    cr.arc(x1 + radius, y2 - radius, radius, 1 * (math.pi / 2), 2 * (math.pi / 2))
    cr.close_path()
    return cr

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv / 3], 16) for i in range(0, lv, lv / 3))

def process_color(item, start, end):
    start = hex_to_rgb(start) + (0,)
    end = hex_to_rgb(end) + (1,)

    r1, g1, b1, pos = start
    r3, g3, b3, pos = end
    r2, g2, b2, pos = (int(r1 + r3) / 2, int(g1 + g3) / 2, int(b1 + b3) / 2, 0.5)
    mid = (r2, g2, b2, pos)

    for i in start, mid, end:
        rgb = float(i[3]), float(i[0]) / 255, float(i[1]) / 255, float(i[2]) / 255
        item.add_color_stop_rgb(*rgb)

def set_color(fs, alto):
    libre = cairo.LinearGradient(0, 0, 0, alto)

    if fs == 'btrfs':
        process_color(libre, '#ff5d2e', '#ff912e')
    elif fs == 'ext2':
        process_color(libre, '#2460c8', '#2e7bff')
    elif fs == 'ext3':
        process_color(libre, '#1b4794', '#2460c8')
    elif fs == 'ext4':
        process_color(libre, '#102b58', '#1b4794')
    elif fs == 'fat16':
        process_color(libre, '#00b900', '#00ff00')
    elif fs == 'fat32':
        process_color(libre, '#008100', '#00b900')
    elif fs == 'ntfs':
        process_color(libre, '#003800', '#008100')
    elif fs == 'hfs+':
        process_color(libre, '#382720', '#895f4d')
    elif fs == 'hfs':
        process_color(libre, '#895f4d', '#e49e80')
    elif fs == 'jfs':
        process_color(libre, '#e49e80', '#ffcfbb')
    elif fs == 'swap':
        process_color(libre, '#650000', '#cc0000')
    elif fs == 'reiser4':
        process_color(libre, '#45374f', '#806794')
    elif fs == 'reiserfs':
        process_color(libre, '#806794', '#b994d5')
    elif fs == 'xfs':
        process_color(libre, '#e89900', '#e8d000')
    elif fs == 'free':
        process_color(libre, '#ffffff', '#ffffff')
    elif fs == 'extended':
        process_color(libre, '#7dfcfe', '#7dfcfe')
    elif fs == 'unknown':
        process_color(libre, '#000000', '#000000')
    elif fs == 'part':
        process_color(libre, '#b8b598', '#b8b598')

    return libre

def floatify(num):
    '''
        Convierte un número escrito en formato para lectura por humanos a
        kilobytes.
        Argumentos:
        - num: un número en formato para lectura por humanos de tipo string
        Salida: el valor en kB de tipo float
    '''
    if not num:
        num = 0

    num = str(num)
    unidad = re.sub('[0123456789.]', '', num.replace(',', '.').upper())
    peso = float(re.sub('[TGMKB]', '', num.replace(',', '.').upper()))

    if unidad == 'TB':      kb = peso * 1024.0 * 1024.0 * 1024.0    # TB a KB
    elif unidad == 'GB':    kb = peso * 1024.0 * 1024.0             # GB a KB
    elif unidad == 'MB':    kb = peso * 1024.0                      # MB a KB
    elif unidad == 'KB':    kb = peso                               # KB a KB
    elif unidad == 'B':     kb = peso / 1024.0                      # B a KB
    else:                   kb = peso                               # Sin unidad
    return float(kb)

def redondear(w, dec=0):
    if type(w) == int : return w
    if dec == 0:
        return int(w) + 1 if int(str(w).split('.')[1][0]) >= 5 else int(w)
    else:
        return float(str(w).split('.')[0] + '.' + str(w).split('.')[1][0:dec])

def humanize(valor):
    valor = float(valor)
    if valor <= 1024.0: return '{0}KB'.format(redondear(valor, 2))
    if valor <= 1048576.0: return '{0}MB'.format(redondear(valor / 1024, 2))
    if valor <= 1073741824.0: return '{0}GB'.format(redondear(valor / 1024 / 1024, 2))
    return valor

def ram():
    return 1024.0 * float(subprocess.Popen(
        'echo "scale=1;$( cat "/proc/meminfo" | grep "MemFree:" | awk \'{print $2}\' )/(10^3)" | bc',
        shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    ).communicate()[0].split('\n')[0])

def aconnect(button, signals, function, params):
    '''
        desconecta los eventos existentes en signals y conecta con function
    '''
    for i in signals:
        if button.handler_is_connected(i):
            button.disconnect(i)
    signals.append(button.connect_object('clicked', function, params))

    return signals

def UserMessage(
    message, title, mtype, buttons, c_1=False, f_1=False, p_1='',
    c_2=False, f_2=False, p_2='', c_3=False, f_3=False, p_3='',
    c_4=False, f_4=False, p_4='', c_5=False, f_5=False, p_5=''
    ):

    dialog = gtk.MessageDialog(
        parent=None, flags=0, type=mtype,
        buttons=buttons, message_format=message
        )
    dialog.set_title(title)
    response = dialog.run()
    dialog.destroy()

    if response == c_1:
        f_1(*p_1)
    if response == c_2:
        f_2(*p_2)
    if response == c_3:
        f_3(*p_3)
    if response == c_4:
        f_4(*p_4)
    if response == c_5:
        f_5(*p_5)

    return response

def ProcessGenerator(command):

    filename = '/tmp/cs-command-' + hashlib.sha1(
        str(random.getrandbits(random.getrandbits(10)))
        ).hexdigest()

    if isinstance(command, list):
        strcmd = ' '.join(command)
    elif isinstance(command, str):
        strcmd = command

    cmd = '{0} 1>{1} 2>&1'.format(strcmd, filename)

    try:
        os.mkfifo(filename)
        fifo = os.fdopen(os.open(filename, os.O_RDONLY | os.O_NONBLOCK))

        process = subprocess.Popen(
                cmd, shell=True, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
                )

        while process.returncode == None:
            process.poll()
            try:
                line = fifo.readline().strip()
                if line: print line
            except:
                continue

    finally:
        os.unlink(filename)

    return process

def debug_list(the_list):
    data = "List [\n"
    for fila in the_list:
        data = data + '  ' + str(fila) + '\n'
    data = data + ']'

    return data

def get_row_index(the_list, row):
        '''Obtiene el numero de la fila seleccionada en la tabla'''
        try:
            return the_list.index(list(row))
        except ValueError:
            return None

def has_next_row(the_list, row_index):
    'Verifica si la lista contiene una fila siguiente'
    if  row_index < len(the_list) - 1:
        return True
    else:
        return False

def get_next_row(the_list, row, row_index=None):
    '''Retorna la fila siguiente si existe'''
    if not row_index:
        row_index = get_row_index(the_list, row)

    if row_index != None and has_next_row(the_list, row_index):
        return the_list[row_index + 1]
    else:
        return None

def is_extended(row):
        'Determina si una fila pertenece a una particion extendida'
        return row[TblCol.TIPO] == msj.particion.extendida

def has_extended(lista):
        'Determina si existe por lo menos una particion extendida en la lista'
        for fila in lista:
            if fila[TblCol.TIPO] == msj.particion.extendida:
                return True
        return False

def set_partition(the_list, selected_row, new_row, pop=True):
    '''Agrega una nueva particion a la lista en el sitio adecuado segun su
    inicio'''
    index = get_row_index(the_list, selected_row)
    if pop:
        the_list[index] = new_row
    else:
        the_list.append(new_row)

    return the_list

def is_primary(fila):
    'Determina si una particion es primaria'
    p_type = fila[TblCol.TIPO]
    p_format = fila[TblCol.FORMATO]
    if p_type == msj.particion.primaria \
    or (p_type == msj.particion.extendida and p_format == ''):
        return True
    else:
        return False

def is_logic(fila):
    'Determina si una particion es lógica'
    p_type = fila[TblCol.TIPO]
    p_format = fila[TblCol.FORMATO]
    if p_type == msj.particion.logica \
    or (p_type == msj.particion.extendida and p_format != ''):
        return True
    else:
        return False

def is_usable(selected_row):
    disp = selected_row[TblCol.DISPOSITIVO]
    tipo = selected_row[TblCol.TIPO]
    fs = selected_row[TblCol.FORMATO]
    try:
        # Esta linea comprueba que el dispositivo termine en un entero, esto
        # para comprobar que tiene un formato similar a /dev/sdb3 por ejemplo.
        int(disp[-1])

        # No se usan las particiones extendidas, sino las logicas
        if tipo == msj.particion.extendida and fs == '':
            return False
        else:
            return True
    except (ValueError, IndexError):
        return False

