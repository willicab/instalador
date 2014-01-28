'''
Created on 13/12/2013

@author: Erick Birbe
'''
import unittest
from canaimainstalador import sequencer
from canaimainstalador.config import SHAREDIR


class Test(unittest.TestCase):

    def setUp(self):
        f = open(SHAREDIR + "/sequences/001_default.stp")
        self.sequence = eval(f.read())

    def test_append_steps(self):
        original = [1, 2.3, 4]
        other = ('a', "BCD", 'F')
        result = sequencer.append_steps(original, other)
        self.assertSequenceEqual(result, [1, 2.3, 4, 'a', "BCD", 'F'])

    def test_read(self):
        print sequencer.read_dir()

    def test_start(self):
        sequencer.start(self.sequence)


if __name__ == "__main__":
    unittest.main()
