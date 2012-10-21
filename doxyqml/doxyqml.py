#!/usr/bin/env python
import logging
import os
import sys
from optparse import OptionParser

import qmlparser
from lexer import Lexer
from qmlclass import QmlClass


def coord_for_idx(text, idx):
    head, sep, tail = text[:idx].rpartition("\n")
    if sep == "\n":
        row = head.count("\n") + 2
    else:
        row = 1
    col = len(tail) + 1
    return row, col


def line_for_idx(text, idx):
    bol = text.rfind("\n", 0, idx)
    if bol == -1:
        bol = 0
    eol = text.find("\n", idx)
    return text[bol:eol]


def info_for_error_at(text, idx):
    row, col = coord_for_idx(text, idx)
    line = line_for_idx(text, idx)
    msg = line + "\n" + "-" * (col - 1) + "^"
    return row, msg


def parse_cmdline():
    parser = OptionParser("usage: %prog [options] <path/to/File.qml>")
    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug", default=False,
                      help="Log debug info to stderr")
    return parser.parse_args()


def main():
    options, args = parse_cmdline()
    name = args[0]

    text = open(name).read()

    lexer = Lexer(text)
    try:
        lexer.tokenize()
    except LexerError, exc:
        logging.error("Failed to tokenize %s" % name)
        row, msg = info_for_error_at(text, exc.idx)
        logging.error("Lexer error line %d: %s\n%s", row, exc, msg)
        if options.debug:
            raise
        else:
            return -1

    if options.debug:
        for token in lexer.tokens:
            print "## type=%s ####" % token.type
            print token.value

    classname = os.path.basename(name).split(".")[0]
    qml_class = QmlClass(classname)

    try:
        qmlparser.parse(lexer.tokens, qml_class)
    except qmlparser.QmlParserError, exc:
        logging.error("Failed to parse %s" % name)
        row, msg = info_for_error_at(text, exc.token.idx)
        logging.error("Lexer error line %d: %s\n%s", row, exc, msg)
        if options.debug:
            raise
        else:
            return -1

    print qml_class

    return 0


if __name__ == "__main__":
    sys.exit(main())
# vi: ts=4 sw=4 et
