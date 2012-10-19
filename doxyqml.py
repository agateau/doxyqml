#!/usr/bin/env python
import logging
import os
import sys
from optparse import OptionParser

from qmlclass import QmlClass, fill_qml_class
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

    if options.debug:
        for type_, value in lexer.tokens:
            print "#### %s ####" % type_
            print value

    classname = os.path.basename(name).split(".")[0]
    qml_class = QmlClass(classname)

    try:
        fill_qml_class(qml_class, lexer.tokens)
    except:
        logging.error("Failed to parse %s" % name)
        raise

    print qml_class

    return 0


if __name__ == "__main__":
    sys.exit(main())
# vi: ts=4 sw=4 et
