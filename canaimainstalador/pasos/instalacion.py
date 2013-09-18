#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# =============================================================================
# PAQUETE: canaima-instalador
# ARCHIVO: canaimainstalador/pasos/instalacion.py
# COPYRIGHT:
#       (C) 2012 William Abrahan Cabrera Reyes <william@linux.es>
#       (C) 2012 Erick Manuel Birbe Salazar <erickcion@gmail.com>
#       (C) 2012 Luis Alejandro Martínez Faneyth <luis@huntingbears.com.ve>
# LICENCIA: GPL-3
# =============================================================================
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

from canaimainstalador.clases.common import UserMessage, ProcessGenerator, \
    reconfigurar_paquetes, desinstalar_paquetes, instalar_paquetes, \
    lista_cdroms, crear_etc_hostname, crear_etc_hosts, \
    crear_etc_network_interfaces, crear_etc_fstab, assisted_mount, \
    assisted_umount, preseed_debconf_values, mounted_targets, mounted_parts, \
    crear_usuarios, ThreadGenerator, get_windows_part_in, activar_swap, \
    crear_archivos_config, activar_accesibilidad, create_file, get_live_path
from canaimainstalador.clases.particiones import Particiones
from canaimainstalador.config import INSTALL_SLIDES, BAR_ICON, SHAREDIR
import Queue
import gobject
import gtk
import os
import pango
import sys
import threading
import webkit
from canaimainstalador.clases import keyboard, i18n
from canaimainstalador.clases.i18n import install_language_pack
from canaimainstalador.translator import gettext_install
from canaimainstalador.mod_accesible import atk_acc_vd


gettext_install()
gobject.threads_init()


class PasoInstalacion():
    def __init__(self, CFG):
        q_button_a = Queue.Queue()
        q_button_b = Queue.Queue()
        q_view = Queue.Queue()
        q_label = Queue.Queue()
        q_win = Queue.Queue()
        event = threading.Event()

        params = {
                'title': _('Canaima Installation'),
                'q_button_a': q_button_a,
                'q_button_b': q_button_b,
                'q_view': q_view,
                'q_label': q_label,
                'q_win': q_win,
                'event': event
                }

        window = install_window(**params)

        ThreadGenerator(
            reference=None, function=window.show_html, params={}
            )

        ThreadGenerator(
            reference=None, function=install_process,
            params={
                'CFG': CFG,
                'q_button_a': q_button_a,
                'q_button_b': q_button_b,
                'q_view': q_view,
                'q_label': q_label,
                'q_win': q_win
                },
            event=event
            )


class install_window(object):

    def __init__(self, title, q_button_a, q_button_b, q_view, q_label, q_win,
                 event):

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

        str_message = _('Canaima installation has been completed')
        message = gtk.Label(str_message)
        message.set_size_request(640, 40)
        message.set_alignment(0, 0)
        message.set_line_wrap(True)
        message.set_attributes(attr)
        box.put(message, 50, 200)

        str_intro = _('You can keep trying Canaima pressing "Restart Later" \
or enjoy your installed operating system by pressing "Restart Now".')
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
        button_a.set_label(_('Restart Later'))
        button_a.connect('clicked', self.close)
        box.put(button_a, 390, 440)

        button_b = gtk.Button()
        button_b.set_size_request(150, 30)
        button_b.set_label(_('Restart Now'))
        button_b.connect('clicked', self.reboot)
        box.put(button_b, 540, 440)

        box.set_flags(gtk.CAN_FOCUS)
        atk_acc_vd(box, str_message + ". " + str_intro)

        window.show_all()

        button_a.hide()
        button_b.hide()

        q_view.put(view)
        q_label.put(label)
        q_win.put(window)
        q_button_a.put(button_a)
        q_button_b.put(button_b)
        event.set()

        self.view = view

    def close(self, widget=None, data=None):
        gtk.main_quit()

    def reboot(self, widget=None, data=None):
        ProcessGenerator('reboot')

    def show_html(self):
        gobject.idle_add(
            self.view.load_uri, 'file://' + os.path.realpath(INSTALL_SLIDES)
            )

    def disable_close(self, widget=None, data=None):
        return True


