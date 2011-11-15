#-*- coding: UTF-8 -*-
import pygtk
import gtk
import threading

gtk.gdk.threads_init()

class Main(gtk.Window):
    hilo = True
    def __init__(self, titulo = '', mensaje = ''):
        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL) #Creo la ventana
        gtk.Window.set_position(self, gtk.WIN_POS_CENTER_ALWAYS)
        self.set_title(titulo)
        self.set_size_request(550, 120)
        self.set_resizable(0)
        self.set_border_width(0)
        self.set_keep_above(True)
        self.connect("destroy", self.close)
        
        self.fijo = gtk.Fixed() # Contenedor Principal
        self.add(self.fijo)
        self.fijo.show()
        
        self.barra = gtk.ProgressBar() # Barra de progreso
        self.barra.set_size_request(530, 30)
        self.fijo.put(self.barra, 10, 40)
        self.barra.set_pulse_step(0.2)
        self.barra.show()
        
        self.lblmensaje = gtk.Label(mensaje) # Etiqueta de mensaje general
        self.lblmensaje.set_size_request(530, 30)
        self.lblmensaje.set_justify(gtk.JUSTIFY_CENTER)
        self.fijo.put(self.lblmensaje, 10, 0)
        self.lblmensaje.show()

        self.lblaccion = gtk.Label('') # Mensajes de acciones
        self.lblaccion.set_size_request(530, 30)
        self.lblaccion.set_justify(gtk.JUSTIFY_CENTER)
        self.fijo.put(self.lblaccion, 10, 80)
        self.lblaccion.show()

    def accion(self, accion): # Agrega el mensaje de acción
        self.lblaccion.set_text(accion)
    
    def start(self): # Inicia la animación del progress bar
        thread = threading.Thread(target=self.anim, args=())
        thread.start()
    
    def stop(self): # finaliza la animación del progress bar
        self.hilo = False
    
    def close(self, widget=None): # finaliza la animación y cierra la ventana
        self.stop()
        self.destroy()
        
    def anim(self): # Genera la animación en el progress bar
        import time
        while self.hilo == True:
            self.barra.pulse()
            time.sleep(0.1)
        
if __name__ == "__main__":
    m = Main("Titulo de prueba", 'mensaje\nde\nprueba')
    m.show()
    m.start()
    gtk.main()
