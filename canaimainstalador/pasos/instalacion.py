#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ==============================================================================
# PAQUETE: canaima-instalador
# ARCHIVO: canaimainstalador/pasos/instalacion.py
# COPYRIGHT:
#       (C) 2012 William Abrahan Cabrera Reyes <william@linux.es>
#       (C) 2012 Erick Manuel Birbe Salazar <erickcion@gmail.com>
#       (C) 2012 Luis Alejandro Martínez Faneyth <luis@huntingbears.com.ve>
# LICENCIA: GPL-3
# ==============================================================================
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# COPYING file for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# CODE IS POETRY

import os, gtk, webkit, sys, Queue, glib, pango, threading

from canaimainstalador.clases.particiones import Particiones
from canaimainstalador.clases.common import UserMessage, ProcessGenerator, \
    reconfigurar_paquetes, desinstalar_paquetes, instalar_paquetes, lista_cdroms, \
    crear_etc_default_keyboard, crear_etc_hostname, crear_etc_hosts, \
    crear_etc_network_interfaces, crear_etc_fstab, assisted_mount, \
    assisted_umount, preseed_debconf_values, debug_list, mounted_targets, \
    mounted_parts, crear_usuarios, ThreadGenerator
from canaimainstalador.config import INSTALL_SLIDES, BAR_ICON

gtk.gdk.threads_init()

class PasoInstalacion(gtk.Fixed):
    def __init__(self, CFG):
        gtk.Fixed.__init__(self)
        q_button_a = Queue.Queue()
        q_button_b = Queue.Queue()
        q_view = Queue.Queue()
        q_label = Queue.Queue()
        event = threading.Event()
        CFG['w'].hide_all()

        params = {
                'title': 'Instalación de Canaima',
                'q_button_a': q_button_a,
                'q_button_b': q_button_b,
                'q_view': q_view,
                'q_label': q_label,
                'event': event
                }

        window = install_window(**params)

        ThreadGenerator(
            reference = None, function = window.show_html, params = {}
            )

        ThreadGenerator(
            reference = None, function = install_process,
            params = {
                'CFG': CFG,
                'q_button_a': q_button_a,
                'q_button_b': q_button_b,
                'q_view': q_view,
                'q_label': q_label
                },
            event = event
            )

class install_window(object):
    def __init__(self, title, q_button_a, q_button_b, q_view, q_label, event):
        window = gtk.Window()
        window.set_border_width(0)
        window.set_title(title)
        window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        window.set_size_request(700, 470)
        window.set_resizable(False)
        window.set_icon_from_file(BAR_ICON)
        window.connect("destroy", self.disable_close)
        window.connect("delete-event", self.disable_close)

        box = gtk.Fixed()
        window.add(box)

        attr = pango.AttrList()
        size = pango.AttrSize(20000, 0, -1)
        attr.insert(size)

        str_message = 'La instalación de Canaima ha terminado'
        message = gtk.Label(str_message)
        message.set_size_request(640, 40)
        message.set_alignment(0, 0)
        message.set_line_wrap(True)
        message.set_attributes(attr)
        box.put(message, 50, 200)

        str_intro = 'Puedes seguir probando Canaima presionando "Reiniciar más tarde" o disfrutar de tu sistema operativo instalado presionando "Reiniciar ahora".'
        intro = gtk.Label(str_intro)
        intro.set_size_request(640, 40)
        intro.set_alignment(0, 0)
        intro.set_line_wrap(True)
        box.put(intro, 50, 250)

        view = webkit.WebView()
        view.set_size_request(700, 430)
        box.put(view, 0, 0)

        linea = gtk.HSeparator()
        linea.set_size_request(700, 5)
        box.put(linea, 0, 435)

        label = gtk.Label()
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.set_size_request(700, 20)
        box.put(label, 0, 440)

        button_a = gtk.Button()
        button_a.set_size_request(150, 30)
        button_a.set_label('Reiniciar más tarde')
        button_a.connect('clicked', self.close)
        box.put(button_a, 390, 440)

        button_b = gtk.Button()
        button_b.set_size_request(150, 30)
        button_b.set_label('Reiniciar ahora')
        button_b.connect('clicked', self.reboot)
        box.put(button_b, 540, 440)

        window.show_all()

        button_a.hide()
        button_b.hide()

        q_view.put(view)
        q_label.put(label)
        q_button_a.put(button_a)
        q_button_b.put(button_b)
        event.set()

        self.view = view

    def close(self, widget=None, data=None):
        gtk.main_quit()

    def reboot(self, widget=None, data=None):
        ProcessGenerator('reboot')

    def show_html(self):
        glib.idle_add(
            self.view.load_uri, 'file://'+os.path.realpath(INSTALL_SLIDES)
            )

    def disable_close(self, widget=None, data=None):
        return True

