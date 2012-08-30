#-*- coding: UTF-8 -*-

import commands, re

root1_min = '2.5GB'
root1_max = '18GB'
root2_min = '512MB'
root2_max = '3GB'
usr_min = '2GB'
usr_max = '15GB'
minimo = '5GB'

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
    unidad = re.sub('[0123456789.]', '', num.replace(',', '.').upper())
    peso = float(re.sub('[TGMKB]', '', num.replace(',', '.').upper()))
    if unidad == 'TB': kb = peso * 1024.0 * 1024.0 * 1024.0	# TB a KB
    if unidad == 'GB': kb = peso * 1024.0 * 1024.0		# GB a KB
    if unidad == 'MB': kb = peso * 1024.0			# MB a KB
    if unidad == 'KB': kb = peso				# KB a KB
    if unidad == 'B': kb = peso / 1024.0			# B a KB
    return kb
    
def redondear(w, dec=0):
    if type(w) == int : return w
    if dec == 0:
        return int(w) + 1 if int(str(w).split('.')[1][0]) >= 5 else int(w)
    else:
        return float(str(w).split('.')[0] + '.' + str(w).split('.')[1][0:dec])

def hum(valor):
    if valor <= 1024.0: return '{0}kB'.format(redondear(valor, 2))
    if valor <= 1048576.0: return '{0}MB'.format(redondear(valor / 1024, 2))
    if valor<=1073741824.0: return '{0}GB'.format(redondear(valor/1024/1024,2))
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

def part_root1(total):
    root = (kb(total) * kb(root1_min)) / kb(minimo)
    if root < kb(root1_min): 
        root = kb(root1_min)
    if root > kb(root1_max): 
        root = kb(root1_max)
    return root

def part_root2(total):
    root = (kb(total) * kb(root2_min)) / kb(minimo)
    if root < kb(root2_min): 
        root = kb(root2_min)
    if root > kb(root2_max): 
        root = kb(root2_max)
    return root

def part_usr(total):
    usr = (kb(total) * kb(usr_min)) / kb(minimo)
    if usr < kb(usr_min): 
        usr = kb(usr_min)
    if usr > kb(usr_max): 
        usr = kb(usr_max)
    return usr

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
            cmd = 'mkdir {0}'.format(d)
            print cmd
            commands.getstatusoutput(cmd)
            cmd = 'mount {0} {1}'.format(p, d)
            print cmd
            salida = commands.getstatusoutput(cmd)
            if salida[0] == 0: del part[p]

# Muesta el texto seleccionado del combobox
def get_active_text(combobox):
    model = combobox.get_model()
    active = combobox.get_active()
    if active < 0:
        return None
    return model[active][0]


