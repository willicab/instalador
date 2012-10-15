#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ==============================================================================
# PAQUETE: canaima-instalador
# ARCHIVO: canaimainstalador/config.py
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

import os

curdir = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

if curdir == '/usr/share/pyshared':
    GUIDIR = '/usr/share/pyshared/canaimainstalador'
    SHAREDIR = '/usr/share/canaima-instalador'
else:
    GUIDIR = curdir + '/canaimainstalador'
    SHAREDIR = curdir

BAR_ICON = GUIDIR+'/data/img/icon.png'
ABOUT_IMAGE = GUIDIR+'/data/img/logo.png'
BANNER_IMAGE = GUIDIR+'/data/img/banner.png'
WELCOME_IMAGE = GUIDIR+'/data/img/welcome.png'
KEY_IMAGE_TMPL = GUIDIR+'/data/img/key_{0}.png'
INSTALL_SLIDES = GUIDIR+'/data/install.html'

VERSION_FILE = SHAREDIR + '/VERSION'
AUTHORS_FILE = SHAREDIR + '/AUTHORS'
LICENSE_FILE = SHAREDIR + '/LICENSE'
TRANSLATORS_FILE = SHAREDIR + '/TRANSLATORS'

APP_NAME = 'Canaima Instalador'
APP_COPYRIGHT = 'Copyright (C) 2012 - Varios autores'
APP_URL = 'http://code.google.com/p/canaima-instalador'
APP_DESCRIPTION = 'Instalador para Canaima GNU/Linux'

ESPACIO_ROOT = 1024 * 1024              # 1GB
ESPACIO_VAR = 1024 * 896                # 896MB
ESPACIO_HOME = 1024 * 1024              # 1GB
ESPACIO_USR = 1024 * 1024 * 2           # 2GB
ESPACIO_BOOT = 1024 * 128               # 128MB
ESPACIO_SWAP = 1024 * 1024              # 1GB
# --------------------------------------# -------
ESPACIO_TOTAL = 1024 * 1024 * 6         # 6GB

CFG = {
    's': []
    }

TECLADOS = {
    'es': 'Español, España',
    'latam': 'Español, Latinoamérica',
    'us': 'Inglés, Estados Unidos'
    }

FSPROGS = {
    'btrfs': ['mkfs.btrfs {0}', 'btrfs filesystem resize {0} {1}'],
    'ext2': ['mkfs.ext2 -q -F -F {0}', 'resize2fs -f {1} {0}'],
    'ext3': ['mkfs.ext3 -q -F -F {0}', 'resize2fs -f {1} {0}'],
    'ext4': ['mkfs.ext4 -q -F -F {0}', 'resize2fs -f {1} {0}'],
    'fat16': ['mkfs.vfat {0}', 'fatresize -q -s {0} {1}'],
    'fat32': ['mkfs.vfat {0}', 'fatresize -q -s {0} {1}'],
    'ntfs': ['mkfs.ntfs -q -F {0}', 'ntfsresize -f -P -b -s {0} {1}'],
    'hfs+': ['mkfs.hfsplus {0}', ''],
    'hfs': ['hformat -f {0}', ''],
    'jfs': ['mkfs.jfs -q {0}', ''],
    'swap': ['mkswap -f {0}', ''],
    'reiser4': ['mkfs.reiser4 -y -f {0}', ''],
    'reiserfs': ['mkfs.reiserfs -q -f -f {0}', 'resize_reiserfs -q -f -s {0} {1}'],
    'xfs': ['mkfs.xfs -q -f {0}', '']
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

