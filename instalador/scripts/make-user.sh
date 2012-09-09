#!/bin/sh
# Author          : Raúl Sánchez Sánchez  
# Created On      : Thu Mar 25 12:00:15 2003
# Last Modified By: Juan Jesús Ojeda Croissier
# Last Modified On: Wed May 28 17:48:44 2003
#
# USAGE: 
#    $ make-user.sh username password
# username: the name of new user or root
# password: password of user. Without this password
# make one entry without password in /etc/shadow

# Gettext
export TEXTDOMAINDIR=locale
export TEXTDOMAIN=make-user

#
# USER no ROOT
if [ "$1" != "root" ]; then
	chroot $3 /usr/sbin/userdel -r canaima
	echo "chroot $3 /usr/sbin/useradd -m -d /home/$1 $1 -s /bin/bash -c \"$4\""
	chroot $3 /usr/sbin/useradd -m -d /home/$1 $1 -s /bin/bash -c "$4"
fi

chroot $3 echo "$1:$2" > /tmp/passwd
# Putting the password
chroot $3 /usr/sbin/chpasswd < /tmp/passwd
# Cleaning
rm -f $3/tmp/passwd
