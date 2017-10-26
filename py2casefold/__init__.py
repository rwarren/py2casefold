from __future__ import unicode_literals
import os
import sys

_this_dir = os.path.abspath(os.path.dirname(__file__))
UNICODE_MAP_FILE = os.path.join(_this_dir, "CaseFolding.txt")
UNICODE_VERSION = "<not loaded>"

_folding_map = {}
_PY3 = sys.version_info.major >= 3

if _PY3:
    unichr = chr
    unicode = str


def set_unicode_version(first_line):
    global UNICODE_VERSION
    UNICODE_VERSION = first_line[first_line.find("-") + 1
                                 :first_line.find(".txt")]

def _get_unichr(s):
    """Returns the unicode char matching the provided hex string index (s)."""
    try:
        # go for the fastest method first...
        return unichr(int(s, 16))
    except ValueError: # wide char!
        # The case folding data contains some wide chars that unichr does not
        # support when python is not compiled with wide character support (very
        # common). The unicode-escape format can help here.
        return ("\\U" + s.zfill(8)).decode("unicode-escape")


def _read_unicode_data():
    global _folding_map

    # Open the official CaseFolding.txt file to read the folding map...
    #  - Codecs.open would be nice, but I'm trying to limit imports here
    #  - Although I can't find a reference for what encoding the Unicode
    #     consortium uses (!!) in their text files, UTF8 is a reasonable guess
    #     which works for the CaseFolding.txt file (where the only non-ascii
    #     char is in the comments, anyway)
    if _PY3:
        fp = open(UNICODE_MAP_FILE, "r", encoding = "utf-8")
    else:
        fp = open(UNICODE_MAP_FILE, "r")
    lines = fp.readlines()
    fp.close()
    # The Unicode version is on the first line of the file.
    set_unicode_version(lines[0])

    for line in lines:
        if not _PY3:
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
    if not isinstance(u, unicode):
        raise ValueError("The 'u' parameter must be unicode")
    return "".join(_folding_map.get(c, c) for c in u)

# read/stash the folding map on import...
_read_unicode_data()
