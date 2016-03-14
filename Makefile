# Makefile

SHELL := sh -e
PYCS = $(shell find . -type f -iname "*.pyc")
IMAGES = $(shell ls -1 instalador/data/img/ | grep "\.svg" | sed 's/\.svg//g')
SLIDES = $(shell ls -1 instalador/data/slides/ | grep "\.svg" | sed 's/\.svg//g')
CONVERT = $(shell which convert)
SHELLBIN = $(shell which sh)
PYTHON = $(shell which python)
SHELLBIN = $(shell which sh)
GIT = $(shell which git)
MSGMERGE = $(shell which msgmerge)
XGETTEXT = $(shell which xgettext)
DEVSCRIPTS = $(shell which debuild)
DPKGDEV = $(shell which dpkg-buildpackage)
DEBHELPER = $(shell which dh)
GBP = $(shell which git-buildpackage)
LINTIAN = $(shell which lintian)
GNUPG = $(shell which gpg)
MD5SUM = $(shell which md5sum)
TAR = $(shell which tar)
BASHISMS = $(shell which checkbashisms)
LC_DIRS = $(shell ls locale)

# Variables de traducciones
DOMAIN_NAME = instalador

all: build

build: gen-img gen-mo-files

gen-img: clean-img

	@printf "Generando imágenes desde las fuentes [SVG > JPG,PNG] ["
	@for IMAGE in $(IMAGES); do \
		$(CONVERT) -background None instalador/data/img/$${IMAGE}.svg instalador/data/img/$${IMAGE}.png; \
		printf "."; \
	done;
	@for SLIDE in $(SLIDES); do \
		$(CONVERT) -background None instalador/data/slides/$${SLIDE}.svg instalador/data/slides/$${SLIDE}.png; \
		$(CONVERT) -background None instalador/data/slides/$${SLIDE}.png instalador/data/slides/$${SLIDE}.jpg; \
		printf "."; \
	done;
	@printf "]\n"

clean-img:

	@printf "Cleaning generated images [JPG,PNG] ["
	@for IMAGE in $(IMAGES); do \
		rm -rf instalador/data/img/$${IMAGE}.png; \
		printf "."; \
	done;
	@for SLIDE in $(SLIDES); do \
		rm -rf instalador/data/slides/$${SLIDE}.png; \
		rm -rf instalador/data/slides/$${SLIDE}.jpg; \
		printf "."; \
	done;
	@printf "]\n"

clean-pyc:

	@printf "Cleaning precompilated python files ["
	@for PYC in $(PYCS); do \
		rm -rf $${PYC}; \
		printf "."; \
	done
	@printf "]\n"

