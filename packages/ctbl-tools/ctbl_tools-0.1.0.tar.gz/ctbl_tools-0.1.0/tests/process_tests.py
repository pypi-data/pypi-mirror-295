import unittest, os, sys
sys.path.append(os.path.normpath(os.path.join(os.path.abspath(sys.path[0]), '../src')))
from cbl_tools.process import process

class TestProcess(unittest.TestCase):

    tp = None

    def setUp(self):
        self.tp = process()
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_ls(self):
        self.tp.run("ls")
        self.assertEqual(self.tp.command, "ls")
        self.assertEqual(self.tp.returncode, 0)
        self.assertTrue(self.tp.is_ok())
        self.assertTrue(self.tp.is_there_stdout())
        self.assertFalse(self.tp.is_there_stderr())

    def test_str(self):
        self.assertEqual(str(self.tp), "<Empty cbl_tools.process object>")

    def test_id(self):
        self.tp.run("whoami")
        self.assertEqual(self.tp.returncode, 0)
        self.assertEqual(len(self.tp.stdout), 1)
        username = self.tp.stdout[0]

        self.tp.reset()
        self.tp.run("id")
        self.assertEqual(self.tp.returncode, 0)
        self.assertEqual(len(self.tp.stdout), 1)
        lst = self.tp.extract(r"(\w+)=(\d+)\((\w+)\)")

        for elem in lst:
            self.assertEqual(elem[2], username)

if __name__ == '__main__':
    unittest.main(verbosity=2)
