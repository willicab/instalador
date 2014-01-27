# -*- coding: UTF-8 -*-
'''
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Ucumari; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA

Created on 12/12/2013

@author: Erick Birbe <erickcion@gmail.com>
'''
from canaimainstalador.clases.common import assisted_umount, assisted_mount


def mount_devices(devices):

    if not assisted_mount(sync=True, bind=False, plist=devices):
        raise Exception(_("Was not possible to mount."))


def umount_devices(devices):

    if not assisted_umount(sync=True, plist=devices):
        raise Exception(_("Was not possible to umount."))
