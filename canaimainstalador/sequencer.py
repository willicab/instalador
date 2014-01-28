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
import logging
import os
from canaimainstalador.config import SHAREDIR

SEQUENCE_DIR = SHAREDIR + "/sequences/"


class Step:
    """This class represents a step in the sequence of steps that is
    passed tothe sequencer."""

    __internal_package = "canaimainstalador.steps"
    __external_package = "canaimainstalador.plugins.steps"

    def __init__(self, data):
        self.__name = None  # Identificator name of the step
        self.__import_name = None  # from some.place import [import_name]
        self.__package = None  # from [package] import some_object
        self.__arguments = None  # arguments tha will receive the function

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
        pname = self.get_package()
        iname = self.get_import_name()
        args = self.get_arguments()

        logging.debug("Running step {0} from {1} with args {2}".format(iname,
            pname, args))

        callback = importlib.import_module(pname)
        caller = operator.methodcaller(iname, *args)

        caller(callback)


def append_steps(original, other):
    """Walk a list of steps and add each one to the original list."""
    for step in other:
        original.append(step)
    return original


def read_dir():
    """Read all .stp files in the 'sequences' directory and build the
    complete list of steps that will be performed during the
    installation process.
    """
    result = []
    # Read the sequences directory
    for walker in os.walk(SEQUENCE_DIR):
        files = walker[2]
        files.sort()
        # Search for '*.stp' files
        for seq_file in files:
            if seq_file[-4:] == ".stp":
                f_path = os.path.join(walker[0], seq_file)
                logging.debug("Reading sequence file: {}".format(f_path))
                with open(f_path) as f:
                    # Appends the new steps to the result list
                    append_steps(result, eval(f.read()))
    return result


# TODO
def write():
    pass


def start(sequence=None):
    """Starts the installation process.

    This function starts the instalation process that consists in a
    sequence of steps.
    """
    if not sequence:
        sequence = read_dir()

    logging.debug("Sequence to be processed:\n{0}".format(sequence))
    logging.info("Steps sequence started.")
    for steps in sequence:
        s = Step(steps)
        s.run()
    logging.info("Steps sequence finished.")
