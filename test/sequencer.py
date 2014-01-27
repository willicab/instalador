'''
Created on 13/12/2013

@author: erick
'''
import unittest
from canaimainstalador import sequencer


class Test(unittest.TestCase):

    def setUp(self):
        self.sequence = [
                {"disc.umount_devices":(["/dev/sdc1"],)},
                {"disc.mount_devices":([("/dev/sdc1", "/montando/", "ext4")],)},
            ]

    def testSequencer(self):
        sequencer.start(self.sequence)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
