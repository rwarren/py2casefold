import os

MAP_FILE = "CaseFolding.txt"

_folding_map = {}

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
    map_path = os.path.join(os.path.dirname(__file__), MAP_FILE)
    with open(map_path, "r") as fp:
        for line in fp:
            if line.startswith("#") or (line.strip() == ""):
                continue
            code, status, mapping, name = line.split("; ")
            in_char = _get_unichr(code)
            # Python 3.5.0 casefold uses full case folding (C and F), so we
            # will too. See https://goo.gl/Tq4ko7.
            if status in "CF":
                out_chars = u"".join(_get_unichr(c) for c in mapping.split())
                _folding_map[in_char] = out_chars


def casefold(u):
    """Returns a casefolded version of u, which must be unicode.

    ValueError is raised if u is not a unicode instance. casefold is a unicode
    concept.
    
    """
    if not isinstance(u, unicode):
        raise ValueError("u must be unicode")
    return u"".join(_folding_map.get(c, c) for c in u)

# read/stash the folding map on import...
_read_unicode_data()
