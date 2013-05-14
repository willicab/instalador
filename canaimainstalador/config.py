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

curdir = os.path.normpath(os.path.join(os.path.realpath(__file__), '..', '..'))

if curdir[:5] == '/usr/':
    GUIDIR = '/usr/share/pyshared/canaimainstalador'
    SHAREDIR = '/usr/share/canaima-instalador'
else:
    GUIDIR = curdir + '/canaimainstalador'
    SHAREDIR = curdir

def get_live_path():
    live_path = ''
    if os.path.exists('/lib/live/mount/medium/'):
        live_path = '/lib/live/mount/medium/'
    elif os.path.exists('/live/image/'):
        live_path = '/live/image/'
    else:
        raise Exception('Imposible encontrar imagen de disco.')

    print "Utilizando imágen de disco en %s" % live_path
    return live_path

BAR_ICON = GUIDIR + '/data/img/icon.png'
ABOUT_IMAGE = GUIDIR + '/data/img/logo.png'
BANNER_IMAGE = GUIDIR + '/data/img/banner.png'
WELCOME_IMAGE = GUIDIR + '/data/img/welcome.png'
KEY_IMAGE_TMPL = GUIDIR + '/data/img/key_{0}.png'
INSTALL_SLIDES = GUIDIR + '/data/install.html'

VERSION_FILE = SHAREDIR + '/VERSION'
AUTHORS_FILE = SHAREDIR + '/AUTHORS'
LICENSE_FILE = SHAREDIR + '/LICENSE'
TRANSLATORS_FILE = SHAREDIR + '/TRANSLATORS'

APP_NAME = 'Canaima Instalador'
APP_COPYRIGHT = 'Copyright (C) 2012 - Varios autores'
APP_URL = 'http://gitorious.org/canaima-gnu-linux/canaima-instalador'
APP_DESCRIPTION = 'Instalador para Canaima GNU/Linux'

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

TECLADOS = {
    'es': 'Español, España',
    'latam': 'Español, Latinoamérica',
    'us': 'Inglés, Estados Unidos'
    }

# TODO: Automatizar el proceso de nombrar los lenguajes (Verificar normas ISO)
LENGUAJES = [
    ('en_AG', 'Inglés, Antigua y Barbuda'),
    ('en_AU', 'Inglés, Australia'),
    ('en_BW', 'Inglés, Botswana'),
    ('en_CA', 'Inglés, Canadá'),
    ('en_DK', 'Inglés, Dinamarca'),
    ('en_GB', 'Inglés, Reino Unido'),
    ('en_HK', 'Inglés, Hong Kong'),
    ('en_IE', 'Inglés, Irlanda'),
    ('en_IN', 'Inglés, India'),
    ('en_NG', 'Inglés, Nigeria'),
    ('en_NZ', 'Inglés, Nueva Zelanda'),
    ('en_PH', 'Inglés, Filipinas'),
    ('en_SG', 'Inglés, Singapur'),
    ('en_US', 'Inglés, Estados Unidos'),
    ('en_ZA', 'Inglés, Sur África'),
    ('en_ZM', 'Inglés, Zambia'),
    ('en_ZW', 'Inglés, Zimbabue'),

    ('es_AR', 'Español, Argentina'),
    ('es_BO', 'Español, Bolivia'),
    ('es_CL', 'Español, Chile'),
    ('es_CO', 'Español, Colombia'),
    ('es_CR', 'Español, Costa Rica'),
    ('es_DO', 'Español, Dominicana'),
    ('es_EC', 'Español, Ecuador'),
    ('es_ES', 'Español, España'),
    ('es_GT', 'Español, Guatemala'),
    ('es_ES', 'Español, España'),
    ('es_HN', 'Español, Honduras'),
    ('es_MX', 'Español, Mexico'),
    ('es_PA', 'Español, Panamá'),
    ('es_PE', 'Español, Perú'),
    ('es_PR', 'Español, Puerto Rico'),
    ('es_PY', 'Español, Paraguay'),
    ('es_SV', 'Español, El Salvador'),
    ('es_US', 'Español, Estados Unidos'),
    ('es_UY', 'Español, Uruguay'),
    ('es_VE', 'Español, Venezuela'),

    ('pt_BR', 'Portugués, Brasil'),
    ('pt_PT', 'Portugués, Portugal'),
    ]

FSPROGS = {
    'btrfs': [
        ['mkfs.btrfs {0}'],
        ['btrfsck {1}', 'umount /mnt || true', 'sync', 'mount -t btrfs {1} /mnt', 'sync', 'btrfs filesystem resize {0} /mnt', 'umount /mnt', 'sync'],
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
        ['ntfsresize -P -i -f -v {1}', 'ntfsresize -P -f -n -s {0} {1}', 'echo y | ntfsresize -P -f -s {0} {1}'],
        ['ntfsresize -P -i -f -v {1}', 'ntfsresize -P -f -n {1}', 'echo y | ntfsresize -P -f {1}'],
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
        ['reiserfsck -q -y --fix-fixable {1} || true', 'echo y | resize_reiserfs -s {0} {1}'],
        ['reiserfsck -q -y --fix-fixable {1} || true', 'echo y | resize_reiserfs {1}'],
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
    'fat16': 1024 * 1024 * 4, # 4 Gb
    'hfs': 1024 * 1024 * 2, # 2 Gb
    }
