#!/usr/bin/env python

# Replaces Unicode characters in input XML file text content with
# ASCII approximations based on file with mappings between the two.

# This is a component in a pipeline to convert PMC NXML files into
# text and standoffs. The whole pipeline can be run as
#
#    python rewritetex.py FILE.xml -s | python rewriteu2a.py - -s | python respace.py - -s | python standoff.py - FILE.{txt,so}

from __future__ import with_statement

import sys
import os
import re
import codecs

from lxml import etree as ET

# The name of the file from which to read the replacement. Each line
# should contain the hex code for the unicode character, TAB, and
# the replacement string.

MAPPING_FILE_NAME = os.path.join(os.path.dirname(__file__), "data/entities.dat")

# XML tag to use to mark text content rewritten by this script.
REWRITTEN_TAG = "n2t-u2a"

# XML attribute to use for storing the original for rewritten text.
ORIG_TEXT_ATTRIBUTE = "orig-text"

# File into which to append unicode codepoints missing from the
# mapping, if any
MISSING_MAPPING_FILE_NAME = "missing-mappings.txt"

INPUT_ENCODING = "UTF-8"
OUTPUT_ENCODING = "UTF-8"


def read_mapping(f, fn="mapping data"):
    """
    Reads in mapping from Unicode to ASCII from the given input stream
    and returns a dictionary keyed by Unicode characters with the
    corresponding ASCII characters as values. The expected mapping
    format defines a single mapping per line, each with the format
    CODE\tASC where CODE is the Unicode code point as a hex number and
    ASC is the replacement ASCII string ("\t" is the literal tab
    character). Any lines beginning with "#" are skipped as comments.
    """

    # read in the replacement data
    linere = re.compile(r"^([0-9A-Za-z]{4,})\t(.*)$")
    mapping = {}

    for i, ll in enumerate(f):
        # ignore lines starting with "#" as comments
        if len(ll) != 0 and ll[0] == "#":
            continue

        m = linere.match(ll)
        assert m, "Format error in %s line %s: '%s'" % (fn, i + 1, ll.replace("\n", ""))
        c, r = m.groups()

        c = wide_unichr(int(c, 16))
        assert c not in mapping or mapping[c] == r, (
            "ERROR: conflicting mappings for %.4X: '%s' and '%s'"
            % (wide_ord(c), mapping[c], r)
        )

        # exception: literal '\n' maps to newline
        if r == "\\n":
            r = "\n"

        mapping[c] = r

    return mapping


def wide_ord(char):
    try:
        return ord(char)
    except TypeError:
        if (
            len(char) == 2
            and 0xD800 <= ord(char[0]) <= 0xDBFF
            and 0xDC00 <= ord(char[1]) <= 0xDFFF
        ):
            return (ord(char[0]) - 0xD800) * 0x400 + (ord(char[1]) - 0xDC00) + 0x10000
        else:
            raise


def wide_unichr(i):
    try:
        return chr(i)
    except ValueError:
        return (r"\U" + hex(i)[2:].zfill(8)).decode("unicode-escape")


def mapchar(c, mapping, missing_mappings, options=None):
    if c in mapping:
        return mapping[c]
    else:
        # make a note of anything unmapped
        missing_mappings.add("%.4X" % wide_ord(c))

        # remove missing by default, keep unicode or output codepoint
        # as hex as an option
        if options is None or (not options.hex and not options.keep_missing):
            return ""
        elif options.keep_missing:
            return c
        else:
            return "<%.4X>" % wide_ord(c)


def replace_mapped_text(e, mapping, missing, options=None):
    # TODO: inefficient, improve
    for i, c in enumerate(e.text):
        if wide_ord(c) >= 128:
            s = mapchar(c, mapping, missing, options)

            # if the character is unchanged, just skip
            if s == c:
                continue

            # create new element for the replacement
            r = ET.Element(REWRITTEN_TAG)
            r.attrib[ORIG_TEXT_ATTRIBUTE] = c
            r.text = s

            # ... make it the first child of the current element
            try:
                e.insert(0, r)
            except TypeError as typeErr:
                print("Type Error: {0}".format(typeErr))
                break

            # ... and split the text between the two
            r.tail = e.text[i + 1 :]
            e.text = e.text[:i]

            # terminate search; the rest of the text is now
            # in a different element
            break


def parent_index(e, parent):
    for i, c in enumerate(parent):
        if c == e:
            return i
    return None