def UserMessageError(message, window, bindlist, mountlist):
    '''Hacemos acá una especie de sobreescritura de UserMessage para resumir
    líneas de código, ya que será un método de uso frecuente en este
    módulo'''

    UserMessage(
        message,
        title='ERROR',
        mtype=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK,
        c_1=gtk.RESPONSE_OK, f_1=assisted_umount, p_1=(True, bindlist),
        c_2=gtk.RESPONSE_OK, f_2=assisted_umount, p_2=(True, mountlist),
        c_3=gtk.RESPONSE_OK, f_3=window.destroy, p_3=(),
        c_4=gtk.RESPONSE_OK, f_4=gtk.main_quit, p_4=(),
        c_5=gtk.RESPONSE_OK, f_5=sys.exit, p_5=()
    )


def conf_files_install(cfg, mountpoint):

    lcl = cfg['locale']
    tzn = cfg['timezone']
    kbd = cfg['keyboard']

    # ------------------------------------------------- Configuración de idioma
    # /etc/default/locale
    data = i18n.locale_content(lcl)
    if not create_file(mountpoint + '/etc/default/locale', data):
        return False
    # /etc/locale.gen
    data = i18n.locale_gen_content(lcl)
    if not create_file(mountpoint + '/etc/locale.gen', data):
        return False

    # ------------------------------------------- Configuración de zona horaria
    data = tzn + '\n'
    if not create_file(mountpoint + '/etc/timezone', data):
        return False

    # ------------------------------------------------ Configuración de teclado
    data = keyboard.keyboard_contents(kbd, lcl.get_locale())
    if not create_file(mountpoint + '/etc/default/keyboard', data):
        return False

    return True


