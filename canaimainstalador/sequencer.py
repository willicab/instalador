# -*- coding: UTF-8 -*-
'''
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Ucumari; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA

Created on 12/12/2013

@author: Erick Birbe <erickcion@gmail.com>
'''
import importlib
import operator


class Step:
    """This class represents a step in the sequence of steps that is
    passed tothe sequencer."""

    __internal_package = "canaimainstalador.steps"
    __external_package = "canaimainstalador.plugins.steps"

    def __init__(self, data):
        self.__name = None
        self.__import_name = None
        self.__package = None
        self.__arguments = None

        self.__set_arguments(data)
        self.__set_import_data(data)

    def get_arguments(self):
        """Get the arguments passed to the callable option."""
        return self.__arguments

    def __set_arguments(self, data):
        if not self.__arguments:
            self.__arguments = data.values()[0]

    def get_name(self):
        """Get a identification name of the step."""
        return self.__name

    def __set_name(self, data):
        if not self.__name:
            self.__name = data.keys()[0]

    def __set_import_data(self, data):
        """Build the package path and set the import name."""

        self.__set_name(data)

        if '.' in self.__name:
            pos = self.__name.rfind('.')
            pkg = self.__name[0:pos]
            iname = self.__name[pos + 1:]
        else:
            pkg = ''
            iname = self.__name

        self.__package = pkg
        self.__import_name = iname

    def get_package(self, external=False):
        """Get the package name.

        Returns the package where to find the callable object.
        """
        if external:
            suffix = self.__external_package
        else:
            suffix = self.__internal_package
        return suffix + "." + self.__package

    def get_import_name(self):
        """Get the name of the fucntion or method to be called"""
        return self.__import_name

    def run(self):
        """Execute the Step callback"""
        callback = importlib.import_module(self.get_package())
        caller = operator.methodcaller(self.get_import_name(),
                                       *self.get_arguments())
        caller(callback)


def start(sequence):
    """Starts the installation process.

    This function starts the instalation process that consists in a
    sequence of steps.
    """
    for steps in sequence:
        s = Step(steps)
        s.run()
