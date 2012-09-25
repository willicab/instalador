#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os, gtk, threading, commands, webkit

from canaimainstalador.clases.particiones import Particiones
from canaimainstalador.clases.common import UserMessage, ProcessGenerator, \
    reconfigurar_paquete, desinstalar_paquete, instalar_paquete, lista_cdroms, \
    crear_etc_default_keyboard, crear_etc_hostname, crear_etc_hosts, \
    crear_etc_network_interfaces
import sys
#===============================================================================
# from canaimainstalador.common import crear_etc_default_keyboard, crear_etc_hostname
# from canaimainstalador.common import crear_etc_hosts, crear_etc_network_interfaces
# from canaimainstalador.common import crear_fstab, lista_cdroms, ProcessGenerator, UserMessage
#===============================================================================

class PasoInstalacion(gtk.Fixed):
    def __init__(self, CFG):
        gtk.Fixed.__init__(self)
        self.w = CFG['wizard']
        self.metodo = CFG['metodo']
        self.acciones = CFG['acciones']
        self.teclado = CFG['teclado']
        self.passroot = CFG['passroot']
        self.nombre = CFG['nombre']
        self.usuario = CFG['usuario']
        self.passuser = CFG['passuser']
        self.maquina = CFG['maquina']
        self.oem = CFG['oem']
        self.chkgdm = CFG['chkgdm']
        self.p = Particiones()
        self.paquetesreconf = [
            'cunaguaro', 'guacharo', 'canaima-estilo-visual', 'canaima-plymouth',
            'canaima-chat-gnome', 'canaima-bienvenido-gnome', 'canaima-escritorio-gnome',
            'canaima-base'
            ]
        self.mountpoint = '/target'
        self.squashfs = '/live/image/live/filesystem.squashfs'
        self.connection = True

        path = os.path.realpath(
            os.path.join(os.path.dirname(__file__), '..', 'data', 'slider.html')
            )

        self.visor = webkit.WebView()
        self.visor.set_size_request(690, 280)
        self.put(self.visor, 0, 0)
        self.visor.open(path)

        msg = 'Ha culminado la instalación, puede reiniciar ahora el sistema o seguir probando canaima y reiniciar más tarde.'
        self.lblInfo = gtk.Label(msg)
        self.lblInfo.set_size_request(690, 280)
        self.put(self.lblInfo, 0, 0)

        self.lblDesc = gtk.Label()
        self.lblDesc.set_size_request(690, 30)
        self.put(self.lblDesc, 0, 290)

        self.w.siguiente.set_label('Reiniciar más tarde')
        self.w.siguiente.set_size_request(150, 30)

        self.w.anterior.set_label('Reiniciar ahora')
        self.w.anterior.set_size_request(150, 30)

        self.w.anterior.hide()
        self.w.siguiente.hide()
        self.w.cancelar.hide()

        self.thread = threading.Thread(target=self.instalar, args=())
        self.thread.start()

    def instalar(self):
        try:
            pass #borrar
            #TODO:
            #===================================================================
            # response = urllib2.urlopen(HeadRequest(requesturl))
            #===================================================================
        except:
            self.connection = False

        self.lblDesc.set_text('Creando particiones en disco ...')
        for a in self.acciones:
            nombre = a[0]
            particion = a[1]
            #montaje = a[2] Unused Variable
            inicio = a[3]
            fin = a[4]
            fs = a[5]
            tipo = a[6]

            if nombre == 'crear':
                if not self.p.crear_particion(
                    drive=self.metodo['disco'][0], start=inicio,
                    end=fin, fs=fs, partype=tipo
                    ):
                    UserMessage(
                        message='Ocurrió un error creando una partición.',
                        title='ERROR',
                        mtype=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK,
                        c_1=gtk.RESPONSE_OK, f_1=sys.exit, p_1=(1,)
                    )

            elif nombre == 'borrar':
                if not self.p.borrar_particion(
                    particion=particion
                    ):
                    UserMessage(
                        message='Ocurrió un error borrando una partición.',
                        title='ERROR',
                        mtype=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK,
                        c_1=gtk.RESPONSE_OK, f_1=sys.exit, p_1=(1,)
                    )

            elif nombre == 'redimensionar':
                if not self.p.redimensionar_particion(
                    part=particion, newend=fin
                    ):
                    UserMessage(
                        message='Ocurrió un error redimensionando una partición.',
                        title='ERROR',
                        mtype=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK,
                        c_1=gtk.RESPONSE_OK, f_1=sys.exit, p_1=(1,)
                    )

        self.lblDesc.set_text('Copiando archivos en disco ...')
        if not ProcessGenerator(
            'unsquashfs -f -i -d {0} {1}'.format(self.mountpoint, self.squashfs)
            ):
            UserMessage(
                message='Ocurrió un error copiando los archivos al disco.',
                title='ERROR',
                mtype=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK,
                c_1=gtk.RESPONSE_OK, f_1=sys.exit, p_1=(1,)
            )

        self.lblDesc.set_text('Configurando detalles del sistema operativo ...')
        for pkg in self.paquetesreconf:
            if not reconfigurar_paquete(pkg):
                UserMessage(
                    message='Ocurrió un error reconfigurando un paquete.',
                    title='ERROR',
                    mtype=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK,
                    c_1=gtk.RESPONSE_OK, f_1=sys.exit, p_1=(1,)
                )

        self.lblDesc.set_text('Removiendo instalador del sistema de archivos ...')
        if not desinstalar_paquete('canaima-instalador'):
            UserMessage(
                message='Ocurrió un error desinstalando un paquete.',
                title='ERROR',
                mtype=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK,
                c_1=gtk.RESPONSE_OK, f_1=sys.exit, p_1=(1,)
            )

        self.lblDesc.set_text('Instalando gestor de arranque ...')
        ProcessGenerator('mount -o bind /dev {0}/dev'.format(self.mountpoint))
        ProcessGenerator('mount -o bind /dev/pts {0}/dev/pts'.format(self.mountpoint))
        ProcessGenerator('mount -o bind /proc {0}/proc'.format(self.mountpoint))
        ProcessGenerator('mount -o bind /sys {0}/sys'.format(self.mountpoint))
        ProcessGenerator(
            'chroot {0} echo "burg-pc burg/linux_cmdline string quiet splash" > /tmp/debconf'.format(self.mountpoint)
            )
        ProcessGenerator(
            'chroot {0} echo "burg-pc burg/linux_cmdline_default string quiet splash vga=791" > /tmp/debconf'.format(self.mountpoint)
            )
        ProcessGenerator(
            'chroot {0} echo "burg-pc burg-pc/install_devices multiselect {1}" > /tmp/debconf'.format(self.mountpoint, self.metodo['disco'][0])
            )
        ProcessGenerator(
            'chroot {0} debconf-set-selections < /tmp/debconf'.format(self.mountpoint)
            )
        ProcessGenerator(
            'rm -rf {0}/tmp/debconf'.format(self.mountpoint)
            )
        instalar_paquete('/live/image/pool/main/b/burg/', 'burg')
        instalar_paquete('/live/image/pool/main/b/burg/', 'burg')
        instalar_paquete('/live/image/pool/main/b/burg/', 'burg')
        instalar_paquete('/live/image/pool/main/b/burg/', 'burg')
        instalar_paquete('/live/image/pool/main/b/burg/', 'burg')
        instalar_paquete('/live/image/pool/main/b/burg/', 'burg')
        ProcessGenerator(
            'burg-install --force --root-directory="{0}" {1}'.format(
                self.mountpoint, self.metodo['disco'][0]
                )
            )
        ProcessGenerator(
            'chroot {0} update-burg'.format(self.mountpoint)
            )

        self.lblDesc.set_text('Generando imagen de arranque ...')
        uname_r = commands.getstatusoutput('echo $(uname -r)')[1]
        initrd = 'initrd.img-' + uname_r
        ProcessGenerator(
            'chroot {0} /usr/sbin/mkinitramfs -o /boot/{1} {2}'.format(self.mountpoint, initrd, uname_r)
            )

        self.lblDesc.set_text('Configurando particiones, usuarios y grupos ...')
        self.cdroms = lista_cdroms()
        self.particiones = self.p.lista_particiones()
        #TODO:
        #=======================================================================
        # fstab = crear_fstab(
        #    mnt=self.mountpoint, cfg='/etc/fstab',
        #    particiones=self.particiones, cdroms=self.cdroms
        #    )
        #=======================================================================
        ProcessGenerator('cp -f /etc/passwd {0}/etc/passwd'.format(self.mountpoint))
        ProcessGenerator('cp -f /etc/group {0}/etc/group'.format(self.mountpoint))
        ProcessGenerator('cp -f /etc/inittab {0}/etc/inittab'.format(self.mountpoint))
        ProcessGenerator('rm -rf {0}/etc/mtab'.format(self.mountpoint))
        ProcessGenerator('touch {0}/etc/mtab'.format(self.mountpoint))

        self.lblDesc.set_text('Configurando teclado ...')
        a = crear_etc_default_keyboard(
            mnt=self.mountpoint, cfg='/etc/canaima-base/alternatives/keyboard',
            key=self.teclado
            )

        self.lblDesc.set_text('Configurando interfaces de red ...')
        a = crear_etc_hostname(mnt=self.mountpoint, cfg='/etc/hostname', maq=self.maquina)
        a = crear_etc_hosts(mnt=self.mountpoint, cfg='/etc/hosts', maq=self.maquina)
        a = crear_etc_network_interfaces(mnt=self.mountpoint, cfg='/etc/network/interfaces')

        if self.oem:
            self.adm_user = 'root'
            self.adm_password = 'root'
            self.nml_user = 'canaima'
            self.nml_password = 'canaima'
            self.nml_name = 'Mantenimiento'
            instalar_paquete(
                '/live/image/pool/main/c/canaima-primeros-pasos/',
                'canaima-primeros-pasos'
                )
        else:
            self.adm_user = 'root'
            self.adm_password = self.passroot
            self.nml_user = self.usuario
            self.nml_password = self.passuser
            self.nml_name = self.nombre

        if self.chkgdm:
            instalar_paquete(
                '/live/image/pool/main/c/canaima-accesibilidad-gdm-gnome/',
                'canaima-accesibilidad-gdm-gnome'
                )

        self.lblDesc.set_text('Creando usuario administrador ...')
        ProcessGenerator('chroot {0} echo "{1}:{2}" > /tmp/passwd'.format(self.mountpoint, self.adm_user, self.adm_password))
        ProcessGenerator('chroot {0} /usr/sbin/chpasswd < /tmp/passwd'.format(self.mountpoint))
        ProcessGenerator('rm -rf {0}/tmp/passwd'.format(self.mountpoint))

        self.lblDesc.set_text('Creando usuario "{0}" ...'.format(self.nml_user))
        ProcessGenerator('chroot {0} /usr/sbin/userdel -r canaima'.format(self.mountpoint))
        ProcessGenerator('chroot {0} /usr/sbin/useradd -m -d /home/{1} {2} -s /bin/bash -c "{3}"'.format(self.mountpoint, self.nml_user, self.nml_user, self.nml_name))
        ProcessGenerator('chroot {0} echo "{1}:{2}" > /tmp/passwd'.format(self.mountpoint, self.nml_user, self.nml_password))
        ProcessGenerator('chroot {0} /usr/sbin/chpasswd < /tmp/passwd'.format(self.mountpoint))
        ProcessGenerator('rm -rf {0}/tmp/passwd'.format(self.mountpoint))

        if self.connection:
            self.lblDesc.set_text('Actualizando sistema operativo desde repositorios ...')
            ProcessGenerator('chroot {0} dhclient'.format(self.mountpoint))
            ProcessGenerator('chroot {0} aptitude update'.format(self.mountpoint))
            ProcessGenerator('chroot {0} aptitude full-upgrade'.format(self.mountpoint))

        self.lblDesc.set_text('Desmontando sistema de ficheros ...')
        ProcessGenerator('umount -l {0}/dev/pts'.format(self.mountpoint))
        ProcessGenerator('umount -l {0}/dev'.format(self.mountpoint))
        ProcessGenerator('umount -l {0}/proc'.format(self.mountpoint))
        ProcessGenerator('umount -l {0}/sys'.format(self.mountpoint))
        ProcessGenerator('umount -l {0}'.format(self.mountpoint))
        ProcessGenerator('sync > /dev/null')

        self.visor.hide()
        self.w.anterior.show()
        self.w.siguiente.show()

