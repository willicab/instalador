#-*- coding: UTF-8 -*-

import gtk

class Main(gtk.Fixed):
    def __init__(self):
        gtk.Fixed.__init__(self)

        self.lbl1 = gtk.Label("Configuración de la cuenta de Root")
        self.lbl1.set_size_request(590, 25)
        self.put(self.lbl1, 0, 0)
        self.lbl1.show()
        
        self.lbl1 = gtk.Label("Escriba la contraseña")
        self.lbl1.set_size_request(590, 25)
        self.lbl1.set_alignment(0, 0)
        self.put(self.lbl1, 0, 25)
        self.lbl1.show()

        self.txt_passroot = gtk.Entry()
        self.txt_passroot.set_size_request(440, 25)
        #self.txt_passroot.set_invisible_char('*')
        self.txt_passroot.set_visibility(False)
        self.put(self.txt_passroot, 150, 25)
        self.txt_passroot.show()

        self.lbl1 = gtk.Label("Repita la contraseña")
        self.lbl1.set_size_request(590, 25)
        self.lbl1.set_alignment(0, 0)
        self.put(self.lbl1, 0, 50)
        self.lbl1.show()

        self.txt_passroot2 = gtk.Entry()
        self.txt_passroot2.set_size_request(440, 25)
        #self.txt_passroot2.set_invisible_char('*')
        self.txt_passroot2.set_visibility(False)
        self.put(self.txt_passroot2, 150, 50)
        self.txt_passroot2.show()

        self.linea = gtk.HSeparator()   
        self.linea.set_size_request(590, 10);
        self.put(self.linea, 0, 75)
        self.linea.show()

        self.lbl1 = gtk.Label("Configuración de la cuenta de Usuario")
        self.lbl1.set_size_request(590, 25)
        self.put(self.lbl1, 0, 80)
        self.lbl1.show()
        
        self.lbl1 = gtk.Label("Nombre Completo")
        self.lbl1.set_size_request(590, 25)
        self.lbl1.set_alignment(0, 0)
        self.put(self.lbl1, 0, 105)
        self.lbl1.show()

        self.txt_nombre = gtk.Entry()
        self.txt_nombre.set_size_request(440, 25)
        #self.txt_nombre.set_invisible_char('*')
        #self.txt_nombre.set_visibility(False)
        self.put(self.txt_nombre, 150, 105)
        self.txt_nombre.show()

        self.lbl1 = gtk.Label('Nombre de usuario')
        self.lbl1.set_size_request(590, 25)
        self.lbl1.set_alignment(0, 0)
        self.put(self.lbl1, 0, 130)
        self.lbl1.show()

        self.txt_usuario = gtk.Entry()
        self.txt_usuario.set_size_request(440, 25)
        #self.txt_usuario.set_invisible_char('*')
        #self.txt_usuario.set_visibility(False)
        self.put(self.txt_usuario, 150, 130)
        self.txt_usuario.show()

        self.lbl1 = gtk.Label("Escriba la contraseña")
        self.lbl1.set_size_request(590, 25)
        self.lbl1.set_alignment(0, 0)
        self.put(self.lbl1, 0, 155)
        self.lbl1.show()

        self.txt_passuser = gtk.Entry()
        self.txt_passuser.set_size_request(440, 25)
        #self.txt_passuser.set_invisible_char('*')
        self.txt_passuser.set_visibility(False)
        self.put(self.txt_passuser, 150, 155)
        self.txt_passuser.show()

        self.lbl1 = gtk.Label("Repita la contraseña")
        self.lbl1.set_size_request(590, 25)
        self.lbl1.set_alignment(0, 0)
        self.put(self.lbl1, 0, 180)
        self.lbl1.show()

        self.txt_passuser2 = gtk.Entry()
        self.txt_passuser2.set_size_request(440, 25)
        #self.txt_passuser2.set_invisible_char('*')
        self.txt_passuser2.set_visibility(False)
        self.put(self.txt_passuser2, 150, 180)
        self.txt_passuser2.show()

        self.linea = gtk.HSeparator()   
        self.linea.set_size_request(590, 10);
        self.put(self.linea, 0, 205)
        self.linea.show()

        self.lbl1 = gtk.Label("Configuraciones avanzadas")
        self.lbl1.set_size_request(590, 25)
        self.put(self.lbl1, 0, 210)
        self.lbl1.show()
        
        self.lbl1 = gtk.Label('Nombre de la máquina')
        self.lbl1.set_size_request(590, 25)
        self.lbl1.set_alignment(0, 0)
        self.put(self.lbl1, 0, 235)
        self.lbl1.show()

        self.txt_maquina = gtk.Entry()
        self.txt_maquina.set_text('canaima-popular')
        self.txt_maquina.set_size_request(440, 25)
        self.put(self.txt_maquina, 150, 235)
        self.txt_maquina.show()

        button = gtk.RadioButton(None, 
           "Instalación OEM (Ignora esta configuración y la realiza al inicio)")
        #button.connect("toggled", self.RadioButton_on_changed, "particion_2")
        button.set_size_request(590, 25)
        self.put(button, 0, 260)
        #button.show()

        msg = 'Necesita definir una contraseña para el superusuario (root), la '
        msg = msg + 'cuenta de administración del\nsistema, Un usuario malicioso'
        msg = msg + ' o sin la debida calificación con acceso a la cuenta de\n'
        msg = msg + 'administración puede acarrear unos resultados desastrosos,'
        msg = msg + ' así que debe tener cuidado\npara que la contraseña del '
        msg = msg + 'superusuario no sea facil de adivinar. No debe ser una '
        msg = msg + 'palabra\nde diccionario, o una palabra que pueda asociarse'
        msg = msg + ' facilmente con usted.\n\nUna buena contraseña debe '
        msg = msg + 'contener una mezcla de letras, números y signos de\n'
        msg = msg + 'puntuación, y debe cambiarse regularmente.'
        self.lbl1 = gtk.Label(msg)
        self.lbl1.set_size_request(590, 170)
        self.lbl1.set_alignment(0, 0)
        self.put(self.lbl1, 0, 30 )
        #self.lbl1.show()

