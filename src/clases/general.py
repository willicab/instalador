#-*- coding: UTF-8 -*-

import commands

def kb(num):
    if type(num) == int or type(num) == float : return float(num)
    unidad = num[-2:]
    num = num[:-2].replace(',', '.')
    num = (float(num))
    if unidad == 'GB': return num * 1048576.0 # Gb a Kb
    if unidad == 'MB': return num * 1024.0    # Mb a Kb
    if unidad == 'kB': return num             # Kb a Kb
    return num / 1024.0                       # Bytes a Kb

def h2kb(num):
    '''
        Convierte un número escrito en formato para lectura por humanos a 
        kilobytes.
        Argumentos:
        - num: un número en formato para lectura por humanos de tipo string
        Salida: el valor en kB de tipo float
    '''
    if type(num) == int or type(num) == float : return float(num)
    unidad, num = num[-2:], float(num[:-2].replace(',', '.'))
    if unidad == 'GB': return num * 1048576.0 # GB a kB
    if unidad == 'MB': return num * 1024.0    # MB a kB
    if unidad == 'kB': return num             # kB a kB
    return num / 1024.0                       # Bytes a kB
    
def redondear(w, dec=0):
    if type(w) == int : return w
    if dec == 0:
        return int(w) + 1 if int(str(w).split('.')[1][0]) >= 5 else int(w)
    else:
        return float(str(w).split('.')[0] + '.' + str(w).split('.')[1][0:dec])

def hum(valor):
    if valor <= 1024.0: return '{0}kB'.format(redondear(valor, 2))
    if valor <= 1048576.0: return '{0}MB'.format(redondear(valor / 1024, 2))
    if valor <= 1073741824.0: return '{0}GB'.format(redondear(valor / 1024 / 1024, 2))
    return valor
    #if valor <= 1099511627776: return '{0} MB'.format(valor / 1024 / 1024)

def ram():
    return commands.getstatusoutput("free -k")[1].split('\n')[1].split()[1]
    
def montados(disco=''):
    p = []
    salida = commands.getstatusoutput('mount')[1].split('\n')
    for m in salida:
        #print m, disco, m.split(' ')[0][:-1], m.split(' ')[2]
        if disco == '': 
            p.append(m.split(' ')[2])
        elif disco == m.split(' ')[0][:-1]:
            p.append(m.split(' ')[2])
    return p         

def desmontar(disco):
    m = montados(disco)
    # Desmonto todas las particiones del disco
    while len(m) > 0:
        for s in m:
            cmd = 'umount -f -l {0}'.format(s)
            salida = commands.getstatusoutput(cmd)
            #print cmd, salida
            if salida[0] == 0 and salida[1].find('Error:') != -1 : m.remove(s)
            if salida[1].find('not found') != -1: m.remove(s)
    commands.getstatusoutput('rm -Rf /target')
    

def montar(particiones):    
    part = particiones
    while len(part) > 0:
        for p, d in part.items():
            commands.getstatusoutput('mkdir {0}'.format(d))
            cmd = 'mount {0} {1}'.format(p, d)
            salida = commands.getstatusoutput(cmd)
            #print cmd, salida
            if salida[0] == 0: del part[p]

