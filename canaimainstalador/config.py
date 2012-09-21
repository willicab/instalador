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
ESPACIO_TOTAL = 1024*1024*1             # 6GB

FSPROGS = {
'btrfs': ['mkfs.btrfs', 'btrfsctl'],
'ext2': ['mkfs.ext2 -q -j -F -F', 'resize2fs'],
'ext3': ['mkfs.ext3 -q -j -F -F', 'resize2fs'],
'ext4': ['mkfs.ext4 -q -j -F -F', 'resize2fs'],
'fat16': ['mkfs.vfat', 'fatresize'],
'fat32': ['mkfs.vfat', 'fatresize'],
'ntfs': ['mkfs.ntfs -q -F', 'ntfsresize'],
'hfs+': ['mkfs.hfsplus', 'parted'],
'hfs': ['hformat -f', 'parted'],
'jfs': ['mkfs.jfs -q', ''],
'swap': ['mkswap -f', ''],
'reiser4': ['mkfs.reiser4 -y -f', ''],
'reiserfs': ['mkfs.reiserfs -q -f -f', 'resize_reiserfs'],
'xfs': ['mkfs.xfs -q -f', '']
}

