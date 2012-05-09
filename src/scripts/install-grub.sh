#!/bin/sh
# install-grub.sh
# Script to install grub in the MBR (based on yami distro)
# Modified by Gilberto Diaz.
# Syntax: install-grub.sh <mount_point> <argument for root instruction, ie (hd0,0)>
# lo ponemos aqui para no ver nada de lo que muestra grub y asi no casca yami
# We put here the command in order to avoid the output and the installer works ok


MOUNTPOINT=$1
DEVICE=$2

chroot ${MOUNTPOINT}/ mkdir -p /root/debs/
 
cp /live/image/pool/main/s/svgalib/libsvga1_1%3a1.4.3-29_i386.deb ${MOUNTPOINT}/root/debs/
cp /live/image/pool/main/libx/libx86/libx86-1_1.1+ds1-6_i386.deb ${MOUNTPOINT}/root/debs/
cp /live/image/pool/main/libs/libsdl1.2/libsdl1.2*.deb ${MOUNTPOINT}/root/debs/
cp /live/image/pool/main/g/gettext/gettext-base*.deb ${MOUNTPOINT}/root/debs/
cp /live/image/pool/main/b/burg/burg*.deb ${MOUNTPOINT}/root/debs/
cp /live/image/pool/main/b/burg-themes/burg*.deb ${MOUNTPOINT}/root/debs/

echo "#!/bin/bash" > ${MOUNTPOINT}/root/instalar-debs.sh
echo "" >> ${MOUNTPOINT}/root/instalar-debs.sh
echo "echo \"burg-pc burg/linux_cmdline string\" | debconf-set-selections" >> ${MOUNTPOINT}/root/instalar-debs.sh
echo "echo \"burg-pc burg/linux_cmdline_default string quiet splash vga=791\" | debconf-set-selections" >> ${MOUNTPOINT}/root/instalar-debs.sh
echo "echo \"burg-pc burg-pc/install_devices multiselect ${DEVICE}\" | debconf-set-selections" >> ${MOUNTPOINT}/root/instalar-debs.sh
echo "DEBIAN_FRONTEND=noninteractive dpkg -i /root/debs/libx86-1*.deb" >> ${MOUNTPOINT}/root/instalar-debs.sh
echo "DEBIAN_FRONTEND=noninteractive dpkg -i /root/debs/libsvga1*.deb" >> ${MOUNTPOINT}/root/instalar-debs.sh
echo "DEBIAN_FRONTEND=noninteractive dpkg -i /root/debs/libsdl1.2*.deb" >> ${MOUNTPOINT}/root/instalar-debs.sh
echo "DEBIAN_FRONTEND=noninteractive dpkg -i /root/debs/gettext-base*.deb" >> ${MOUNTPOINT}/root/instalar-debs.sh
echo "DEBIAN_FRONTEND=noninteractive dpkg -i /root/debs/burg-themes-common*.deb" >> ${MOUNTPOINT}/root/instalar-debs.sh
echo "DEBIAN_FRONTEND=noninteractive dpkg -i /root/debs/burg-themes_*.deb" >> ${MOUNTPOINT}/root/instalar-debs.sh
echo "DEBIAN_FRONTEND=noninteractive dpkg -i /root/debs/burg-common*.deb" >> ${MOUNTPOINT}/root/instalar-debs.sh
echo "DEBIAN_FRONTEND=noninteractive dpkg -i /root/debs/burg-emu*.deb" >> ${MOUNTPOINT}/root/instalar-debs.sh
echo "DEBIAN_FRONTEND=noninteractive dpkg -i /root/debs/burg-pc*.deb" >> ${MOUNTPOINT}/root/instalar-debs.sh
echo "DEBIAN_FRONTEND=noninteractive dpkg -i /root/debs/burg*.deb" >> ${MOUNTPOINT}/root/instalar-debs.sh
echo "aptitude purge canaima-instalador --assume-yes" >> ${MOUNTPOINT}/root/instalar-debs.sh
echo "dpkg-reconfigure cunaguaro guacharo canaima-estilo-visual canaima-plymouth canaima-escritorio-gnome canaima-chat canaima-bienvenido canaima-escritorio-gnome canaima-base" >> ${MOUNTPOINT}/root/instalar-debs.sh
echo "update-burg" >> ${MOUNTPOINT}/root/instalar-debs.sh

chmod +x ${MOUNTPOINT}/root/instalar-debs.sh
chroot ${MOUNTPOINT}/ bash /root/instalar-debs.sh

rm ${MOUNTPOINT}/root/instalar-debs.sh
rm -rf ${MOUNTPOINT}/root/debs/

[ -e ${MOUNTPOINT}/root/copiar-debs.sh ] && rm ${MOUNTPOINT}/root/copiar-debs.sh
