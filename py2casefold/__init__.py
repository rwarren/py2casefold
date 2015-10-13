from __future__ import unicode_literals
import sys
import os

PY3 = sys.version_info.major >= 3

try:
    _unichr = unichr
except NameError:
    _unichr = chr

try:
    _unicode_str = unicode
except NameError:
    _unicode_str = str

MAP_FILE = "CaseFolding.txt"

_folding_map = {}

def _get_unichr(s):
    """Returns the unicode char matching the provided hex string index (s)."""
    try:
        # go for the fastest method first...
        return _unichr(int(s, 16))
    except ValueError: # wide char!
        # The case folding data contains some wide chars that unichr does not
        # support when python is not compiled with wide character support (very
        # common). The unicode-escape format can help here.
        return ("\\U" + s.zfill(8)).decode("unicode-escape")


def _read_unicode_data():
    global _folding_map
    map_path = os.path.join(os.path.dirname(__file__), MAP_FILE)
    
    # Open the official CaseFolding.txt file to read the folding map...
    #  - Codecs.open would be nice, but I'm trying to limit imports here
    #  - Although I can't find a reference for what encoding the Unicode
    #     consortium uses (!!) in their text files, UTF8 is a reasonable guess
    #     which works for the CaseFolding.txt file (where the only non-ascii
    #     char is in the comments, anyway)
    if PY3:
        fp = open(map_path, "r", encoding = "utf-8")
    else:
        fp = open(map_path, "r")
    
    with open(map_path, "r") as fp:
        for line in fp:
            if not PY3:
                line = line.decode("utf-8")
            if line.startswith("#") or (line.strip() == ""):
                continue
            code, status, mapping, name = line.split("; ")
            in_char = _get_unichr(code)
            # Python 3.5.0 casefold uses full case folding (C and F), so we
            # will too. See https://goo.gl/Tq4ko7.
            if status in "CF":
                out_chars = "".join(_get_unichr(c) for c in mapping.split())
                _folding_map[in_char] = out_chars


def casefold(u):
    """Returns a casefolded version of u, which must be unicode.

    ValueError is raised if u is not a unicode instance. casefold is a unicode
    concept.
    
    """
    if not isinstance(u, _unicode_str):
        raise ValueError("u must be unicode")
    return "".join(_folding_map.get(c, c) for c in u)

# read/stash the folding map on import...
_read_unicode_data()
