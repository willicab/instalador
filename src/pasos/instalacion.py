#-*- coding: UTF-8 -*-

import os
import gtk
import clases.particiones
import clases.general as gen
import clases.install.fstab
import clases.install.particion_todo
import clases.install.particion_auto
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
        self.lbl1 = gtk.Label(msg)
        self.lbl1.set_size_request(590, 280)
        self.put(0, 0)
        #self.lbl1.show()
        
        path = os.path.realpath(os.path.join(os.path.dirname(__file__), 
                '..', 'data', 'preview', 'carrusel.html'))
        self.visor.open(path)        
    
        self.thread = threading.Thread(target=self.instalar, args=())
        self.thread.start()

    def instalar(self):
        self.par.mostrar_barra()
        self.par.info_barra("Creando particiones en el disco duro ...")
        # Comenzando el particionado
        if self.metodo == 'todo':
            part_todo = clases.install.particion_todo.Main(self.cfg, self.par)
            if self.tipo == 'particion_1':
                self.salida = part_todo.particion_1()
            if self.tipo == 'particion_2':
                self.salida = part_todo.particion_2()
            if self.tipo == 'particion_3':
                self.salida = part_todo.particion_3()
        else:
            part_auto = clases.install.particion_auto.Main(self.cfg, self.par)
            if self.tipo == 'particion_1':
                self.salida = part_auto.particion_1()
            if self.tipo == 'particion_2':
                self.salida = part_auto.particion_2()
            if self.tipo == 'particion_3':
                self.salida = part_auto.particion_3()
        self.particiones_montadas = self.salida [0]
        self.particion_boot = self.salida [1]
        # Copiando los archivos
        self.par.info_barra("Instalando Canaima GNU/Linux ...")
        self.par.accion('Copiando los archivos al disco')
        self.copiar()
        fstab = clases.install.fstab.Main(self.particiones_montadas)
        fstab.crear_archivo()
        self.par.accion('Copiando archivos group y etc')
        os.system('cp /etc/passwd /etc/group /target/etc')
        os.system('mount -o bind /dev /target/dev')
        os.system('mount -o bind /proc /target/proc')
        os.system('mount -o bind /sys /target/sys')
        os.system('mkdir /target/boot/burg')
        self.par.accion('instalando burg')
        script = os.path.realpath(os.path.join(os.path.dirname(__file__), 
                '..', 'scripts', 'install-grub-ini.sh'))
                
        print 'termina install-grub-ini****************************************'
        os.system('echo "0" > /proc/sys/kernel/printk')
        os.system('chmod +x {0}'.format(script))
        os.system('sh {0} {1}'.format(script, self.particion_boot))
        cmd = "burg-install --force --root-directory=/target {0}"
        os.system(cmd.format(self.disco))
        
        print 'termina burg-install********************************************'
        uname_r = commands.getstatusoutput('echo $(uname -r)')[1]
        vmlinuz = 'vmlinuz-' + uname_r 
        initrd = 'initrd.img-'  + uname_r
        print "vmlinuz {0} | initrd {1}".format(vmlinuz, initrd)

        script = os.path.realpath(os.path.join(os.path.dirname(__file__), 
                '..', 'scripts', 'install-grub.sh'))
        os.system('chmod +x {0}'.format(script))
        os.system('sh {0} /target {1} '.format(script, self.disco))

        os.system('echo "6" > /proc/sys/kernel/printk')

        print 'Generando initrd************************************************'
        self.par.accion('Generando initrd')
        os.system('rm -f /target/boot/{0}'.format(initrd))
        os.system('chroot /target /usr/sbin/mkinitramfs -o /boot/{0} {1}'. \
            format(initrd, uname_r))

        print 'Creando Usuario Root********************************************'
        self.par.accion('Creando usuarios')
        script = os.path.realpath(os.path.join(os.path.dirname(__file__), 
                '..', 'scripts', 'make-user.sh'))
        os.system('sh {0} "root" "{1}" "/target"'. \
            format(script, self.passroot))
        os.system('sh {0} "{1}" "{2}" "/target" "{3}"'. \
            format(script, self.usuario, self.passuser, self.nombre))

        self.par.accion('Ejecutando últimas configuraciones')
        os.system('rm -f /target/etc/mtab')
        os.system('touch /target/etc/mtab')

        os.system('cp -f /.dirs/image/etc/inittab /target/etc/inittab')
        os.system('chroot /target install-keymap {0}'.format(self.teclado))
        self.interfaces()
        self.hostname()
        os.system('chroot /target dhclient -v')
        os.system('chroot /target aptitude update')
        #os.system('chroot /target aptitude remove canaima-instalador')
        #os.system('chroot /target aptitude install canaima-contrasena -y')
        print 'desmontar /target/dev'
        os.system('umount /target/dev')
        print 'desmontar /target/proc'
        os.system('umount /target/proc')
        print 'desmontar /target/sys'
        os.system('umount /target/sys ')
        print 'desmontar /target'
        os.system('umount -l /target ')
        print 'sync > /dev/null'
        os.system('sync > /dev/null')
        print 'ocultar barra'
        self.par.ocultar_barra()

        self.visor.hide()
        self.lbl1.show()
        frmMain.btn_siguiente.set_label('Reiniciar más tarde')
        frmMain.btn_siguiente.set_size_request(150, 30)
        frmMain.botonera.move(frmMain.btn_siguiente, 440, 10)
        frmMain.btn_anterior.set_label('Reiniciar Ahora')
        frmMain.btn_anterior.set_size_request(150, 30)
        frmMain.botonera.move(frmMain.btn_anterior, 280, 10)
        frmMain.btn_cancelar.hide()
        
        #msg = 'Ha culminado la instalación, puede reiniciar ahora el sistema\n'
        #msg = msg + 'o seguir probando canaima y reiniciar más tarde.'
        #label = gtk.Label(msg)
        #dialog = gtk.Dialog("Reiniciar el sistema",
        #                None,
        #                gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
        #                ("Reiniciar ahora", gtk.RESPONSE_ACCEPT,
        #                 "Reiniciar más tarde", gtk.RESPONSE_REJECT))
        #dialog.vbox.pack_start(label)
        #label.show()
        #response = dialog.run()
        #dialog.destroy()
        #print response, gtk.RESPONSE_ACCEPT, gtk.RESPONSE_REJECT, (response == gtk.RESPONSE_ACCEPT)
        #if response == gtk.RESPONSE_ACCEPT:
        #    os.system('reboot')
        #    #self.par.close()
        #else:
        #    pass
        #    #self.par.close()

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
        sal = '# This file describes the network interfaces available on your '
        sal = sal + ' system\n# and how to activate them. For more information,' 
        sal = sal + 'see interfaces(5).\n\n# The loopback network interface\n'
        sal = sal + 'auto lo\niface lo inet loopback\n\n'
        sal = sal + '# The primary network interface\n'
        sal = sal + 'auto	{0}'.format(eth)
        sal = sal + 'iface {0} inet dhcp'.format(eth)
        des = '/target/etc/network/interfaces'
        os.system('echo {0} > {1}'.format(sal, des))
        os.system('cat {0}'.format(des))
    
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

