# Makefile

SHELL := sh -e
PYCS = $(shell find . -type f -iname "*.pyc")
IMAGES = $(shell ls -1 canaimainstalador/data/img/ | grep "\.svg" | sed 's/\.svg//g')
SLIDES = $(shell ls -1 canaimainstalador/data/slides/ | grep "\.svg" | sed 's/\.svg//g')
CONVERT = $(shell which convert)

SCRIPTS = "debian/preinst install" "debian/postinst configure" "debian/prerm remove" "debian/postrm remove"

all: build

build:

	@echo "Nada para compilar!"

gen-img: clean-img

	@printf "Generando imágenes desde las fuentes [SVG > PNG,JPG] ["
	@for IMAGE in $(IMAGES); do \
		$(CONVERT) -background None canaimainstalador/data/img/$${IMAGE}.svg canaimainstalador/data/img/$${IMAGE}.png; \
		printf "."; \
	done;
	@for SLIDE in $(SLIDES); do \
		$(CONVERT) -background None canaimainstalador/data/slides/$${SLIDE}.svg canaimainstalador/data/slides/$${SLIDE}.png; \
		$(CONVERT) -background None canaimainstalador/data/slides/$${SLIDE}.png canaimainstalador/data/slides/$${SLIDE}.jpg; \
		printf "."; \
	done;
	@printf "]\n"

clean-img:

	@printf "Cleaning generated images [JPG,PNG] ["
	@for IMAGE in $(IMAGES); do \
		rm -rf canaimainstalador/data/img/$${IMAGE}.png; \
		printf "."; \
	done
	@for SLIDE in $(SLIDES); do \
		rm -rf canaimainstalador/data/slides/$${SLIDE}.png; \
		rm -rf canaimainstalador/data/slides/$${SLIDE}.jpg; \
		printf "."; \
	done
	@printf "]\n"

clean-pyc:

	@printf "Cleaning precompilated python files ["
	@for PYC in $(PYCS); do \
		rm -rf $${PYC}; \
		printf "."; \
	done
	@printf "]\n"

install:

	@mkdir -p $(DESTDIR)/usr/bin
	@mkdir -p $(DESTDIR)/usr/share/pyshared
	@mkdir -p $(DESTDIR)/etc/skel/Escritorio
	@mkdir -p $(DESTDIR)/etc/gdm3/Init

	@cp canaima-instalador.desktop $(DESTDIR)/etc/skel/Escritorio/
	@cp canaima-instalador.py $(DESTDIR)/usr/bin/canaima-instalador
	@cp -r instalador $(DESTDIR)/usr/share/pyshared/

uninstall:

	@rm -rf $(DESTDIR)/usr/bin/canaima-instalador
	@rm -rf $(DESTDIR)/usr/share/canaima-instalador
	@rm -rf $(DESTDIR)/etc/skel/Escritorio/canaima-instalador.desktop

clean:

reinstall: uninstall install
