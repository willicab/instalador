#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# =============================================================================
# PAQUETE: instalador
# ARCHIVO: instalador/config.py
# COPYRIGHT:
#       (C) 2012 William Abrahan Cabrera Reyes <william@linux.es>
#       (C) 2012 Erick Manuel Birbe Salazar <erickcion@gmail.com>
#       (C) 2012 Luis Alejandro Martínez Faneyth <luis@huntingbears.com.ve>
# LICENCIA: GPL-2
# =============================================================================
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import os
from instalador.translator import gettext_install

gettext_install()

curdir = os.path.normpath(os.path.join(os.path.realpath(__file__), '..', '..'))

DISTRIBUTION = 'canaima'

if curdir[:5] == '/usr/':
    GUIDIR = '/usr/share/pyshared/instalador'
    SHAREDIR = '/usr/share/instalador'
else:
    GUIDIR = curdir + '/instalador'
    SHAREDIR = curdir

BAR_ICON = GUIDIR + '/data/' + DISTRIBUTION + '/img/icon.png'
ABOUT_IMAGE = GUIDIR + '/data/' + DISTRIBUTION + '/img/logo.png'
BANNER_IMAGE = GUIDIR + '/data/' + DISTRIBUTION + '/img/banner.png'
WELCOME_IMAGE = GUIDIR + '/data/' + DISTRIBUTION + '/img/welcome.png'
KEY_IMAGE_TMPL = GUIDIR + '/data/' + DISTRIBUTION + '/img/key_{0}.png'
INSTALL_SLIDES = GUIDIR + '/data/' + DISTRIBUTION + '/slider/install.html'

VERSION_FILE = SHAREDIR + '/VERSION'
AUTHORS_FILE = SHAREDIR + '/AUTHORS'
LICENSE_FILE = SHAREDIR + '/LICENSE'
TRANSLATORS_FILE = SHAREDIR + '/TRANSLATORS'

APP_NAME = _('Canaima Installer')
APP_COPYRIGHT = _('Copyright (C) 2012 - Several authors')
APP_URL = 'https://github.com/willicab/instalador.git'
APP_DESCRIPTION = _('Installer for Canaima GNU/Linux')

ESPACIO_ROOT = 1024.0 * 1024.0              # 1GB
ESPACIO_VAR = 1024.0 * 896.0                # 896MB
ESPACIO_HOME = 1024.0 * 1024.0              # 1GB
ESPACIO_USR = 1024.0 * 1024.0 * 2.0         # 2GB
ESPACIO_BOOT = 1024.0 * 128.0               # 128MB
ESPACIO_SWAP = 1024.0 * 1024.0              # 1GB
# ------------------------------------------# -------
ESPACIO_TOTAL = 1024.0 * 1024.0 * 6.0       # 6GB

ESPACIO_USADO_EXTRA = 1024.0 * 512.0

CFG = {
    's': []
    }

FSPROGS = {
    'btrfs': [
        ['mkfs.btrfs {0}'],
        ['btrfsck {1}', 'umount /mnt || true', 'sync',
         'mount -t btrfs {1} /mnt', 'sync', 'btrfs filesystem resize {0} /mnt',
         'umount /mnt', 'sync'],
        ['btrfsck {1}'],
        ['sfdisk --id {0} {1} 83']
        ],
    'ext2': [
        ['mkfs.ext2 -q -F -F {0}'],
        ['e2fsck -f -y -v {1}', 'resize2fs {1} {0}'],
        ['e2fsck -f -y -v {1}', 'resize2fs {1}'],
        ['sfdisk --id {0} {1} 83']
        ],
    'ext3': [
        ['mkfs.ext3 -q -F -F {0}'],
        ['e2fsck -f -y -v {1}', 'resize2fs {1} {0}'],
        ['e2fsck -f -y -v 1}', 'resize2fs {1}'],
        ['sfdisk --id {0} {1} 83']
        ],
    'ext4': [
        ['mkfs.ext4 -q -F -F {0}'],
        ['e2fsck -f -y -v {1}', 'resize2fs {1} {0}'],
        ['e2fsck -f -y -v {1}', 'resize2fs {1}'],
        ['sfdisk --id {0} {1} 83']
        ],
    'fat16': [
        ['mkfs.vfat -F 16 {0}'],
        ['dosfsck -a -w -v {1}', 'fatresize -q -s {0} {1}'],
        ['dosfsck -a -w -v {1}'],
        ['sfdisk --id {0} {1} 6']
        ],
    'fat32': [
        ['mkfs.vfat -F 32 {0}'],
        ['dosfsck -a -w -v {1}', 'fatresize -q -s {0} {1}'],
        ['dosfsck -a -w -v {1}'],
        ['sfdisk --id {0} {1} b']
        ],
    'ntfs': [
        ['mkfs.ntfs -q -F {0}'],
        ['ntfsresize -P -i -f -v {1}', 'ntfsresize -P -f -n -s {0} {1}',
         'echo y | ntfsresize -P -f -s {0} {1}'],
        ['ntfsresize -P -i -f -v {1}', 'ntfsresize -P -f -n {1}',
         'echo y | ntfsresize -P -f {1}'],
        ['sfdisk --id {0} {1} 7']
        ],
    'hfs+': [
        ['mkfs.hfsplus {0}'],
        [''],
        [''],
        ['sfdisk --id {0} {1} af']
        ],
    'hfs': [
        ['hformat -f {0}'],
        [''],
        [''],
        ['sfdisk --id {0} {1} af']
        ],
    'jfs': [
        ['mkfs.jfs -q {0}'],
        [''],
        [''],
        ['sfdisk --id {0} {1} 83']
        ],
    'swap': [
        ['mkswap -f {0}'],
        [''],
        [''],
        ['sfdisk --id {0} {1} 82']
        ],
    'reiser4': [
        ['mkfs.reiser4 -y -f {0}'],
        [''],
        [''],
        ['sfdisk --id {0} {1} 83']
        ],
    'reiserfs': [
        ['mkfs.reiserfs -q -f -f {0}'],
        ['reiserfsck -q -y --fix-fixable {1} || true',
         'echo y | resize_reiserfs -s {0} {1}'],
        ['reiserfsck -q -y --fix-fixable {1} || true',
         'echo y | resize_reiserfs {1}'],
        ['sfdisk --id {0} {1} 83']
        ],
    'xfs': [
        ['mkfs.xfs -q -f {0}'],
        [''],
        [''],
        ['sfdisk --id {0} {1} 83']
        ]
    }

FSMIN = {
    'btrfs': 1024 * 256,
    'ext2': 1024,
    'ext3': 1024,
    'ext4': 1024,
    'fat16': 128,
    'fat32': 32,
    'ntfs': 1024,
    'hfs+': 512,
    'hfs': 800,
    'jfs': 1024 * 16,
    'swap': 40,
    'reiser4': 156,
    'reiserfs': 1024 * 16,
    'xfs': 1024 * 16
    }

FSMAX = {
    'fat16': 1024 * 1024 * 4,
    'hfs': 1024 * 1024 * 2,
    }
