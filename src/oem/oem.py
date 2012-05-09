#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
import webkit
import os
import re
import time

SEGURIDAD = {
    0: '#f00',
    1: '#eeaaaa',
    2: '#eed284',
    3: '#eeeeaa',
    4: '#e6ff90',
    5: '#aaeeaa',
}
PATTERNS = [
    re.compile('([0-9])'),
    re.compile('[a-z]'),
    re.compile('[A-Z]'),
    re.compile('[+*^$@%/¿?\|_#!¡&()=",.-]+')
]
class frmMain(gtk.Window):
    nombre = ''
    usuario = ''
    pass1 = ''
    pass2 = ''
    passroot1 = ''
    passroot2 = ''
    maquina = ''
    def __init__(self):
        #Creo la ventana
        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        gtk.Window.set_position(self, gtk.WIN_POS_CENTER_ALWAYS)
        self.set_size_request(600, 440)
        self.set_decorated(False)
        
        self.visor = webkit.WebView()
        self.visor.set_size_request(590, 280)
        self.visor.connect("navigation-requested", self.on_navigation_requested)
        self.add(self.visor)
        
        path = os.path.realpath(os.path.join(os.path.dirname(__file__), 
                'usuario.html'))
        self.visor.open(path)

        self.show_all()

    def on_navigation_requested(self, view, frame, req, data=None):
        uri = req.get_uri()
        scheme, path=uri.split('://', 1)
        #print uri, scheme, path
        if scheme == 'btnapagar':
            self.visor.execute_script("document.getElementById('apagar').style.visibility = 'visible';")
            return True
        elif scheme == 'btnapagarcancelar':
            self.visor.execute_script("document.getElementById('apagar').style.visibility = 'hidden';")
            return True
        elif scheme == 'btnapagaraceptar':
            os.system('shutdown -h now')
            return True
        elif scheme == 'btnmantenimiento':
            self.visor.execute_script("document.getElementById('mantenimiento').style.visibility = 'visible';")
            return True
        elif scheme == 'btncontinuar':
            self.mantenimiento()
            return True
        elif scheme == 'btncancelar':
            self.visor.execute_script("document.getElementById('mantenimiento').style.visibility = 'hidden';")
            return True
        elif scheme == 'chgnombre':
            self.nombre = path.replace('%20', ' ')
            print self.nombre, path
            nombre = path.split('%20')
            if len(nombre) == 1:
                usuario = nombre[0]
            elif len(nombre) == 2:
                usuario = nombre[0][0] + nombre[1]
            else:
                usuario = nombre[0][0] + nombre[2]
            self.usuario = usuario
            self.visor.execute_script("document.getElementById('usuario').value = '{0}';".format(usuario.lower()))
            self.visor.execute_script("document.getElementById('maquina').value = '{0}-pc';".format(usuario.lower()))
            return True
        elif scheme == 'chgusuario':
            self.usuario = path.lower()
            self.visor.execute_script("document.getElementById('maquina').value = '{0}-pc';".format(path.lower()))
            return True
        elif scheme == 'chguserpass1':
            self.pass1 = path
            color = SEGURIDAD[self.verificar_fortaleza(path)]
            self.visor.execute_script("document.getElementById('userpass1').style.background = '{0}';".format(color))
            return True
        elif scheme == 'chguserpass2':
            self.pass2 = path
            if self.pass1 == self.pass2:
                color = '#aaeeaa'
            else:
                color = '#eeaaaa'
            self.visor.execute_script("document.getElementById('userpass2').style.background = '{0}';".format(color))
            return True
        elif scheme == 'chgrootpass1':
            self.passroot1 = path
            color = SEGURIDAD[self.verificar_fortaleza(path)]
            self.visor.execute_script("document.getElementById('rootpass1').style.background = '{0}';".format(color))
            return True
        elif scheme == 'chgrootpass2':
            self.passroot2 = path
            if self.passroot1 == self.passroot2:
                color = '#aaeeaa'
            else:
                color = '#eeaaaa'
            self.visor.execute_script("document.getElementById('rootpass2').style.background = '{0}';".format(color))
            return True
        elif scheme == 'btnaceptar':
            print "aceptando"
            if self.nombre == '':
                self.mensaje("Debe escribir su nombre")
            elif self.usuario == '':
                self.mensaje("Debe escribir un nombre de usuario")
            elif self.pass1 == '':
                self.mensaje("La contraseña del usuario no puede quedar en blanco")
            elif len(self.pass1) <= 6:
                self.mensaje("La contraseña de usuario debe tener más de 6 caracteres, se recomienda el uso de mayúsculas, minúsculas, números, y caracteres especiales como @#$%")
            elif self.pass1 != self.pass2:
                self.mensaje("Las contraseñas de usuario no coinciden")
            elif self.passroot1 == '':
                self.mensaje("La contraseña de root no puede quedar en blanco")
            elif len(self.passroot1) <= 6:
                self.mensaje("La contraseña de root debe tener más de 6 caracteres, se recomienda el uso de mayúsculas, minúsculas, números, y caracteres especiales como @#$%")
            elif self.passroot1 != self.passroot2:
                self.mensaje("Las contraseñas de root no coinciden")
            else:
                self.visor.execute_script("document.getElementById('espera').style.visibility = 'visible';")
                time.sleep(1)
                self.aceptar()
            return True
        elif scheme == 'btnmessageaceptar':
            self.visor.execute_script("document.getElementById('msgbox').style.visibility = 'hidden';")
            return True
        else:
            return False
        
    def mensaje(self, msg):
        self.visor.execute_script("document.getElementById('msgbox').style.visibility = 'visible';")
        self.visor.execute_script("document.getElementById('message').innerHTML = '"+msg+"';")

    def verificar_fortaleza(self, password):
        strenght = 0
        if len(password) > 6:
            strenght += 1
        for p in PATTERNS:
            exist = p.search(password)
            if exist:
                strenght += 1
        return strenght
        
    def mantenimiento(self, widget=None):
        w = open('/tmp/oem', 'w')
        w.write('mantenimiento')
        w.close()
        gtk.main_quit()

    def aceptar(self, widget=None):
        w = open('/tmp/oem', 'w')
        w.write('creado')
        self.crear_usuario()
        w.close()
        gtk.main_quit()

    def crear_usuario(self):
        usr = self.usuario
        pas = self.nombre
        os.system('/usr/sbin/userdel -r canaima')
        os.system('/usr/sbin/useradd -m -d /home/{0} {0} -s /bin/bash -c "{1}"'.format(usr, pas))
        os.system('/usr/sbin/adduser {0} audio'.format(usr))
        os.system('/usr/sbin/adduser {0} dialout'.format(usr))
        os.system('/usr/sbin/adduser {0} disk'.format(usr))
        os.system('/usr/sbin/adduser {0} floppy'.format(usr))
        os.system('/usr/sbin/adduser {0} cdrom'.format(usr))
        os.system('/usr/sbin/adduser {0} video'.format(usr))
        os.system('/usr/sbin/adduser {0} plugdev'.format(usr))
        os.system('/usr/sbin/adduser {0} admin'.format(usr))
        
        os.system('echo "{0}:{1}" > /tmp/passwd'.format(self.usuario, self.pass1))
        os.system('/usr/sbin/chpasswd < /tmp/passwd')
        os.system('rm -f /tmp/passwd')

        os.system('echo "root:{0}" > /tmp/passwd'.format(self.passroot1))
        os.system('/usr/sbin/chpasswd < /tmp/passwd')
        os.system('rm -f /tmp/passwd')
        
        os.system('aptitude purge canaima-instalador --assume-yes')
def main():
    '''
        Inicia la parte gráfica
    '''
    gtk.main()
    return 0

if __name__ == "__main__":
    frmMain()
    main()
