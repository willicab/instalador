#-*- coding: UTF-8 -*-

def kb(num):
    unidad = num[-2:]
    num = num[:-2].replace(',', '.')
    num = int(float(num))
    if unidad == 'GB': return num * 1048576 # Gb a Kb
    if unidad == 'MB': return num * 1024    # Mb a Kb
    if unidad == 'kB': return num           # Kb a Kb
    return num / 1024                       # Bytes a Kb
    
def redondear(w, dec=0):
    if dec == 0:
        return int(w) + 1 if int(str(w).split('.')[1][0]) >= 5 else int(w)
    else:
        return str(w).split('.')[0] + '.' + str(w).split('.')[1][0:dec]

def hum(valor):
    valor = valor
    if valor <= 1024.0: return '{0} kB'.format(redondear(valor, 1))
    if valor <= 1048576.0: return '{0} MB'.format(redondear(valor / 1024, 1))
    if valor <= 1073741824.0: return '{0} GB'.format(redondear(valor / 1024 / 1024, 1))
    return valor
    #if valor <= 1099511627776: return '{0} MB'.format(valor / 1024 / 1024)
