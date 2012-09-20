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
'ext2': ['mkfs.ext2', 'resize2fs'],
'ext3': ['mkfs.ext3', 'resize2fs'],
'ext4': ['mkfs.ext4', 'resize2fs'],
'fat16': ['mkdosfs', ''],
'fat32': ['mkdosfs', ''],
'ntfs': ['mkfs.ntfs', 'ntfsresize'],
'hfs+': ['mkfs.hfsplus', ''],
'hfs': ['hformat', ''],
'jfs': ['mkfs.jfs', ''],
'swap': ['mkswap', ''],
'reiser4': ['mkfs.reiser4', ''],
'reiserfs': ['mkfs.reiserfs', 'resize_reiserfs'],
'xfs': ['mkfs.xfs', '']
}

