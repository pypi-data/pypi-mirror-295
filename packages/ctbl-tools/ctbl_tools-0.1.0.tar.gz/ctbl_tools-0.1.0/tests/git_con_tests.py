import unittest, os, sys
sys.path.append(os.path.normpath(os.path.join(os.path.abspath(sys.path[0]), '../src')))
from cbl_tools import process

class TestGitRemote(unittest.TestCase):

    def setUp(self):
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

if __name__ == '__main__':
    unittest.main(verbosity=2)
