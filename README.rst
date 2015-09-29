``py2casefold``
===============

Python 3 has ``str.casefold()``.  Python 2 doesn't.  ``py2casefold``
brings casefolding support to Python 2.

Installation
============

``pip install py2casefold``

Usage
=====

    >>> from py2casefold import casefold
    >>> print casefold(u"tschüß")
    tschüss
    >>> casefold(u"ΣίσυφοςﬁÆ") == casefold(u"ΣΊΣΥΦΟσFIæ") == u"σίσυφοσfiæ"
    True

Note that ``casefold`` does *not* normalize the string.  Casefolding and
normalization are different operations.  For more info see
http://www.w3.org/International/wiki/Case_folding, and
http://www.w3.org/TR/charmod-norm/.

If you are looking for string similarity you will also probably want to
consider one of the unicode normalization options (NFC, NFKC, NFD, NFKD)
that are available with python's built in ``unicodedata.normalize()``.

Speed
=====

At the moment, this pure python ``casefold`` implementation is
significantly (> 20X) slower than the optimized py3 C implementation.
This can be improved later, but it is currently more than sufficient
for basic case folding.  As a rough estimate, case folding 100
characters clocks in at ~ 25us on an old developer laptop.

License
=======
BSD and the Unicode license agreement.  This module includes data from
the Unicode consortium which should include the appropriate notice (see
http://unicode.org/copyright.html).

See ``LICENSE`` file for details.
