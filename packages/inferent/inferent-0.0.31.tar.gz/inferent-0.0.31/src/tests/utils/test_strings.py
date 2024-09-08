import unittest

from inferent.utils import ct

class TestStringMethods(unittest.TestCase):

    def test_ct(self):
        ### edge cases
        self.assertEqual(ct(None), "")
        self.assertEqual(ct(""), "")

        ### encoding
        self.assertEqual(ct("foo\xfc"), "foo")  # Non UTF8 
        self.assertEqual(ct("foo\u0627"), "foo")  # UTF8, non-ascii
        self.assertEqual(ct("f$oo, bar"), "foo bar")  # punctuation
        self.assertEqual(ct("FOO BAR"), "foo bar")  # lowercase
        self.assertEqual(ct("  foo  bar   "), "foo  bar")  # strip

if __name__ == '__main__':
    unittest.main()
