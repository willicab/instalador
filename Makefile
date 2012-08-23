# Makefile

SHELL := sh -e

SCRIPTS = "debian/preinst install" "debian/postinst configure" "debian/prerm remove" "debian/postrm remove"

all: build

test:

	@echo -n "\n===== Comprobando posibles errores de sintaxis en los scripts de mantenedor =====\n\n"

	@for SCRIPT in $(SCRIPTS); \
	do \
		echo -n "$${SCRIPT}\n"; \
		bash -n $${SCRIPT}; \
	done

	@echo -n "\n=================================================================================\nHECHO!\n\n"

build:

	@echo "Nada para compilar!"

install:

	install -d $(DESTDIR)/usr/bin
	install -d $(DESTDIR)/usr/share/canaima-instalador
	#install -d $(DESTDIR)/usr/share/canaima-instalador/oem
	install -d $(DESTDIR)/usr/share/canaima-instalador/data
	install -d $(DESTDIR)/usr/share/canaima-instalador/data/distribuciones
	install -d $(DESTDIR)/usr/share/canaima-instalador/data/preview
	install -d $(DESTDIR)/usr/share/canaima-instalador/clases
	install -d $(DESTDIR)/usr/share/canaima-instalador/clases/install
	install -d $(DESTDIR)/usr/share/canaima-instalador/pasos
	install -d $(DESTDIR)/usr/share/canaima-instalador/scripts
	install -d $(DESTDIR)/etc/skel/Escritorio
	install -d $(DESTDIR)/etc/gdm3/Init

	install -m 755 src/canaima-instalador.desktop $(DESTDIR)/etc/skel/Escritorio/canaima-instalador.desktop
	install -m 755 src/canaima-instalador.py $(DESTDIR)/usr/share/canaima-instalador/canaima-instalador.py
	install -m 755 src/canaima-instalador $(DESTDIR)/usr/bin/canaima-instalador
	install -m 644 src/wizard.py $(DESTDIR)/usr/share/canaima-instalador/wizard.py
	install -m 644 src/data/wait.gif $(DESTDIR)/usr/share/canaima-instalador/data/wait.gif
	install -m 644 src/data/canaima.png $(DESTDIR)/usr/share/canaima-instalador/data/canaima.png
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
	install -m 644 src/pasos/particion_manual.py $(DESTDIR)/usr/share/canaima-instalador/pasos/particion_manual.py
	install -m 644 src/pasos/particion_auto.py $(DESTDIR)/usr/share/canaima-instalador/pasos/particion_auto.py
	install -m 644 src/pasos/particion_todo.py $(DESTDIR)/usr/share/canaima-instalador/pasos/particion_todo.py
	install -m 644 src/pasos/teclado.py $(DESTDIR)/usr/share/canaima-instalador/pasos/teclado.py
	install -m 644 src/pasos/usuario.py $(DESTDIR)/usr/share/canaima-instalador/pasos/usuario.py
	install -m 644 src/pasos/accesibilidad.py $(DESTDIR)/usr/share/canaima-instalador/pasos/accesibilidad.py
	install -m 755 src/scripts/install-grub.sh $(DESTDIR)/usr/share/canaima-instalador/scripts/install-grub.sh
	install -m 755 src/scripts/install-grub-ini.sh $(DESTDIR)/usr/share/canaima-instalador/scripts/install-grub-ini.sh
	install -m 755 src/scripts/make-user.sh $(DESTDIR)/usr/share/canaima-instalador/scripts/make-user.sh
	install -m 644 src/clases/tabla_particiones.py $(DESTDIR)/usr/share/canaima-instalador/clases/tabla_particiones.py
	install -m 644 src/clases/particion_nueva.py $(DESTDIR)/usr/share/canaima-instalador/clases/particion_nueva.py
	install -m 644 src/clases/particiones.py $(DESTDIR)/usr/share/canaima-instalador/clases/particiones.py
	install -m 644 src/clases/barra_manual.py $(DESTDIR)/usr/share/canaima-instalador/clases/barra_manual.py
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
	install -m 644 src/clases/install/particion_manual.py $(DESTDIR)/usr/share/canaima-instalador/clases/install/particion_manual.py
	
uninstall:

	rm -rf $(DESTDIR)/usr/bin/canaima-instalador
	rm -rf $(DESTDIR)/usr/share/canaima-instalador
	rm -rf $(DESTDIR)/etc/skel/Escritorio/canaima-instalador.desktop

clean:

reinstall: uninstall install
