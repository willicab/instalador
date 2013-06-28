# Makefile

SHELL := sh -e
PYCS = $(shell find . -type f -iname "*.pyc")
IMAGES = $(shell ls -1 canaimainstalador/data/img/ | grep "\.svg" | sed 's/\.svg//g')
SLIDES = $(shell ls -1 canaimainstalador/data/slides/ | grep "\.svg" | sed 's/\.svg//g')
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

# Variables de tradicciones
DOMAIN_NAME = canaimainstalador

all: build

build: gen-img gen-mo-files

gen-img: clean-img

	@printf "Generando imágenes desde las fuentes [SVG > JPG,PNG] ["
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
	done;
	@for SLIDE in $(SLIDES); do \
		rm -rf canaimainstalador/data/slides/$${SLIDE}.png; \
		rm -rf canaimainstalador/data/slides/$${SLIDE}.jpg; \
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
	mkdir -p $(DESTDIR)/usr/share/canaima-instalador
	mkdir -p $(DESTDIR)/etc/skel/Escritorio
	mkdir -p $(DESTDIR)/etc/xdg/autostart/

	cp canaima-instalador.desktop $(DESTDIR)/etc/skel/Escritorio/
	cp canaima-instalador.desktop $(DESTDIR)/etc/xdg/autostart/
	cp -r canaimainstalador $(DESTDIR)/usr/share/pyshared/
	cp VERSION AUTHORS LICENSE TRANSLATORS \
		$(DESTDIR)/usr/share/canaima-instalador/
	cp -r templates/ $(DESTDIR)/usr/share/canaima-instalador/

	cp canaima-instalador.py $(DESTDIR)/usr/bin/canaima-instalador
	chmod +x $(DESTDIR)/usr/bin/canaima-instalador

	# Instalar traducciones
	mkdir -p $(DESTDIR)/usr/share/locale/
	for LC in $(LC_DIRS); do \
		LOCALE_DIR=locale/$${LC}; \
		if [ -d $${LOCALE_DIR} ]; then \
			cp -r $${LOCALE_DIR} $(DESTDIR)/usr/share/locale/; \
		fi; \
	done


	# Removiendo archivos de imagenes innecesarios
	rm -rf $(DESTDIR)/usr/share/pyshared/canaimainstalador/data/slides/*.png
	rm -rf $(DESTDIR)/usr/share/pyshared/canaimainstalador/data/slides/*.svg
	rm -rf $(DESTDIR)/usr/share/pyshared/canaimainstalador/data/img/*.svg

uninstall:

	rm -rf $(DESTDIR)/usr/bin/canaima-instalador
	rm -rf $(DESTDIR)/usr/share/pyshared/canaimainstalador
	rm -rf $(DESTDIR)/etc/skel/Escritorio/canaima-instalador.desktop
	rm -f $(DESTDIR)/etc/xdg/autostart/canaima-instalador.desktop

	# Desinstalar traducciones
	rm -f $(DESTDIR)/usr/share/locale/*/LC_MESSAGES/$(DOMAIN_NAME).mo

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
	"Erick Birbe <erickcion@gmail.com>" --package-name "canaima-instalador" \
	--msgid-bugs-address "desarrolladores@canaima.softwarelibre.gob.ve" -F \
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
