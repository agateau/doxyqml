#!/usr/bin/env python
import argparse
import logging
import os
import sys

import qmlparser
from lexer import Lexer, LexerError
from qmlclass import QmlClass


VERSION = "0.2.0"
DESCRIPTION = "Doxygen input filter for QML files"


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


def parse_args():
    parser = argparse.ArgumentParser(
        version=VERSION,
        description=DESCRIPTION,
        )
    parser.add_argument("-d", "--debug",
                      action="store_true",
                      help="Log debug info to stderr")
    parser.add_argument("qml_file",
                        help="The QML file to parse")
    return parser.parse_args()


def main():
    args = parse_args()

    name = args.qml_file
    text = open(name).read()

    lexer = Lexer(text)
    try:
        lexer.tokenize()
    except LexerError, exc:
        logging.error("Failed to tokenize %s" % name)
        row, msg = info_for_error_at(text, exc.idx)
        logging.error("Lexer error line %d: %s\n%s", row, exc, msg)
        if args.debug:
            raise
        else:
            return -1

    if args.debug:
        for token in lexer.tokens:
            print "%20s %s" % (token.type, token.value)

    classname = os.path.basename(name).split(".")[0]
    qml_class = QmlClass(classname)

    try:
        qmlparser.parse(lexer.tokens, qml_class)
    except qmlparser.QmlParserError, exc:
        logging.error("Failed to parse %s" % name)
        row, msg = info_for_error_at(text, exc.token.idx)
        logging.error("Lexer error line %d: %s\n%s", row, exc, msg)
        if args.debug:
            raise
        else:
            return -1

    print qml_class

    return 0


if __name__ == "__main__":
    sys.exit(main())
# vi: ts=4 sw=4 et
