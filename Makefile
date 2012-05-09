# Makefile
# El Makefile es una hoja de instruciones para ejecutar el programa GNU MAKE.
# A través de MAKE, es posible compilar, instalar, desinstalar, comprobar y limpiar
# el software que estamos distribuyendo. También es usado por debian/rules para
# construir el paquete (si se le especifica).
# Hay que tener claro dos cosas. Existen dos visiones en el desarrollo de software
# para Canaima GNU/Linux: la del desarrollador del software y la del mantenedor del
# paquete. La visión del desarrollador tiene un ámbito íntimamente relacionado con
# el Makefile: es a través de él que el desarrollador proporciona una herramienta
# al usuario para interactuar con su software (compilarlo, instalarlo, etc.). El
# desarrollador diseña su programa de forma genérica, para funcionar en un sistema
# GNU/Linux que soporte lenguajes conocidos (bash, C, C++, Python, Perl, entre otros);
# no se preocupa por las reglas ni particularidades de determinada Distribución
# GNU/Linux (Debian, Fedora, Gentoo, etc.). La visión del Mantenedor del paquete está
# enfocada a determinar cómo hacer funcionar el software del desarrollador en una
# determinada Distribución GNU/Linux, con sus reglas y particularidades. Para ello se
# vale de "los scripts del mantenedor" (preinst, postinst, prerm, postrm, rules), de
# los scripts de "control" (control, docs, conffiles, compat, etc.) y ocasionalmente
# (si la licencia y el autor lo permiten) puede modificar el código fuente del
# desarrollador para adaptarlo a sus necesidades.

SHELL := sh -e

SCRIPTS = "debian/preinst install" "debian/postinst configure" "debian/prerm remove" "debian/postrm remove"

all: build

test:

	# Aquí se realizan diversas pruebas para segurar que
	# todo lo que se realice con el Makefile salga bien
	# (compilación, instalación, desinstalación, entre otros)
	# Una práctica común es la de correr los scripts en modo
	# "de prueba" para comprobar que están bien escritos.

	@echo -n "\n===== Comprobando posibles errores de sintaxis en los scripts de mantenedor =====\n\n"

	@for SCRIPT in $(SCRIPTS); \
	do \
		echo -n "$${SCRIPT}\n"; \
		bash -n $${SCRIPT}; \
	done

	@echo -n "\n=================================================================================\nHECHO!\n\n"

build:

	# Aquí se realizan todos los procedimientos relativos a
	# generación de archivos que necesitan compilarse.
	# Por ejemplo, una conversión de imágenes PNG > png,
	# Debe ir aquí. La compilación de binarios C++, debe ir
	# aquí. Entre otros ejemplos. Todos los programas que
	# utilices acá, debes incluirlas como dependencias de
	# compilación en el campo "Build-Depends" del archivo
	# debian/control.
	# Si no hay nada que compilar (por ejemplo, si tu
	# programa está hecho en bash o PHP) puedes dejar éste
	# espacio en blanco.
	#
	# EJEMPLO:
	# convert ejemplo.png ejemplo.png

	@echo "Nada para compilar!"