def install_process(CFG, q_button_a, q_button_b, q_view, q_label, q_win):
    button_a = q_button_a.get()
    button_b = q_button_b.get()
    view = q_view.get()
    label = q_label.get()
    window = q_win.get()
    p = Particiones()
    metodo = CFG['metodo']
    acciones = CFG['acciones']
    passroot = CFG['passroot1']
    nombre = CFG['nombre']
    usuario = CFG['usuario']
    passuser = CFG['passuser1']
    maquina = CFG['maquina']
    lcl_item = CFG['locale']
    oem = CFG['oem']
    gdm = CFG['gdm']
    mountpoint = '/target'
    LIVE_PATH = get_live_path()
    squashfs = LIVE_PATH + '/live/filesystem.squashfs'
    uninstpkgs = [
        'canaima-instalador', 'live-config', 'live-boot',
        'live-boot-initramfs-tools', 'live-initramfs', 'live-config-sysvinit',
        'live-tools'
        ]
    reconfpkgs = [
        'locales', 'canaima-estilo-visual-gnome', 'canaima-escritorio-gnome',
        'canaima-base', 'tzdata', 'software-center', 'console-data'
        ]
    instpkgs_burg = [
        [LIVE_PATH + '/pool/main/libx/libx86', 'libx86-1'],
        [LIVE_PATH + '/pool/main/s/svgalib', 'libsvga1'],
        [LIVE_PATH + '/pool/main/libs/libsdl1.2', 'libsdl1.2debian'],
        [LIVE_PATH + '/pool/main/g/gettext', 'libasprintf0c2'],
        [LIVE_PATH + '/pool/main/g/gettext', 'gettext-base'],
        [LIVE_PATH + '/pool/main/b/burg-themes', 'burg-themes-common'],
        [LIVE_PATH + '/pool/main/b/burg-themes', 'burg-themes'],
        [LIVE_PATH + '/pool/main/b/burg', 'burg-common'],
        [LIVE_PATH + '/pool/main/b/burg', 'burg-emu'],
        [LIVE_PATH + '/pool/main/b/burg', 'burg-pc'],
        [LIVE_PATH + '/pool/main/b/burg', 'burg']
        ]
    instpkgs_cpp = [[
        LIVE_PATH + '/pool/main/c/canaima-primeros-pasos/',
        'canaima-primeros-pasos'
        ]]
    debconflist = [
        'burg-pc burg/linux_cmdline string quiet splash',
        'burg-pc burg/linux_cmdline_default string quiet splash vga=791',
        'burg-pc burg-pc/install_devices multiselect {0}'.format(
                                                ', '.join(p.lista_discos())),
        #TODO: Automatizar la configuración del teclado de las TTY
        "console-data console-data/keymap/qwerty/layout select Latin American",
        "console-data console-data/keymap/family select qwerty",
        "console-common console-data/keymap/family select qwerty",
        "console-data console-data/keymap/qwerty/latin_american/variant \
select Standard",
        "console-data console-data/keymap/qwerty/latin_american/standard/\
keymap select Standard",
        "console-data console-data/keymap/policy select Select keymap from \
arch list"
        ]
    bindlist = [
        ['/dev', mountpoint + '/dev', ''],
        ['/dev/pts', mountpoint + '/dev/pts', ''],
        ['/sys', mountpoint + '/sys', ''],
        ['/proc', mountpoint + '/proc', '']
        ]
    mountlist = []

    # Lista de archivos de configuración que se copiaran al disco
    conffilelist = [
        [SHAREDIR + '/templates/sources.list',
                                        mountpoint + '/etc/apt/sources.list'],
        [SHAREDIR + '/templates/adduser.conf',
                                        mountpoint + '/etc/adduser.conf'],
        # Agregamos mtab para que no falle al instalar Burg
        ['/etc/mtab', mountpoint + '/etc/mtab']
    ]

    if not os.path.isdir(mountpoint):
        os.makedirs(mountpoint)

    #TODO: Esta validación deberia hacerse al inicio de la aplicación y no
    # esperar hasta este punto
    if not os.path.exists(squashfs):
        UserMessageError(_('Not found squashfs image.'),
                         window, bindlist, mountlist)

    if not assisted_umount(sync=True, plist=mounted_targets(mnt=mountpoint)):
        UserMessageError(_('An error occurred unmounting the partitions.'),
                         window, bindlist, mountlist)

    if not assisted_umount(sync=True,
                           plist=mounted_parts(disk=metodo['disco'][0])):
        UserMessageError(_('An error occurred unmounting the partitions.'),
                         window, bindlist, mountlist)

    label.set_text(_('Creating partitions in the disk ...'))
    for a in acciones:
        accion = a[0]
        montaje = a[2]
        inicio = a[3]
        fin = a[4]
        fs = a[5]
        tipo = a[6]
        nuevo_fin = a[7]
        disco = metodo['disco'][0]
        cdroms = lista_cdroms()

        if accion == 'crear':
            if not p.crear_particion(
                drive=disco, start=inicio, end=fin, fs=fs, partype=tipo,
                format=True):
                UserMessageError(_('An error occurred creating a partition.'),
                         window, bindlist, mountlist)
            else:
                if montaje:
                    mountlist.append([
                        p.nombre_particion(disco, tipo, inicio, fin),
                        mountpoint + montaje, fs
                        ])

        elif accion == 'borrar':
            particion = p.nombre_particion(disco, tipo, inicio, fin)
            if not p.borrar_particion(drive=disco, part=particion):
                UserMessageError(_('An error occurred removing a partition.'),
                         window, bindlist, mountlist)
            else:
                for item in mountlist:
                    if item[0] == particion:
                        mountlist.remove(item)

        elif accion == 'redimensionar':
            particion = p.nombre_particion(disco, tipo, inicio, fin)
            if not p.redimensionar_particion(drive=disco, part=particion,
                                             newend=nuevo_fin):
                UserMessageError(_('An error occurred resizing a partition.'),
                         window, bindlist, mountlist)

        elif accion == 'formatear':
            particion = p.nombre_particion(disco, tipo, inicio, fin)
            if not p.formatear_particion(part=particion, fs=fs):
                UserMessageError(_('An error occurred formatting a \
partition.'),
                         window, bindlist, mountlist)
            else:
                if montaje:
                    mountlist.append([
                        p.nombre_particion(disco, tipo, inicio, fin),
                        mountpoint + montaje, fs
                        ])

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
    winpart = get_windows_part_in(metodo['disco'][0])
    if winpart:
        set_boot = winpart
    else:
        for part, mount, fs in mountlist:
            if mount == mountpoint + '/':
                set_boot = part
            elif mount == mountpoint + '/boot':
                set_boot = part

    if unset_boot:
        if not p.remover_bandera(
            drive=metodo['disco'][0], part=unset_boot, flag='boot'
            ):
            UserMessageError(_("An error occurred mounting the filesystem"),
                             window, bindlist, mountlist)

    if set_boot:
        if not p.asignar_bandera(
            drive=metodo['disco'][0], part=set_boot, flag='boot'
            ):
            UserMessageError(_("An error occurred mounting the filesystem"),
                             window, bindlist, mountlist)

    if not activar_swap(plist=mountlist):
        UserMessageError(_("An error occurred activating the swap partition"),
                         window, bindlist, mountlist)

    label.set_text(_("Mounting the filesystem ..."))
    if not assisted_mount(sync=True, bind=False, plist=mountlist):
        UserMessageError(_("An error occurred mounting the filesystem"),
                         window, bindlist, mountlist)

    label.set_text(_("Copying files to disk ..."))
    if ProcessGenerator(
        'unsquashfs -f -n -d {0} {1}'.format(mountpoint, squashfs)
        ).returncode != 0:
        UserMessageError(_("An error occurred copying files to disk."),
                         window, bindlist, mountlist)

    label.set_text(_("Mounting the filesystem ..."))
    if not assisted_mount(sync=True, bind=True, plist=bindlist):
        UserMessageError(_("An error occurred mounting the filesystem"),
                         window, bindlist, mountlist)

    # Configuración de archivos del sistema
    label.set_text(_("Configuring system files ..."))
    if not crear_archivos_config(mnt=mountpoint, conffilelist=conffilelist):
        UserMessageError(_("An error occurred configuring the system files"),
                         window, bindlist, mountlist)
    if not conf_files_install(CFG, mountpoint):
        UserMessageError(_("An error occurred configuring the system files"),
                         window, bindlist, mountlist)

    label.set_text(_("Configuring network interfaces ..."))
    if not crear_etc_hostname(mnt=mountpoint, cfg='/etc/hostname',
                              maq=maquina):
        UserMessageError(_("An error occurred creating file /etc/hostname"),
                         window, bindlist, mountlist)
    if not crear_etc_hosts(mnt=mountpoint, cfg='/etc/hosts', maq=maquina):
        UserMessageError(_("An error occurred creating file /etc/hosts"),
                         window, bindlist, mountlist)
    if not crear_etc_network_interfaces(mnt=mountpoint,
                                        cfg='/etc/network/interfaces'):
        UserMessageError(_("An error occurred creating file \
/etc/network/interfaces"), window, bindlist, mountlist)

    label.set_text(_("Registering partitions in the system ..."))
    if not crear_etc_fstab(mnt=mountpoint, cfg='/etc/fstab',
                           mountlist=mountlist, cdroms=cdroms):
        UserMessageError(_("An error occurred creating file /etc/fstab"),
                         window, bindlist, mountlist)

    # Instalar accesibilidad en el GDM
    if gdm:
        label.set_text(_("Installing accessibility components in GDM ..."))
        if not activar_accesibilidad(mnt=mountpoint):
            UserMessageError(_("An error occurred activating accesibility."),
                         window, bindlist, mountlist)

    # Reconfigurando paquetes del sistema
    label.set_text(_("Configuring additional details on the system ..."))
    if not reconfigurar_paquetes(mnt=mountpoint, plist=reconfpkgs):
        UserMessageError(_("An error occurred reconfiguring a package."),
                         window, bindlist, mountlist)

    # instalación de los paquetes de idiomas
    label.set_text(_("Configuring additional language packages ..."))
    if not install_language_pack(lcl_item.get_locale(), mountpoint):
        print "ADVERTENCIA: No se instalaran los paquetes adicionales del \
idioma"

    # Activa la funcionalidad OEM si ha sido seleccionada por el usuario
    if oem:
        adm_user = 'root'
        adm_password = 'root'
        nml_user = 'canaima'
        nml_password = 'canaima'
        nml_name = 'Mantenimiento'
        # Instala Canaima Primeros Pasos
        label.set_text(_("Installing OEM characteristics ..."))
        if not instalar_paquetes(mnt=mountpoint, dest='/tmp',
                                 plist=instpkgs_cpp):
            UserMessageError(_("An error occurred installing a package"),
                         window, bindlist, mountlist)
    else:
        adm_user = 'root'
        adm_password = passroot
        nml_user = usuario
        nml_password = passuser
        nml_name = nombre

    label.set_text(_("Creating system users ..."))
    if not crear_usuarios(mnt=mountpoint, a_user=adm_user, a_pass=adm_password,
                          n_name=nml_name, n_user=nml_user,
                          n_pass=nml_password):
        UserMessageError(_("An error occurred creating system user"),
                         window, bindlist, mountlist)

    label.set_text(_("Removing temporary data of installation ..."))
    if not desinstalar_paquetes(mnt=mountpoint, plist=uninstpkgs):
        UserMessageError(_("An error occurred removing a package"),
                         window, bindlist, mountlist)

    label.set_text(_("Installing Bootloader ..."))
    if not preseed_debconf_values(mnt=mountpoint, debconflist=debconflist):
        UserMessageError(_("An error occurred preseeding answers in debconf."),
                         window, bindlist, mountlist)
    if not instalar_paquetes(mnt=mountpoint, dest='/tmp', plist=instpkgs_burg):
        UserMessageError(_("An error occurred installing a package."),
                         window, bindlist, mountlist)
    if ProcessGenerator('chroot {0} update-burg'.format(mountpoint)
                        ).returncode != 0:
        UserMessageError(_("An error occurred updating BURG."),
                         window, bindlist, mountlist)

    label.set_text(_("Configuring system boot ..."))
    if ProcessGenerator(
        'chroot {0} /usr/sbin/mkinitramfs -o /boot/{1} {2}'.format(
            mountpoint, 'initrd.img-' + os.uname()[2], os.uname()[2]
            )
        ).returncode != 0:
        UserMessageError(_("An error occurred generating boot image"),
                         window, bindlist, mountlist)
    if ProcessGenerator(
        'chroot {0} update-initramfs -u -t'.format(mountpoint)
        ).returncode != 0:
        UserMessageError(_("An error occurred updating the boot image."),
                         window, bindlist, mountlist)

    # Terminando la instalación
    label.set_text(_("Umounting filesistems ..."))
    if not assisted_umount(sync=True, plist=bindlist):
        UserMessageError(_("An error occurred umounting partitions."),
                         window, bindlist, mountlist)
    if not assisted_umount(sync=True, plist=mountlist):
        UserMessageError(_("An error occurred umounting partitions."),
                         window, bindlist, mountlist)

    button_a.show()
    button_b.show()
    label.get_parent().remove(label)
    view.get_parent().remove(view)
