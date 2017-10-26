#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import sys
import unittest

import py2casefold

casefold = py2casefold.casefold # space saver

class TestCasefold(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(casefold("tschüß"), "tschüss")
        self.assertEqual(casefold("ΣίσυφοςﬁÆ"),
                         casefold("ΣΊΣΥΦΟσFIæ"))
        self.assertEqual(casefold("ﬃ"), "ffi")
    
    def test_empty_string(self):
        self.assertEqual(casefold(""), "")
    
    def test_ascii_only(self):
        self.assertEqual(casefold("aA"), "aa")
        self.assertEqual(casefold("fOo Bar"), "foo bar")
    
    def test_unsupported(self):
        # This makes sure that full case folding (C+F) is done, not
        # simple or special case folding.
        
        # First some Turkish fun...
        # 0x130 folds to:
        #    0x0069 + 0x0307 with full case folding (F)
        #    0x0069 ("i") alone with the Turkish special case (T)
        # We expect full case folding...
        self.assertEqual(casefold("\u0130"), "i\u0307")
        
        # Now explicitly check a full vs simple fold...
        # 0x1F9B folds to:
        #    0x1F23 + 0x03B9 with full case folding (F)
        #    0x1F93 alone with simple case folding (S)
        self.assertEqual(casefold("\u1F9B"), "\u1F23\u03B9")

    def test_str(self):
        if sys.version_info.major >= 3:
            # always unicode!
            return
        else:
            self.assertRaises(ValueError, casefold, *(str("foo"), ))

    def test_unicode_info(self):
        self.assertEqual("10.0.0", py2casefold.UNICODE_VERSION)
        self.assert_(os.path.exists(py2casefold.UNICODE_MAP_FILE))

if __name__ == "__main__":
    unittest.main()
