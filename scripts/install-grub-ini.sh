#!/bin/sh
# install-grub.sh
# Script to install grub in the MBR (based on yami distro)
# Modified by Gilberto Diaz.
# Syntax: install-grub.sh <mount_point> <argument for root instruction, ie (hd0,0)>
# lo ponemos aqui para no ver nada de lo que muestra grub y asi no casca yami
# We put here the command in order to avoid the output and the installer works ok

DEVICE=${1}
echo "burg-pc burg-pc/install_devices multiselect ${DEVICE}"
echo "burg-pc burg/linux_cmdline string quiet splash" | debconf-set-selections
echo "burg-pc burg/linux_cmdline_default string quiet splash vga=791" | debconf-set-selections
echo "burg-pc burg-pc/install_devices multiselect ${DEVICE}" | debconf-set-selections

DEBIAN_FRONTEND=noninteractive dpkg -i /live/image/pool/main/libx/libx86/libx86-1*.deb
DEBIAN_FRONTEND=noninteractive dpkg -i /live/image/pool/main/s/svgalib/libsvga1*.deb
DEBIAN_FRONTEND=noninteractive dpkg -i /live/image/pool/main/libs/libsdl1.2/libsdl1.2*.deb
DEBIAN_FRONTEND=noninteractive dpkg -i /live/image/pool/main/g/gettext/gettext-base*.deb
DEBIAN_FRONTEND=noninteractive dpkg -i /live/image/pool/main/b/burg-themes/burg-themes-common*.deb
DEBIAN_FRONTEND=noninteractive dpkg -i /live/image/pool/main/b/burg-themes/burg-themes_*.deb
DEBIAN_FRONTEND=noninteractive dpkg -i /live/image/pool/main/b/burg/burg-common*.deb
DEBIAN_FRONTEND=noninteractive dpkg -i /live/image/pool/main/b/burg/burg-emu*.deb
DEBIAN_FRONTEND=noninteractive dpkg -i /live/image/pool/main/b/burg/burg-pc*.deb
DEBIAN_FRONTEND=noninteractive dpkg -i /live/image/pool/main/b/burg/burg*.deb

