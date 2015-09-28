#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from py2casefold import casefold

class TestCasefold(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(casefold(u"tschüß"), u"tschüss")
        self.assertEqual(casefold(u"ΣίσυφοςﬁÆ"),
                         casefold(u"ΣΊΣΥΦΟσFIæ"))

    def test_str(self):
        self.assertRaises(ValueError, casefold, *("foo", )) 

if __name__ == "__main__":
    unittest.main()
