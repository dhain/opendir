import os
import sys
import errno
import shutil
import unittest
import pyximport; pyximport.install()

import opendir


TEST_DIR = os.path.join(os.getenv('TEMP', '/tmp'), 'test_opendir')


class TestOpendir(unittest.TestCase):
    def setUp(self):
        self.path = os.path.join(TEST_DIR, u'\u2603')
        self.str_path = self.path.encode(sys.getfilesystemencoding() or
                                         sys.getdefaultencoding())
        self.contents = set(u'\u2603-%d' % (i,) for i in xrange(3))
        self.str_contents = set(name.encode(sys.getfilesystemencoding() or
                                            sys.getdefaultencoding())
                                for name in self.contents)
        try:
            shutil.rmtree(TEST_DIR)
        except OSError, err:
            if err.errno != errno.ENOENT:
                raise
        for name in self.contents:
            os.makedirs(os.path.join(self.path, name))

    def test_read(self):
        d = opendir.opendir(self.str_path)
        for _ in xrange(len(self.str_contents)):
            self.assertTrue(d.read() in self.str_contents)
        self.assertTrue(d.read() is None)
        self.assertTrue(d.read() is None)

    def test_iter(self):
        d = opendir.opendir(self.str_path)
        self.assertEqual(set(iter(d)), self.str_contents)

    def test_closing_again(self):
        d = opendir.opendir(self.str_path)
        d.close()
        d.close()

    def test_nonexistent_dir(self):
        self.assertRaises(
            OSError,
            opendir.opendir,
            os.path.join(self.str_path, 'bogus_dir')
        )

    def test_rewind(self):
        d = opendir.opendir(self.str_path)
        self.assertEqual(set(iter(d)), self.str_contents)
        d.rewind()
        self.assertEqual(set(iter(d)), self.str_contents)

    def test_tell_seek(self):
        d = opendir.opendir(self.str_path)
        it = iter(d)
        pos = d.tell()
        name = it.next()
        d.seek(pos)
        self.assertEqual(d.tell(), pos)
        self.assertEqual(it.next(), name)

    def test_unicode(self):
        d = opendir.opendir(self.path)
        seen = set()
        for name in d:
            self.assertTrue(isinstance(name, unicode))
            seen.add(name)
        self.assertEqual(seen, self.contents)

    def test_unicode_non_decodable(self):
        d = opendir.opendir(self.path)
        real_getfilesystemencoding = opendir.sys.getfilesystemencoding
        opendir.sys.getfilesystemencoding = lambda: 'ascii'
        try:
            self.assertEqual(set(d), self.str_contents)
        finally:
            opendir.sys.getfilesystemencoding = real_getfilesystemencoding


if __name__ == "__main__":
    unittest.main()