def install_process(CFG, q_button_a, q_button_b, q_view, q_label):
    button_a = q_button_a.get()
    button_b = q_button_b.get()
    view = q_view.get()
    label = q_label.get()
    p = Particiones()
    w = CFG['w']
    metodo = CFG['metodo']
    acciones = CFG['acciones']
    teclado = CFG['teclado']
    passroot = CFG['passroot1']
    nombre = CFG['nombre']
    usuario = CFG['usuario']
    passuser = CFG['passuser1']
    maquina = CFG['maquina']
    oem = CFG['oem']
    gdm = CFG['gdm']
    mountpoint = '/target'
    squashfs = '/live/image/live/filesystem.squashfs'
    requesturl = 'http://www.google.com/'
    uninstpkgs = ['canaima-instalador']
    reconfpkgs = [
        'canaima-estilo-visual-gnome', 'canaima-plymouth',
        'canaima-chat-gnome', 'canaima-bienvenido-gnome',
        'canaima-escritorio-gnome', 'canaima-base'
        ]
    instpkgs_burg = [
        ['/live/image/pool/main/libx/libx86', 'libx86-1'],
        ['/live/image/pool/main/s/svgalib', 'libsvga1'],
        ['/live/image/pool/main/libs/libsdl1.2', 'libsdl1.2debian-alsa'],
        ['/live/image/pool/main/libs/libsdl1.2', 'libsdl1.2debian'],
        ['/live/image/pool/main/g/gettext', 'gettext-base'],
        ['/live/image/pool/main/b/burg-themes', 'burg-themes-common'],
        ['/live/image/pool/main/b/burg-themes', 'burg-themes'],
        ['/live/image/pool/main/b/burg', 'burg-common'],
        ['/live/image/pool/main/b/burg', 'burg-emu'],
        ['/live/image/pool/main/b/burg', 'burg-pc'],
        ['/live/image/pool/main/b/burg', 'burg']
        ]
    instpkgs_cpp = [[
        '/live/image/pool/main/c/canaima-primeros-pasos/',
        'canaima-primeros-pasos'
        ]]
    instpkgs_cagg = [[
        '/live/image/pool/main/c/canaima-accesibilidad-gdm-gnome/',
        'canaima-accesibilidad-gdm-gnome'
        ]]
    debconflist = [
        'burg-pc burg/linux_cmdline string quiet splash',
        'burg-pc burg/linux_cmdline_default string quiet splash vga=791',
        'burg-pc burg-pc/install_devices multiselect {0}'.format(metodo['disco'][0])
        ]
    bindlist = [
        ['/dev', mountpoint + '/dev', ''],
        ['/dev/pts', mountpoint + '/dev/pts', ''],
        ['/sys', mountpoint + '/sys', ''],
        ['/proc', mountpoint + '/proc', '']
        ]
    connection = True
    mountlist = []

    if not os.path.isdir(mountpoint):
        os.makedirs(mountpoint)

    if not os.path.exists(squashfs):
        UserMessage(
            message='No se encuentra la imagen squashfs.',
            title='ERROR',
            mtype=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK,
            c_1=gtk.RESPONSE_OK, f_1=assisted_umount, p_1=(True, bindlist),
            c_2=gtk.RESPONSE_OK, f_2=assisted_umount, p_2=(True, mountlist),
            c_3=gtk.RESPONSE_OK, f_3=sys.exit, p_3=(1,)
            )

    if not assisted_umount(sync=True, plist=mounted_targets(mnt=mountpoint)):
        UserMessage(
            message='Ocurrió un error desmontando las particiones.',
            title='ERROR',
            mtype=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK,
            c_1=gtk.RESPONSE_OK, f_1=assisted_umount, p_1=(True, bindlist),
            c_2=gtk.RESPONSE_OK, f_2=assisted_umount, p_2=(True, mountlist),
            c_3=gtk.RESPONSE_OK, f_3=sys.exit, p_3=(1,)
            )

    if not assisted_umount(
        sync=True, plist=mounted_parts(disk=metodo['disco'][0])
        ):
        UserMessage(
            message='Ocurrió un error desmontando las particiones.',
            title='ERROR',
            mtype=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK,
            c_1=gtk.RESPONSE_OK, f_1=assisted_umount, p_1=(True, bindlist),
            c_2=gtk.RESPONSE_OK, f_2=assisted_umount, p_2=(True, mountlist),
            c_3=gtk.RESPONSE_OK, f_3=sys.exit, p_3=(1,)
            )

    label.set_text('Creando particiones en disco ...')
    for a in acciones:
        accion = a[0]
        montaje = a[2]
        inicio = a[3]
        fin = a[4]
        fs = a[5]
        tipo = a[6]
        nuevo_fin = a[7]
        disco = metodo['disco'][0]
        particiones = p.lista_particiones(disco)
        cdroms = lista_cdroms()

        if accion == 'crear':
            if not p.crear_particion(
                drive=disco, start=inicio, end=fin, fs=fs, partype=tipo
                ):
                UserMessage(
                    message='Ocurrió un error creando una partición.',
                    title='ERROR',
                    mtype=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK,
                    c_1=gtk.RESPONSE_OK, f_1=assisted_umount, p_1=(True, bindlist),
                    c_2=gtk.RESPONSE_OK, f_2=assisted_umount, p_2=(True, mountlist),
                    c_3=gtk.RESPONSE_OK, f_3=sys.exit, p_3=(1,)
                    )
            else:
                if montaje:
                    mountlist.append([
                        p.nombre_particion(disco, tipo, inicio, fin),
                        mountpoint + montaje, fs
                        ])

        elif accion == 'borrar':
            particion = p.nombre_particion(disco, tipo, inicio, fin)
            if not p.borrar_particion(drive=disco, part=particion):
                UserMessage(
                    message='Ocurrió un error borrando una partición.',
                    title='ERROR',
                    mtype=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK,
                    c_1=gtk.RESPONSE_OK, f_1=assisted_umount, p_1=(True, bindlist),
                    c_2=gtk.RESPONSE_OK, f_2=assisted_umount, p_2=(True, mountlist),
                    c_3=gtk.RESPONSE_OK, f_3=sys.exit, p_3=(1,)
                    )

        elif accion == 'redimensionar':
            particion = p.nombre_particion(disco, tipo, inicio, fin)
            if not p.redimensionar_particion(
                drive=disco, part=particion, newend=nuevo_fin
                ):
                UserMessage(
                    message='Ocurrió un error redimensionando una partición.',
                    title='ERROR',
                    mtype=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK,
                    c_1=gtk.RESPONSE_OK, f_1=assisted_umount, p_1=(True, bindlist),
                    c_2=gtk.RESPONSE_OK, f_2=assisted_umount, p_2=(True, mountlist),
                    c_3=gtk.RESPONSE_OK, f_3=sys.exit, p_3=(1,)
                    )

        elif accion == 'formatear':
            particion = p.nombre_particion(disco, tipo, inicio, fin)
            if not p.formatear_particion(part=particion, fs=fs):
                UserMessage(
                    message='Ocurrió un error formateando una partición.',
                    title='ERROR',
                    mtype=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK,
                    c_1=gtk.RESPONSE_OK, f_1=assisted_umount, p_1=(True, bindlist),
                    c_2=gtk.RESPONSE_OK, f_2=assisted_umount, p_2=(True, mountlist),
                    c_3=gtk.RESPONSE_OK, f_3=sys.exit, p_3=(1,)
                    )

        elif accion == 'usar':
            if montaje:
                mountlist.append([
                    p.nombre_particion(disco, tipo, inicio, fin),
                    mountpoint + montaje, fs
                    ])

    unset_boot = ''
    for i in p.lista_particiones(metodo['disco'][0]):
        for flag in i[6]:
            if flag == 'boot':
                unset_boot = i[0]

    set_boot = ''
    for part, mount, fs in mountlist:
        if mount == mountpoint + '/':
            set_boot = part
        elif mount == mountpoint + '/boot':
            set_boot = part

    if unset_boot:
        if not p.remover_bandera(
            drive=metodo['disco'][0], part=unset_boot, flag='boot'
            ):
            UserMessage(
                message='Ocurrió un error montando los sistemas de archivos.',
                title='ERROR',
                mtype=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK,
                c_1=gtk.RESPONSE_OK, f_1=assisted_umount, p_1=(True, bindlist),
                c_2=gtk.RESPONSE_OK, f_2=assisted_umount, p_2=(True, mountlist),
                c_3=gtk.RESPONSE_OK, f_3=sys.exit, p_3=(1,)
                )

    if set_boot:
        if not p.asignar_bandera(
            drive=metodo['disco'][0], part=set_boot, flag='boot'
            ):
            UserMessage(
                message='Ocurrió un error montando los sistemas de archivos.',
                title='ERROR',
                mtype=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK,
                c_1=gtk.RESPONSE_OK, f_1=assisted_umount, p_1=(True, bindlist),
                c_2=gtk.RESPONSE_OK, f_2=assisted_umount, p_2=(True, mountlist),
                c_3=gtk.RESPONSE_OK, f_3=sys.exit, p_3=(1,)
                )

    label.set_text('Montando sistemas de archivos ...')
    if not assisted_mount(sync=True, bind=False, plist=mountlist):
        UserMessage(
            message='Ocurrió un error montando los sistemas de archivos.',
            title='ERROR',
            mtype=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK,
            c_1=gtk.RESPONSE_OK, f_1=assisted_umount, p_1=(True, bindlist),
            c_2=gtk.RESPONSE_OK, f_2=assisted_umount, p_2=(True, mountlist),
            c_3=gtk.RESPONSE_OK, f_3=sys.exit, p_3=(1,)
            )

    label.set_text('Copiando archivos en disco ...')
    if ProcessGenerator(
        'unsquashfs -f -n -d {0} {1}'.format(mountpoint, squashfs)
        ).returncode != 0:
        UserMessage(
            message='Ocurrió un error copiando los archivos al disco.',
            title='ERROR',
            mtype=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK,
            c_1=gtk.RESPONSE_OK, f_1=assisted_umount, p_1=(True, bindlist),
            c_2=gtk.RESPONSE_OK, f_2=assisted_umount, p_2=(True, mountlist),
            c_3=gtk.RESPONSE_OK, f_3=sys.exit, p_3=(1,)
            )

    label.set_text('Montando sistema de archivos ...')
    if not assisted_mount(sync=True, bind=True, plist=bindlist):
        UserMessage(
            message='Ocurrió un error montando los sistemas de archivos.',
            title='ERROR',
            mtype=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK,
            c_1=gtk.RESPONSE_OK, f_1=assisted_umount, p_1=(True, bindlist),
            c_2=gtk.RESPONSE_OK, f_2=assisted_umount, p_2=(True, mountlist),
            c_3=gtk.RESPONSE_OK, f_3=sys.exit, p_3=(1,)
            )

    label.set_text('Instalando gestor de arranque ...')
    if not preseed_debconf_values(mnt=mountpoint, debconflist=debconflist):
        UserMessage(
            message='Ocurrió un error presembrando las respuestas debconf.',
            title='ERROR',
            mtype=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK,
            c_1=gtk.RESPONSE_OK, f_1=assisted_umount, p_1=(True, bindlist),
            c_2=gtk.RESPONSE_OK, f_2=assisted_umount, p_2=(True, mountlist),
            c_3=gtk.RESPONSE_OK, f_3=sys.exit, p_3=(1,)
            )

    if not instalar_paquetes(mnt=mountpoint, dest='/tmp', plist=instpkgs_burg):
        UserMessage(
            message='Ocurrió un error instalando un paquete.',
            title='ERROR',
            mtype=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK,
            c_1=gtk.RESPONSE_OK, f_1=assisted_umount, p_1=(True, bindlist),
            c_2=gtk.RESPONSE_OK, f_2=assisted_umount, p_2=(True, mountlist),
            c_3=gtk.RESPONSE_OK, f_3=sys.exit, p_3=(1,)
            )

    if ProcessGenerator(
        'chroot {0} burg-install --force {1}'.format(
            mountpoint, metodo['disco'][0]
            )
        ).returncode != 0:
        UserMessage(
            message='Ocurrió un error instalando burg.',
            title='ERROR',
            mtype=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK,
            c_1=gtk.RESPONSE_OK, f_1=assisted_umount, p_1=(True, bindlist),
            c_2=gtk.RESPONSE_OK, f_2=assisted_umount, p_2=(True, mountlist),
            c_3=gtk.RESPONSE_OK, f_3=sys.exit, p_3=(1,)
            )

    if ProcessGenerator(
        'chroot {0} update-burg'.format(mountpoint)
        ).returncode != 0:
        UserMessage(
            message='Ocurrió un error actualizando burg.',
            title='ERROR',
            mtype=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK,
            c_1=gtk.RESPONSE_OK, f_1=assisted_umount, p_1=(True, bindlist),
            c_2=gtk.RESPONSE_OK, f_2=assisted_umount, p_2=(True, mountlist),
            c_3=gtk.RESPONSE_OK, f_3=sys.exit, p_3=(1,)
            )

    label.set_text('Generando imagen de arranque ...')
    if ProcessGenerator(
        'chroot {0} /usr/sbin/mkinitramfs -o /boot/{1} {2}'.format(
            mountpoint, 'initrd.img-' + os.uname()[2], os.uname()[2]
            )
        ).returncode != 0:
        UserMessage(
            message='Ocurrió un error generando la imagen de arranque.',
            title='ERROR',
            mtype=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK,
            c_1=gtk.RESPONSE_OK, f_1=assisted_umount, p_1=(True, bindlist),
            c_2=gtk.RESPONSE_OK, f_2=assisted_umount, p_2=(True, mountlist),
            c_3=gtk.RESPONSE_OK, f_3=sys.exit, p_3=(1,)
            )

    if ProcessGenerator(
        'chroot {0} update-initramfs -u -t'.format(mountpoint)
        ).returncode != 0:
        UserMessage(
            message='Ocurrió un error actualizando la imagen de arranque.',
            title='ERROR',
            mtype=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK,
            c_1=gtk.RESPONSE_OK, f_1=assisted_umount, p_1=(True, bindlist),
            c_2=gtk.RESPONSE_OK, f_2=assisted_umount, p_2=(True, mountlist),
            c_3=gtk.RESPONSE_OK, f_3=sys.exit, p_3=(1,)
            )

    label.set_text('Configurando detalles del sistema operativo ...')
    if not reconfigurar_paquetes(mnt=mountpoint, plist=reconfpkgs):
        UserMessage(
            message='Ocurrió un error reconfigurando un paquete.',
            title='ERROR',
            mtype=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK,
            c_1=gtk.RESPONSE_OK, f_1=assisted_umount, p_1=(True, bindlist),
            c_2=gtk.RESPONSE_OK, f_2=assisted_umount, p_2=(True, mountlist),
            c_3=gtk.RESPONSE_OK, f_3=sys.exit, p_3=(1,)
            )

    label.set_text('Configurando interfaces de red ...')
    if not crear_etc_hostname(mnt=mountpoint, cfg='/etc/hostname', maq=maquina):
        UserMessage(
            message='Ocurrió un error creando el archivo /etc/hostname.',
            title='ERROR',
            mtype=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK,
            c_1=gtk.RESPONSE_OK, f_1=assisted_umount, p_1=(True, bindlist),
            c_2=gtk.RESPONSE_OK, f_2=assisted_umount, p_2=(True, mountlist),
            c_3=gtk.RESPONSE_OK, f_3=sys.exit, p_3=(1,)
            )

    if not crear_etc_hosts(mnt=mountpoint, cfg='/etc/hosts', maq=maquina):
        UserMessage(
            message='Ocurrió un error creando el archivo /etc/hosts.',
            title='ERROR',
            mtype=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK,
            c_1=gtk.RESPONSE_OK, f_1=assisted_umount, p_1=(True, bindlist),
            c_2=gtk.RESPONSE_OK, f_2=sys.exit, p_2=(1,)
            )

    if not crear_etc_network_interfaces(
        mnt=mountpoint, cfg='/etc/network/interfaces'
        ):
        UserMessage(
            message='Ocurrió un error creando el archivo /etc/network/interfaces.',
            title='ERROR',
            mtype=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK,
            c_1=gtk.RESPONSE_OK, f_1=assisted_umount, p_1=(True, bindlist),
            c_2=gtk.RESPONSE_OK, f_2=assisted_umount, p_2=(True, mountlist),
            c_3=gtk.RESPONSE_OK, f_3=sys.exit, p_3=(1,)
            )

    label.set_text('Configurando teclado ...')
    if not crear_etc_default_keyboard(
        mnt=mountpoint, cfg='/etc/canaima-base/alternatives/keyboard',
        key=teclado
        ):
        UserMessage(
            message='Ocurrió un error configurando el teclado.',
            title='ERROR',
            mtype=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK,
            c_1=gtk.RESPONSE_OK, f_1=assisted_umount, p_1=(True, bindlist),
            c_2=gtk.RESPONSE_OK, f_2=assisted_umount, p_2=(True, mountlist),
            c_3=gtk.RESPONSE_OK, f_3=sys.exit, p_3=(1,)
            )

    label.set_text('Configurando particiones en /etc/fstab ...')
    if not crear_etc_fstab(
        mnt=mountpoint, cfg='/etc/fstab',
        mountlist=mountlist, cdroms=cdroms
        ):
        UserMessage(
            message='Ocurrió un error creando el archivo /etc/fstab.',
            title='ERROR',
            mtype=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK,
            c_1=gtk.RESPONSE_OK, f_1=assisted_umount, p_1=(True, bindlist),
            c_2=gtk.RESPONSE_OK, f_2=assisted_umount, p_2=(True, mountlist),
            c_3=gtk.RESPONSE_OK, f_3=sys.exit, p_3=(1,)
            )

    label.set_text('Configurando usuarios y grupos ...')
    if not crear_passwd_group_inittab_mtab(mnt=mountpoint):
        UserMessage(
            message='Ocurrió un error configurando usuarios y grupos.',
            title='ERROR',
            mtype=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK,
            c_1=gtk.RESPONSE_OK, f_1=assisted_umount, p_1=(True, bindlist),
            c_2=gtk.RESPONSE_OK, f_2=assisted_umount, p_2=(True, mountlist),
            c_3=gtk.RESPONSE_OK, f_3=sys.exit, p_3=(1,)
            )

    if oem:
        adm_user = 'root'
        adm_password = 'root'
        nml_user = 'canaima'
        nml_password = 'canaima'
        nml_name = 'Mantenimiento'

        if not instalar_paquetes(
            mnt=mountpoint, dest='/tmp', plist=instpkgs_cpp
            ):
            UserMessage(
                message='Ocurrió un error instalando un paquete.',
                title='ERROR',
                mtype=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK,
                c_1=gtk.RESPONSE_OK, f_1=assisted_umount, p_1=(True, bindlist),
                c_2=gtk.RESPONSE_OK, f_2=assisted_umount, p_2=(True, mountlist),
                c_3=gtk.RESPONSE_OK, f_3=sys.exit, p_3=(1,)
                )

    else:
        adm_user = 'root'
        adm_password = passroot
        nml_user = usuario
        nml_password = passuser
        nml_name = nombre

    if gdm:
        if not instalar_paquetes(
            mnt=mountpoint, dest='/tmp', plist=instpkgs_cagg
            ):
            UserMessage(
                message='Ocurrió un error instalando un paquete.',
                title='ERROR',
                mtype=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK,
                c_1=gtk.RESPONSE_OK, f_1=assisted_umount, p_1=(True, bindlist),
                c_2=gtk.RESPONSE_OK, f_2=assisted_umount, p_2=(True, mountlist),
                c_3=gtk.RESPONSE_OK, f_3=sys.exit, p_3=(1,)
                )

    label.set_text('Creando usuarios de sistema ...')
    if not crear_usuarios(
        mnt=mountpoint, a_user=adm_user, a_pass=adm_password,
        n_name=nml_name, n_user=nml_user, n_pass=nml_password
        ):
        UserMessage(
            message='Ocurrió un error creando los usuarios de sistema.',
            title='ERROR',
            mtype=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK,
            c_1=gtk.RESPONSE_OK, f_1=assisted_umount, p_1=(True, bindlist),
            c_2=gtk.RESPONSE_OK, f_2=assisted_umount, p_2=(True, mountlist),
            c_3=gtk.RESPONSE_OK, f_3=sys.exit, p_3=(1,)
            )

    label.set_text('Removiendo instalador del sistema de archivos ...')
    if not desinstalar_paquetes(mnt=mountpoint, plist=uninstpkgs):
        UserMessage(
            message='Ocurrió un error desinstalando un paquete.',
            title='ERROR',
            mtype=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK,
            c_1=gtk.RESPONSE_OK, f_1=assisted_umount, p_1=(True, bindlist),
            c_2=gtk.RESPONSE_OK, f_2=assisted_umount, p_2=(True, mountlist),
            c_3=gtk.RESPONSE_OK, f_3=sys.exit, p_3=(1,)
            )

    label.set_text('Desmontando sistema de archivos ...')
    if not assisted_umount(sync=True, plist=bindlist):
        UserMessage(
            message='Ocurrió un error desmontando las particiones.',
            title='ERROR',
            mtype=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK,
            c_1=gtk.RESPONSE_OK, f_1=assisted_umount, p_1=(True, bindlist),
            c_2=gtk.RESPONSE_OK, f_2=assisted_umount, p_2=(True, mountlist),
            c_3=gtk.RESPONSE_OK, f_3=sys.exit, p_3=(1,)
            )

    if not assisted_umount(sync = True, plist = mountlist):
        UserMessage(
            message='Ocurrió un error desmontando las particiones.',
            title='ERROR',
            mtype=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK,
            c_1=gtk.RESPONSE_OK, f_1=assisted_umount, p_1=(True, bindlist),
            c_2=gtk.RESPONSE_OK, f_2=assisted_umount, p_2=(True, mountlist),
            c_3=gtk.RESPONSE_OK, f_3=sys.exit, p_3=(1,)
            )

    button_a.show()
    button_b.show()
    label.hide()
    view.hide()

