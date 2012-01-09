#-*- coding: UTF-8 -*-

import os
import gtk
import clases.particiones
import clases.general as gen
import clases.install.fstab
import clases.install.particion_todo as particion_todo
import clases.install.particion_auto as particion_auto
import threading
import commands
import webkit

class Main(gtk.Fixed):
    root1 = '20GB'
    root2 = '3GB'
    usr = '18GB'
    boot = '256MB'
    part = clases.particiones.Main()
    particiones_montadas = {}

    def __init__(self, cfg, parent):
        gtk.Fixed.__init__(self)
        self.par = parent
        self.cfg = cfg
        self.metodo = cfg['metodo']
        self.tipo = cfg['tipo']
        self.teclado = cfg['teclado']
        self.disco = cfg['disco']
        self.passroot = cfg['passroot']
        self.nombre = cfg['nombre']
        self.usuario = cfg['usuario']
        self.passuser = cfg['passuser']
        self.maquina = cfg['maquina']

        self.visor = webkit.WebView()
        self.visor.set_size_request(590, 280)
        self.put(self.visor, 0, 0)
        self.visor.show()
        
        msg = 'Ha culminado la instalación, puede reiniciar ahora el sistema\n'
        msg = msg + 'o seguir probando canaima y reiniciar más tarde.'
        self.lblInfo = gtk.Label(msg)
        self.lblInfo.set_size_request(590, 280)
        self.put(self.lblInfo, 0, 0)
        #self.lblInfo.show()
        
        path = os.path.realpath(os.path.join(os.path.dirname(__file__), 
                '..', 'data', 'preview', 'carrusel.html'))
        self.visor.open(path)        
    
        self.thread = threading.Thread(target=self.instalar, args=())
        self.thread.start()

    def instalar(self):
        self.par.mostrar_barra()

        self.par.btn_siguiente.set_label('Reiniciar más tarde')
        self.par.btn_siguiente.set_size_request(150, 30)
        self.par.botonera.move(self.par.btn_siguiente, 440, 10)
        self.par.btn_anterior.set_label('Reiniciar Ahora')
        self.par.btn_anterior.set_size_request(150, 30)
        self.par.botonera.move(self.par.btn_anterior, 280, 10)
        self.par.btn_cancelar.hide()
        
        self.par.info_barra("Creando particiones en el disco duro ...")
        # Comenzando el particionado
        if self.metodo == 'todo':
            part_todo = particion_todo.Main(self.cfg, self.par, False)
            if self.tipo == 'particion_1':
                self.salida = part_todo.particion_1()
            if self.tipo == 'particion_2':
                self.salida = part_todo.particion_2()
            if self.tipo == 'particion_3':
                self.salida = part_todo.particion_3()
        elif self.metodo == 'vacio':
            part_todo = particion_todo.Main(self.cfg, self.par, True)
            if self.tipo == 'particion_1':
                self.salida = part_todo.particion_1()
            if self.tipo == 'particion_2':
                self.salida = part_todo.particion_2()
            if self.tipo == 'particion_3':
                self.salida = part_todo.particion_3()
        else:
            part_auto = particion_auto.Main(self.cfg, self.par)
            if self.tipo == 'particion_1':
                self.salida = part_auto.particion_1()
            if self.tipo == 'particion_2':
                self.salida = part_auto.particion_2()
            if self.tipo == 'particion_3':
                self.salida = part_auto.particion_3()
        self.particiones_montadas = self.salida [0]
        self.particion_boot = self.salida [1]
# Aumenta la Barra 10
        # Copiando los archivos
        self.par.info_barra("Instalando Canaima GNU/Linux ...")
        self.par.accion('Copiando los archivos al disco')
        self.copiar()
# Aumenta la Barra 30
        fstab = clases.install.fstab.Main(self.particiones_montadas)
        fstab.crear_archivo()
# Aumenta la Barra 40
        self.par.accion('Copiando archivos group y etc')
        os.system('cp /etc/passwd /etc/group /target/etc')
        os.system('mount -o bind /dev /target/dev')
        os.system('mount -o bind /proc /target/proc')
        os.system('mount -o bind /sys /target/sys')
        os.system('mkdir -p /target/boot/burg')
