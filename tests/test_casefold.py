#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from py2casefold import casefold

class TestCasefold(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(casefold(u"tschüß"), u"tschüss")
        self.assertEqual(casefold(u"ΣίσυφοςﬁÆ"),
                         casefold(u"ΣΊΣΥΦΟσFIæ"))
        self.assertEqual(casefold(u"ﬃ"), u"ffi")
    
    def test_empty_string(self):
        self.assertEqual(casefold(u""), u"")
    
    def test_ascii_only(self):
        self.assertEqual(casefold(u"aA"), u"aa")
        self.assertEqual(casefold(u"fOo Bar"), u"foo bar")
    
    def test_unsupported(self):
        # This makes sure that full case folding (C+F) is done, not
        # simple or special case folding.
        
        # First some Turkish fun...
        # 0x130 folds to:
        #    0x0069 + 0x0307 with full case folding (F)
        #    0x0069 ("i") alone with the Turkish special case (T)
        # We expect full case folding...
        self.assertEqual(casefold(u"\u0130"), u"i\u0307")
        
        # Now explicitly check a full vs simple fold...
        # 0x1F9B folds to:
        #    0x1F23 + 0x03B9 with full case folding (F)
        #    0x1F93 alone with simple case folding (S)
        self.assertEqual(casefold(u"\u1F9B"), u"\u1F23\u03B9")

    def test_str(self):
        self.assertRaises(ValueError, casefold, *("foo", )) 

if __name__ == "__main__":
    unittest.main()
