import unittest, os, sys, tempfile, errno
sys.path.append(os.path.normpath(os.path.join(os.path.abspath(sys.path[0]), '../src')))
from cbl_tools import config, create_tempdir


class ConfigTests(unittest.TestCase):

    x = None

    def setUp(self) -> None:
        self.x = config.config(initpath=create_tempdir(True) + '/zort.ini', default_section='base')
        return super().setUp()

    def _create_values(self):
        self.x.add_section('blabla')
        self.x.set('blabla', 'a', '1')
        self.x.set('blabla', 'b', 'be')
        self.x.set('blabla', 'c', '3.141592653')
        self.x.set('blabla', 'switch', 'on')
        self.x.add_section('naka')
        self.x.set('naka', 'valor1', 'a${blabla:a}c${blabla:c}zzz${blabla:b}')
        self.x.set(None, 'tres', 'cuatro')

    def test_exceptions(self):
        # Opening an inexistent folder should raise an OSError:1
        try:
            config.config(initpath = os.path.join(tempfile.gettempdir(), "inexistent_folder_029837492837498/file.txt"), create_folder=False)
        except FileNotFoundError as e:
            self.assertEqual(e.errno, errno.ENOENT, "An inexistent path with false create_folder should raise a FileNotFoundError")

        try:
            config.config(initpath = os.path.join(tempfile.gettempdir(), 'X', 'Y'))
        except FileNotFoundError as e:
            self.assertEqual(e.errno, errno.ENOENT, "More than two inexistent folders should raise a FileNotFoundError")

        try:
            config.config(initpath = '/root/my_own_folder/file.txt')
        except PermissionError as e:
            self.assertEqual(e.errno, errno.EACCES, "Trying to create a folder within /root should raise a PermissionError!")

    def test_create_normal_config(self):
        # If asked to open an inexistent folder within a valid path, I should be able to create it.
        path = os.path.dirname(self.x.path)
        self.assertTrue(os.path.exists(path), f"Config should be able to create folder {path}")
        self.assertTrue(os.path.isdir(path), f"{path} should be a folder (it's not)")

        # Create a few values and then retrieve them
        self.assertFalse(self.x.has_section('blabla'), "An inexistent section ('blabla') exists")
        self._create_values()
        self.assertTrue(self.x.has_section('blabla'), "Cannot create section 'blabla'")
        self.assertEqual(self.x.get('blabla', 'a'), '1', 'get(blabla:a) should be equal to \'1\'; it\'s not')
        self.assertEqual(int(self.x.get('blabla', 'a')), 1, 'getint(blabla:a) should be equal to 1; it\'s not')
        self.assertEqual(self.x.get('blabla', 'b'), 'be', 'get(blabla:b) should be equal to \'be\'; it\'s not')
        self.assertEqual(float(self.x.get('blabla', 'c')), 3.141592653, 'getint(blabla:c) should be equal to pi; it\'s not')
        self.assertTrue(bool(self.x.get('blabla', 'switch')), 'getbool(blabla:switch) should be True; it\'s not')

    def test_interpolation(self):
        self._create_values()
        self.assertTrue(self.x.has_section('naka'), "Cannot create section 'naka'")
        self.assertEqual(self.x.get('naka', 'valor1'), 'a1c3.141592653zzzbe')

    def test_abusive_conf(self):
        try:
            self.x = config.config(os.getenv("HOME") + "/../another_user")
        except ValueError:
            pass

    def test_store_and_retrieve(self):
        self._create_values()
        self.x.flush()

        y = config.config(initpath=self.x.path, create_folder=False)
        self.assertTrue(y.has_section('blabla'), "Cannot create section 'blabla'")
        self.assertEqual(y.get('blabla', 'a'), '1', 'get(blabla:a) should be equal to \'1\'; it\'s not')
        self.assertEqual(y.get('blabla', 'b'), 'be', 'get(blabla:b) should be equal to \'be\'; it\'s not')
        self.assertEqual(float(y.get('blabla', 'c')), 3.141592653, 'getint(blabla:c) should be equal to pi; it\'s not')
        self.assertTrue(bool(y.get('blabla', 'switch')), 'getbool(blabla:switch) should be True; it\'s not')

    def test_sections(self):
        self._create_values()
        self.assertListEqual(self.x.sections(), ['blabla', 'naka'], "sections() should return all sections, but it doesn't")

    def test_keys(self):
        self._create_values()
        self.assertListEqual(self.x.keys('blabla'), ['a', 'b', 'c', 'switch', 'tres'])

if __name__ == '__main__':
    unittest.main(verbosity=2)