# Aumenta la Barra 50
        self.par.accion('instalando burg')
        script = os.path.realpath(os.path.join(os.path.dirname(__file__), 
                '..', 'scripts', 'install-grub-ini.sh'))
        os.system('echo "0" > /proc/sys/kernel/printk')
        os.system('chmod +x {0}'.format(script))
        os.system('sh {0} {1}'.format(script, self.particion_boot))
        cmd = "burg-install --force --root-directory=/target {0}"
        os.system(cmd.format(self.disco))
        uname_r = commands.getstatusoutput('echo $(uname -r)')[1]
        vmlinuz = 'vmlinuz-' + uname_r 
        initrd = 'initrd.img-'  + uname_r
        script = os.path.realpath(os.path.join(os.path.dirname(__file__), 
                '..', 'scripts', 'install-grub.sh'))
        os.system('chmod +x {0}'.format(script))
        os.system('sh {0} /target {1} '.format(script, self.disco))
        os.system('echo "6" > /proc/sys/kernel/printk')
# Aumenta la Barra 70
        self.par.accion('Generando initrd')
        os.system('rm -f /target/boot/{0}'.format(initrd))
        os.system('chroot /target /usr/sbin/mkinitramfs -o /boot/{0} {1}'. \
            format(initrd, uname_r))
# Aumenta la Barra 80
        self.par.accion('Creando usuarios')
        script = os.path.realpath(os.path.join(os.path.dirname(__file__), 
                '..', 'scripts', 'make-user.sh'))
        os.system('sh {0} "root" "{1}" "/target"'. \
            format(script, self.passroot))
        os.system('sh {0} "{1}" "{2}" "/target" "{3}"'. \
            format(script, self.usuario, self.passuser, self.nombre))
# Aumenta la Barra 90
        self.par.accion('Ejecutando últimas configuraciones')
        os.system('rm -f /target/etc/mtab')
        os.system('touch /target/etc/mtab')
        os.system('cp -f /.dirs/image/etc/inittab /target/etc/inittab')
        os.system('chroot /target install-keymap {0}'.format(self.teclado))
        self.interfaces()
        self.hostname()
        os.system('chroot /target dhclient -v')
        os.system('chroot /target aptitude update')
# Aumenta la Barra 100
        #os.system('chroot /target aptitude remove canaima-instalador')
        #os.system('chroot /target aptitude install canaima-contrasena -y')
        os.system('umount -l /target/dev')
        os.system('umount -l /target/proc')
        os.system('umount -l /target/sys ')
        os.system('umount -l /target/boot ')
        os.system('umount -l /target/usr ')
        os.system('umount -l /target/home ')
        os.system('umount -l /target ')
        os.system('sync > /dev/null')
        self.visor.hide()
        self.lblInfo.show()
        self.par.ocultar_barra()

    def copiar(self):
        cmd = 'unsquashfs -f -i -d /target /live/image/live/filesystem.squashfs'
        salida = os.popen(cmd)
        #while 1:
        #    linea = salida.readline()
        #    if not linea: break
        #    cmd = linea.split('\n')[0]
        #    print cmd
        #    self.par.accion(cmd)

    def interfaces(self):
        eth = commands.getstatusoutput('ifconfig -a | grep eth')[1].split()[0]
        des = '/target/etc/network/interfaces'
        os.system('echo auto {0} > {1}'.format(eth, des))
        os.system('echo iface {0} inet dhcp >> {1}'.format(eth, des))
    
    def hostname(self):
        cmd = 'echo "{0}" > /target/etc/hostname'.format(self.maquina)
        print cmd
        os.system('{0}'.format(cmd))

        cmd = 'echo "127.0.0.1\t\t{0}\t\tlocalhost'.format(self.maquina)
        cmd = cmd + '::1\t\tlocalhost\t\tip6-localhost ip6-loopback'
        cmd = cmd + 'fe00::0\t\tip6-localnet'
        cmd = cmd + 'ff00::0\t\tip6-mcastprefix'
        cmd = cmd + 'ff02::1\t\tip6-allnodes'
        cmd = cmd + 'ff02::2\t\tip6-allrouters'
        cmd = cmd + 'ff02::3\t\tip6-allhosts" > /target/etc/hosts    '
        print cmd
        os.system('{0}'.format(cmd))

