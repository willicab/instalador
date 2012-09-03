# Makefile

SHELL := sh -e
PYCS = $(shell find . -type f -iname "*.pyc")

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

clean-pyc:

	@printf "Cleaning precompilated python files ["
	@for PYC in $(PYCS); do \
		rm -rf $${PYC}; \
		printf "."; \
	done
	@printf "]\n"

install:

	@mkdir -p $(DESTDIR)/usr/bin
	@mkdir -p $(DESTDIR)/usr/share/canaima-instalador
	@mkdir -p $(DESTDIR)/etc/skel/Escritorio
	@mkdir -p $(DESTDIR)/etc/gdm3/Init

	@cp canaima-instalador.desktop $(DESTDIR)/etc/skel/Escritorio/
	@cp canaima-instalador $(DESTDIR)/usr/bin/canaima-instalador
	@cp -r data pasos scripts clases wizard.py canaima-instalador.py $(DESTDIR)/usr/share/canaima-instalador/

uninstall:

	@rm -rf $(DESTDIR)/usr/bin/canaima-instalador
	@rm -rf $(DESTDIR)/usr/share/canaima-instalador
	@rm -rf $(DESTDIR)/etc/skel/Escritorio/canaima-instalador.desktop

clean:

reinstall: uninstall install
