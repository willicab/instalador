#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

LONG_DESCRIPTION = """Instalador Vivo para el proyecto canaima GNU/Linux"""

# TODO: Maybe find some better ways to do this
# looking distutils's copy_tree method
data_files=[
    ('./', ['AUTHORS']),
    ('share/pixmaps', ['canaima/instalador/data/canaima.png']),
    ('share/applications', ['canaima-instalador.desktop']),
    ('share/doc/canaima-instalador', ['THANKS', 'README', 'COPYING']),
]

setup(name="canaima.instalador",
      version='3.1',
      description="Instalador Vivo para el proyecto canaima GNU/Linux",
      long_description=LONG_DESCRIPTION,
      author="Wil Alvarez",
      author_email="wil.alejandro@gmail.com",
      maintainer="Wil Alvarez",
      maintainer_email="wil.alejandro@gmail.com",
      url="http://canaima.softwarelibre.gob.ve",
      license="GPLv3",
      keywords='canaima gnu linux live installer',
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: X11 Applications :: GTK",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
      ],
      namespace_packages=['canaima'],
      packages=find_packages(),
      package_data={
        'instalador': ['data/distribuciones/*', 'data/preview/*', 'data/*']
      },
      entry_points={
        'console_scripts': [
            'canaima-instalador = canaima.instalador.main:Instalador',
        ],
      },
      data_files=data_files,
)
