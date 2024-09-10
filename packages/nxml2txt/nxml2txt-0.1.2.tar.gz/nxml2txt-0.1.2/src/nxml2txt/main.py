#!/usr/bin/env python

# Convert NLM .nxml to text and standoff annotations

import os
import sys

from collections import namedtuple
from lxml import etree as ET

import rewriteu2a
import respace
import rewritetex
import standoff
import rewritemmla

usage = "%s NXMLFILE [TEXTFILE] [SOFILE]" % __file__

TexOptions = namedtuple("TexOptions", "verbose")
U2aOptions = namedtuple("U2aOptions", "hex keep_missing stdout directory overwrite")

def nxml2txt(nxmlfn, tex_options=None, u2a_options=None):
    tree = ET.parse(nxmlfn)

    # process embedded TeX math
    if tex_options is None:
        tex_options = TexOptions(verbose=True)
    rewritetex.process_tree(tree, options=tex_options)

    # process MathML annotations
    rewritemmla.process_tree(tree)

    # normalize whitespace
    respace.process_tree(tree)

    # map unicode to ASCII
    if u2a_options is None:
        u2a_options = U2aOptions(
            keep_missing=True, hex=False, stdout=False, directory=None, overwrite=False
        )
    rewriteu2a.process_tree(tree, options=u2a_options)

    # convert to text and standoffs
    text, standoffs = standoff.convert_tree(tree)

    return text, standoffs


def write_text(text, nxmlfn, argv=None):
    if argv is not None and len(argv) > 2:
        textfn = argv[2]
    else:
        textfn = nxmlfn.replace(".nxml", "") + ".txt"
    standoff.write_text(text, textfn)


def write_standoffs(standoffs, nxmlfn, argv=None):
    if argv is not None and len(argv) > 3:
        sofn = argv[3]
    else:
        sofn = nxmlfn.replace(".nxml", "") + ".so"
    standoff.write_standoffs(standoffs, sofn)


def main(argv):
    if len(argv) < 2 or len(argv) > 4:
        sys.stderr.write("Usage: %s\n" % usage)
        return 1
    nxmlfn = argv[1]

    if os.path.exists(nxmlfn[:-5] + ".txt"):
        return 0

    text, standoffs = nxml2txt(nxmlfn)

    write_text(text, nxmlfn, argv)
    write_standoffs(standoffs, nxmlfn, argv)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
