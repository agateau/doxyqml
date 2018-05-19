#!/usr/bin/env python3

import argparse
import logging
import os
import re
import sys

from . import qmlparser
from .lexer import Lexer, LexerError
from .qmlclass import QmlClass


VERSION = "0.4.0"
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


def parse_args(argv):
    parser = argparse.ArgumentParser(
        prog="doxyqml",
        description=DESCRIPTION,
        )
    parser.add_argument("-d", "--debug",
                        action="store_true",
                        help="Log debug info to stderr")
    parser.add_argument("--namespace",
                        action='append',
                        default=[],
                        help="Wrap the generated C++ classes in NAMESPACE")
    parser.add_argument('--version',
                        action='version',
                        version='%%(prog)s %s' % VERSION)
    parser.add_argument("qml_file",
                        help="The QML file to parse")

    return parser.parse_args(argv)

def find_qmldir_file(qml_file):
    dir = os.path.dirname(qml_file)

    while True:
        # Check if `dir` contains a file of the name "qmldir".
        name = os.path.join(dir, 'qmldir')

        if os.path.isfile(name):
            return name

        # Pick parent of `dir`. Abort once parent stops changing,
        # either because we reached the root directory, or because
        # relative paths were used and we reached the currrent
        # working directory.
        parent = os.path.dirname(dir)

        if parent == dir:
            return None

        dir = parent


def find_classname(qml_file, namespace=None):
    classname = os.path.basename(qml_file).split(".")[0]
    classversion = None
    modulename = ''

    qmldir = find_qmldir_file(qml_file)

    if qmldir:
        text = open(qmldir).read()
        match = re.match(r'^module\s+((?:\w|\.)+)\s*$', text, re.MULTILINE)

        if match:
            modulename = match.group(1)

        basedir = os.path.dirname(qmldir)

        rx_object_type = re.compile(r'^(\w+)\s+(\d+(?:\.\d+)*)\s+(\S+)\s*$', re.MULTILINE)

        for name, version, path in rx_object_type.findall(text):
            filename = os.path.join(basedir, path)

            if os.path.isfile(filename) and os.path.samefile(qml_file, filename):
                classversion = version
                classname = name
                break

    if modulename:
        classname = modulename + '.' + classname

    if namespace:
        classname = '.'.join(namespace) + '.' + classname

    return classname, classversion

def main(argv=None, out=None):
    if argv is None:
        argv = sys.argv[1:]
    if out is None:
        out == sys.stdout

    args = parse_args(argv)

    name = args.qml_file
    namespace = args.namespace
    text = open(name, encoding="utf-8").read()

    lexer = Lexer(text)
    try:
        lexer.tokenize()
    except LexerError as exc:
        logging.error("Failed to tokenize %s" % name)
        row, msg = info_for_error_at(text, exc.idx)
        logging.error("Lexer error line %d: %s\n%s", row, exc, msg)
        if args.debug:
            raise
        else:
            return -1

    if args.debug:
        for token in lexer.tokens:
            print("%20s %s" % (token.type, token.value))

    classname, classversion = find_classname(name, namespace)
    qml_class = QmlClass(classname, classversion)

    try:
        qmlparser.parse(lexer.tokens, qml_class)
    except qmlparser.QmlParserError as exc:
        logging.error("Failed to parse %s" % name)
        row, msg = info_for_error_at(text, exc.token.idx)
        logging.error("Lexer error line %d: %s\n%s", row, exc, msg)
        if args.debug:
            raise
        else:
            return -1

    print(qml_class, file=out)

    return 0


if __name__ == "__main__":
    sys.exit(main())
# vi: ts=4 sw=4 et