def replace_mapped_tail(e, mapping, missing, parent, options=None):
    while True:
        replaced = False
        # TODO: inefficient, improve
        for i, c in enumerate(e.tail):
            # skip ASCII
            if wide_ord(c) < 128:
                continue

            s = mapchar(c, mapping, missing, options)

            # if the character is unchanged, just skip
            if s == c:
                continue

            # create new element for the replacement
            r = ET.Element(REWRITTEN_TAG)
            r.attrib[ORIG_TEXT_ATTRIBUTE] = c
            r.text = s

            # ... make it the next child of the parent after the
            # current
            pidx = parent_index(e, parent)
            parent.insert(pidx + 1, r)

            # ... and split the text between the two
            r.tail = e.tail[i + 1 :]
            e.tail = e.tail[:i]

            # process the rest in the new element, avoiding tail
            # recursion
            replaced = True
            e = r
            break

        if not replaced:
            break


def replace_mapped(e, mapping, missing, parent=None, options=None):
    # process text content
    if e.text is not None and e.text != "":
        replace_mapped_text(e, mapping, missing, options)

    # process children recursively
    for c in e:
        replace_mapped(c, mapping, missing, e, options)

    # process tail unless at root
    if parent is not None and e.tail is not None and e.tail != "":
        replace_mapped_tail(e, mapping, missing, parent, options)


def read_tree(filename):
    try:
        return ET.parse(filename)
    except ET.XMLSyntaxError:
        sys.stderr.write("Error parsing %s\n" % filename)
        raise


def write_tree(tree, fn, options=None):
    if options is not None and options.stdout:
        tree.write(sys.stdout, encoding=OUTPUT_ENCODING)
        return True

    if options is not None and options.directory is not None:
        output_dir = options.directory
    else:
        output_dir = ""

    output_fn = os.path.join(output_dir, os.path.basename(fn))

    # TODO: better protection against clobbering.
    # if output_fn == fn and not options.overwrite:
    #    print >> sys.stderr, 'rewriteu2a: skipping output for %s: file would overwrite input (consider -d and -o options)' % fn
    # else:
    # OK to write output_fn
    try:
        with open(output_fn, "w") as of:
            tree.write(of, encoding=OUTPUT_ENCODING)
    except IOError as ex:
        sys.stderr.write("rewriteu2a: failed write: %s\n" % ex)

    return True


def process_tree(tree, mapping=None, missing=None, options=None):
    if mapping is None:
        mapping = load_mapping()
    if missing is None:
        missing = set()

    root = tree.getroot()
    replace_mapped(root, mapping, missing, options=options)
    return tree


def process(fn, mapping, missing, options):
    tree = read_tree(fn)
    process_tree(tree)
    write_tree(tree, fn, options)


def argparser():
    import argparse

    ap = argparse.ArgumentParser(
        description="Rewrite Unicode text content with approximately equivalent ASCII in PMC NXML files."
    )
    ap.add_argument(
        "-d", "--directory", default=None, metavar="DIR", help="output directory"
    )
    ap.add_argument(
        "-o",
        "--overwrite",
        default=False,
        action="store_true",
        help="allow output to overwrite input files",
    )
    ap.add_argument(
        "-s", "--stdout", default=False, action="store_true", help="output to stdout"
    )
    ap.add_argument(
        "-x",
        "--hex",
        default=False,
        action="store_true",
        help="write hex sequence for missing mappings",
    )
    ap.add_argument(
        "-k",
        "--keep-missing",
        default=False,
        action="store_true",
        help="keep unicode for missing mappings",
    )
    ap.add_argument("file", nargs="+", help="input PubMed Central NXML file")
    return ap


def load_mapping(mapfn=MAPPING_FILE_NAME):
    if not os.path.exists(mapfn):
        # fall back to trying in script dir
        mapfn = os.path.join(
            os.path.dirname(__file__), os.path.basename(MAPPING_FILE_NAME)
        )
    try:
        with codecs.open(mapfn, encoding="utf-8") as f:
            return read_mapping(f, mapfn)
    except IOError as e:
        sys.stderr.write("Error reading mapping from %s: %s\n" % (MAPPING_FILE_NAME, e))
        raise


def write_missing(missing_mappings, filename=MISSING_MAPPING_FILE_NAME):
    # if there were any missing mappings and an output file name is
    # defined for these, try to append them in that file.
    if len(missing_mappings) > 0 and filename is not None:
        try:
            for mm in missing_mappings:
                sys.stderr.write("%s\t%s\n" % (filename, mm))
        except IOError as e:
            sys.stderr.write(
                "Warning: failed to write missing mappings to %s: %s\n" % (filename, e)
            )


def main(argv):
    options = argparser().parse_args(argv[1:])

    mapping = load_mapping()
    missing = set()

    for fn in options.file:
        process(fn, mapping, missing, options)

    write_missing(missing)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
