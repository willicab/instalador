#!/usr/bin/env python
# -*- coding: UTF-8 -*-

CFG = {'s': []}
BANNER = 'canaimainstalador/data/img/banner.png'

TECLADOS = {
    'Español, España' : 'es',
    'Español, Latinoamérica' : 'latam',
    'Ingles, Estados Unidos' : 'us'
}

ESPACIO_ROOT = 1024*1024                # 1GB
ESPACIO_VAR = 1024*896                  # 896MB
ESPACIO_HOME = 1024*1024                # 1GB
ESPACIO_USR = 1024*1024*2               # 2GB
ESPACIO_BOOT = 1024*128                 # 128MB
ESPACIO_SWAP = 1024*1024                # 1GB
# --------------------------------------# -------
ESPACIO_TOTAL = 1024*1024*6             # 6GB

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

SUPPORTED_FS = [
'btrfs', 'ext2', 'ext3', 'ext4', 'vfat', 'hfs',
'hfsplus', 'jfs', 'ntfs', 'xfs', 'reiser4', 'reiserfs'
]