install:

	# Aquí se instala el software. Para ello se mueven los
	# archivos necesarios a los lugares destinados para su
	# correcto funcionamiento. Es necesario crear todos los
	# directorios utilizados. Recuerda que el Makefile se
	# utiliza en la creación de la estructura de archivos 
	# del paquete.
	# Debes anteponer la variable $(DESTDIR) en todos los
	# destinos:
	# Si haces "make install", la variable $(DESTDIR) es
	# removida por no tener valor y el programa se instala
	# en el sistema tal cual.
	# Si utilizas el Makefile en el empaquetamiento, puedes
	# asignarle el valor DESTDIR=$(CURDIR)/debian/nombre-p/
	# para que sea el contenido del paquete.
	#
	# EJEMPLOS
	# mkdir -p $(DESTDIR)/usr/bin/
	# mkdir -p $(DESTDIR)/etc/skel/Escritorio/
	# cp -r desktop/nombre-p.desktop $(DESTDIR)/usr/share/applications/
	# cp -r scripts/nombre-p.py $(DESTDIR)/usr/share/nombre-p/
	# cp -r scripts/interfaz.glade $(DESTDIR)/usr/share/nombre-p/
	# cp -r scripts/canaima-bienvenido.sh $(DESTDIR)/usr/bin/nombre-p

	install -d $(DESTDIR)/usr/bin
	install -d $(DESTDIR)/usr/share/canaima-instalador
	install -d $(DESTDIR)/usr/share/canaima-instalador/data
	install -d $(DESTDIR)/usr/share/canaima-instalador/data/distribuciones
	install -d $(DESTDIR)/usr/share/canaima-instalador/data/preview
	install -d $(DESTDIR)/usr/share/canaima-instalador/clases
	install -d $(DESTDIR)/usr/share/canaima-instalador/clases/install
	install -d $(DESTDIR)/usr/share/canaima-instalador/pasos
	install -d $(DESTDIR)/usr/share/canaima-instalador/scripts
	install -d $(DESTDIR)/etc/skel/Escritorio

	install -m 755 src/canaima-instalador.desktop $(DESTDIR)/etc/skel/Escritorio/canaima-instalador.desktop
	install -m 755 src/canaima-instalador.py $(DESTDIR)/usr/share/canaima-instalador/canaima-instalador.py
	install -m 755 src/canaima-instalador $(DESTDIR)/usr/bin/canaima-instalador
	install -m 755 src/canaima-oem $(DESTDIR)/usr/bin/canaima-oem
	install -m 644 src/wizard.py $(DESTDIR)/usr/share/canaima-instalador/wizard.py
	install -m 644 src/oem/oem.py $(DESTDIR)/usr/share/canaima-instalador/oem/oem.py
	install -m 644 src/oem/usuario.html $(DESTDIR)/usr/share/canaima-instalador/oem/usuario.html
	install -m 755 src/oem/Default $(DESTDIR)/etc/gdm3/Init/Default
	install -m 644 src/data/banner-app-top.png $(DESTDIR)/usr/share/canaima-instalador/data/banner-app-top.png
	install -m 644 src/data/buscar-discos.png $(DESTDIR)/usr/share/canaima-instalador/data/buscar-discos.png
	install -m 644 src/data/distribuciones/es.png $(DESTDIR)/usr/share/canaima-instalador/data/distribuciones/es.png
	install -m 644 src/data/distribuciones/us.png $(DESTDIR)/usr/share/canaima-instalador/data/distribuciones/us.png
	install -m 644 src/data/distribuciones/latam.png $(DESTDIR)/usr/share/canaima-instalador/data/distribuciones/latam.png
	install -m 644 src/data/preview/carrusel.html $(DESTDIR)/usr/share/canaima-instalador/data/preview/carrusel.html
	install -m 644 src/data/preview/jquery-1.js $(DESTDIR)/usr/share/canaima-instalador/data/preview/jquery-1.js
	install -m 644 src/data/preview/image1.png $(DESTDIR)/usr/share/canaima-instalador/data/preview/image1.png
	install -m 644 src/data/preview/image2.png $(DESTDIR)/usr/share/canaima-instalador/data/preview/image2.png
	install -m 644 src/data/preview/image3.png $(DESTDIR)/usr/share/canaima-instalador/data/preview/image3.png
	install -m 644 src/data/preview/image4.png $(DESTDIR)/usr/share/canaima-instalador/data/preview/image4.png
	install -m 644 src/data/preview/image5.png $(DESTDIR)/usr/share/canaima-instalador/data/preview/image5.png
	install -m 644 src/data/preview/image6.png $(DESTDIR)/usr/share/canaima-instalador/data/preview/image6.png
	install -m 644 src/data/preview/image7.png $(DESTDIR)/usr/share/canaima-instalador/data/preview/image7.png
	install -m 644 src/pasos/bienvenida.py $(DESTDIR)/usr/share/canaima-instalador/pasos/bienvenida.py
	install -m 644 src/pasos/info.py $(DESTDIR)/usr/share/canaima-instalador/pasos/info.py
	install -m 644 src/pasos/__init__.py $(DESTDIR)/usr/share/canaima-instalador/pasos/__init__.py
	install -m 644 src/pasos/instalacion.py $(DESTDIR)/usr/share/canaima-instalador/pasos/instalacion.py
	install -m 644 src/pasos/metodo.py $(DESTDIR)/usr/share/canaima-instalador/pasos/metodo.py
	install -m 644 src/pasos/particion_auto.py $(DESTDIR)/usr/share/canaima-instalador/pasos/particion_auto.py
	install -m 644 src/pasos/particion_todo.py $(DESTDIR)/usr/share/canaima-instalador/pasos/particion_todo.py
	install -m 644 src/pasos/teclado.py $(DESTDIR)/usr/share/canaima-instalador/pasos/teclado.py
	install -m 644 src/pasos/usuario.py $(DESTDIR)/usr/share/canaima-instalador/pasos/usuario.py
	install -m 755 src/scripts/install-grub.sh $(DESTDIR)/usr/share/canaima-instalador/scripts/install-grub.sh
	install -m 755 src/scripts/install-grub-ini.sh $(DESTDIR)/usr/share/canaima-instalador/scripts/install-grub-ini.sh
	install -m 755 src/scripts/make-user.sh $(DESTDIR)/usr/share/canaima-instalador/scripts/make-user.sh
	install -m 644 src/clases/tabla_particiones.py $(DESTDIR)/usr/share/canaima-instalador/clases/tabla_particiones.py
	install -m 644 src/clases/particion_nueva.py $(DESTDIR)/usr/share/canaima-instalador/clases/particion_nueva.py
	install -m 644 src/clases/particiones.py $(DESTDIR)/usr/share/canaima-instalador/clases/particiones.py
	install -m 644 src/clases/barra_auto.py $(DESTDIR)/usr/share/canaima-instalador/clases/barra_auto.py
	install -m 644 src/clases/barra_particiones.py $(DESTDIR)/usr/share/canaima-instalador/clases/barra_particiones.py
	install -m 644 src/clases/barra_todo.py $(DESTDIR)/usr/share/canaima-instalador/clases/barra_todo.py
	install -m 644 src/clases/distribuciones.py $(DESTDIR)/usr/share/canaima-instalador/clases/distribuciones.py
	install -m 644 src/clases/general.py $(DESTDIR)/usr/share/canaima-instalador/clases/general.py
	install -m 644 src/clases/get_partitions.py $(DESTDIR)/usr/share/canaima-instalador/clases/get_partitions.py
	install -m 644 src/clases/__init__.py $(DESTDIR)/usr/share/canaima-instalador/clases/__init__.py
	install -m 644 src/clases/leyenda_auto.py $(DESTDIR)/usr/share/canaima-instalador/clases/leyenda_auto.py
	install -m 644 src/clases/leyenda_todo.py $(DESTDIR)/usr/share/canaima-instalador/clases/leyenda_todo.py
	install -m 644 src/clases/install/fstab.py $(DESTDIR)/usr/share/canaima-instalador/clases/install/fstab.py
	install -m 644 src/clases/install/__init__.py $(DESTDIR)/usr/share/canaima-instalador/clases/install/__init__.py
	install -m 644 src/clases/install/particion_auto.py $(DESTDIR)/usr/share/canaima-instalador/clases/install/particion_auto.py
	install -m 644 src/clases/install/particion_todo.py $(DESTDIR)/usr/share/canaima-instalador/clases/install/particion_todo.py
	
uninstall:

# Aquí se deshace lo que se hizo en el install, borrando exactamente lo que
# se creó en el install

clean:

# Borrar todo lo hecho en build para que quede todo como estaba antes de la
# compilación

reinstall: uninstall install