install:

	mkdir -p $(DESTDIR)/usr/bin
	mkdir -p $(DESTDIR)/usr/share/pyshared
	mkdir -p $(DESTDIR)/usr/share/instalador
	mkdir -p $(DESTDIR)/etc/skel/Escritorio
	mkdir -p $(DESTDIR)/etc/xdg/autostart/
	mkdir -p $(DESTDIR)/usr/share/applications/

	cp -r instalador $(DESTDIR)/usr/share/pyshared/
	cp VERSION AUTHORS LICENSE TRANSLATORS \
		$(DESTDIR)/usr/share/instalador/
	cp -r templates/ $(DESTDIR)/usr/share/instalador/

	cp instalador.py $(DESTDIR)/usr/bin/instalador
	chmod +x $(DESTDIR)/usr/bin/instalador

	# Instalar traducciones
	mkdir -p $(DESTDIR)/usr/share/locale/
	for LC in $(LC_DIRS); do \
		LOCALE_DIR=locale/$${LC}; \
		if [ -d $${LOCALE_DIR} ]; then \
			cp -r $${LOCALE_DIR} $(DESTDIR)/usr/share/locale/; \
		fi; \
	done

	# Removiendo archivos de imagenes innecesarios
	rm -rf $(DESTDIR)/usr/share/pyshared/instalador/data/slides/*.png
	rm -rf $(DESTDIR)/usr/share/pyshared/instalador/data/slides/*.svg
	rm -rf $(DESTDIR)/usr/share/pyshared/instalador/data/img/*.svg

	# Accesos directos
	cp instalador.desktop $(DESTDIR)/etc/skel/Escritorio/
	cp instalador.desktop $(DESTDIR)/etc/xdg/autostart/
	cp instalador.desktop $(DESTDIR)/usr/share/applications/

uninstall:

	rm -f $(DESTDIR)/usr/bin/instalador
	rm -rf $(DESTDIR)/usr/share/pyshared/instalador/

	# Remover accesos directos
	rm -f $(DESTDIR)/etc/skel/Escritorio/instalador.desktop
	rm -f $(DESTDIR)/etc/xdg/autostart/instalador.desktop
	rm -f $(DESTDIR)/usr/share/applications/instalador.desktop

	# Desinstalar traducciones
	rm -f $(DESTDIR)/usr/share/locale/*/LC_MESSAGES/$(DOMAIN_NAME).mo
	# Removiendo accesos directos
	rm -f $(DESTDIR)/usr/share/applications/instalador.desktop \
	  $(DESTDIR)/etc/xdg/autostart/instalador.desktop \
	  $(DESTDIR)/etc/skel/Escritorio/instalador.desktop

clean: clean-img clean-pyc clean-mo-files

reinstall: uninstall install

snapshot: check-maintdep

	@$(MAKE) clean
	@$(SHELLBIN) tools/snapshot.sh

release: check-maintdep

	@$(MAKE) clean
	@$(SHELLBIN) tools/release.sh

deb-test-snapshot: check-maintdep

	@$(MAKE) clean
	@$(SHELLBIN) tools/buildpackage.sh test-snapshot

deb-test-release: check-maintdep

	@$(MAKE) clean
	@$(SHELLBIN) tools/buildpackage.sh test-release

deb-final-release: check-maintdep

	@$(MAKE) clean
	@$(SHELLBIN) tools/buildpackage.sh final-release

check-maintdep:

	@printf "Checking if we have python ... "
	@if [ -z $(PYTHON) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"python\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have a shell ... "
	@if [ -z $(SHELLBIN) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"bash\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have git... "
	@if [ -z $(GIT) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"git-core\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have debhelper ... "
	@if [ -z $(DEBHELPER) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"debhelper\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have devscripts ... "
	@if [ -z $(DEVSCRIPTS) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"devscripts\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have dpkg-dev ... "
	@if [ -z $(DPKGDEV) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"dpkg-dev\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have git-buildpackage ... "
	@if [ -z $(GBP) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"git-buildpackage\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have lintian ... "
	@if [ -z $(LINTIAN) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"lintian\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have gnupg ... "
	@if [ -z $(GNUPG) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"gnupg\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have md5sum ... "
	@if [ -z $(MD5SUM) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"coreutils\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have tar ... "
	@if [ -z $(TAR) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"tar\" package."; \
		exit 1; \
	fi
	@echo

gen-pot-template:

	find . -type f -name \*.py | xgettext --language=Python --copyright-holder \
	"William Cabrera <william@linux.es>" --package-name "instalador" \
	--msgid-bugs-address "william@linux.es" -F \
	-o locale/messages.pot -f -

update-po-files: gen-pot-template

	msgmerge locale/es.po locale/messages.pot -o locale/es.po

gen-mo-files:

	mkdir -p locale/es/LC_MESSAGES/
	msgfmt locale/es.po -o locale/es/LC_MESSAGES/$(DOMAIN_NAME).mo

clean-mo-files:
	for LC in $(LC_DIRS); do \
		LOCALE_DIR=locale/$${LC}; \
		if [ -d $${LOCALE_DIR} ]; then \
			rm -r $${LOCALE_DIR}/; \
		fi; \
	done
