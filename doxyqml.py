#!/usr/bin/env python
import logging
import os
import sys
from optparse import OptionParser


from lexer import Lexer


def main():
    parser = OptionParser("usage: %prog [options] <path/to/File.qml>")
    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug", default=False,
                      help="Log debug info to stderr")
    (options, args) = parser.parse_args()
    name = args[0]

    lexer = Lexer(options)
    text = open(name).read()
    ok = lexer.tokenize(text)
    if not ok:
        return 1

    classname = os.path.basename(name).split(".")[0]

    for type_, value in lexer.tokens:
        print "#### %s ####" % type_
        print value
    return 0


if __name__ == "__main__":
    sys.exit(main())
# vi: ts=4 sw=4 et
