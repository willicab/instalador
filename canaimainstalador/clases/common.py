#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import commands, re, subprocess, math, cairo, gtk

from canaimainstalador.config import *
from canaimainstalador.translator import msj

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

def givemeswap():
    r = ram()
    if r >= float(1024 * 1024):
        return r
    else:
        return r * 2

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

def process_color (item, start, end):
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

#def kb(num):
#    if type(num) == int or type(num) == float : return float(num)
#    unidad = num[-2:]
#    num = num[:-2].replace(',', '.')
#    num = (float(num))
#    if unidad == 'GB': return num * 1048576.0 # Gb a Kb
#    if unidad == 'MB': return num * 1024.0    # Mb a Kb
#    if unidad == 'kB': return num             # Kb a Kb
#    return num / 1024.0                       # Bytes a Kb

#def montados(disco=''):
#    p = []
#    salida = commands.getstatusoutput('mount')[1].split('\n')
#    for m in salida:
#        #print m, disco, m.split(' ')[0][:-1], m.split(' ')[2]
#        if disco == '': 
#            p.append(m.split(' ')[2])
#        elif disco == m.split(' ')[0][:-1]:
#            p.append(m.split(' ')[2])
#    return p         

#def part_root1(total):
#    root = (kb(total) * kb(root1_min)) / kb(minimo)
#    if root < kb(root1_min): 
#        root = kb(root1_min)
#    if root > kb(root1_max): 
#        root = kb(root1_max)
#    return root

#def part_root2(total):
#    root = (kb(total) * kb(root2_min)) / kb(minimo)
#    if root < kb(root2_min): 
#        root = kb(root2_min)
#    if root > kb(root2_max): 
#        root = kb(root2_max)
#    return root

#def part_usr(total):
#    usr = (kb(total) * kb(usr_min)) / kb(minimo)
#    if usr < kb(usr_min): 
#        usr = kb(usr_min)
#    if usr > kb(usr_max): 
#        usr = kb(usr_max)
#    return usr

#def desmontar(disco):
#    m = montados(disco)
#    # Desmonto todas las particiones del disco
#    while len(m) > 0:
#        for s in m:
#            cmd = 'umount -f -l {0}'.format(s)
#            salida = commands.getstatusoutput(cmd)
#            #print cmd, salida
#            if salida[0] == 0 and salida[1].find('Error:') != -1 : m.remove(s)
#            if salida[1].find('not found') != -1: m.remove(s)
#    commands.getstatusoutput('rm -Rf /target')
#    

#def montar(particiones):
#    part = particiones
#    while len(part) > 0:
#        for p, d in part.items():
#            cmd = 'mkdir {0}'.format(d)
#            print cmd
#            commands.getstatusoutput(cmd)
#            cmd = 'mount {0} {1}'.format(p, d)
#            print cmd
#            salida = commands.getstatusoutput(cmd)
#            if salida[0] == 0: del part[p]

## Muesta el texto seleccionado del combobox
#def get_active_text(combobox):
#    model = combobox.get_model()
#    active = combobox.get_active()
#    if active < 0:
#        return None
#    return model[active][0]

def aconnect(button, signals, function, params):
    '''
        desconecta los eventos existentes en signals y conecta con function
    '''
    for i in signals:
        if button.handler_is_connected(i):
            button.disconnect(i)
    signals.append(button.connect_object('clicked', function, params))

    return signals

def UserMessage(message, title, mtype, buttons,
                    c_1=False, f_1=False, p_1='',
                    c_2=False, f_2=False, p_2='',
                    c_3=False, f_3=False, p_3='',
                    c_4=False, f_4=False, p_4='',
                    c_5=False, f_5=False, p_5=''
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
    try:
        int(disp[-1])
        return True
    except (ValueError, IndexError):
        return False
