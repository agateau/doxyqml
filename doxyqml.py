#!/usr/bin/env python
import os
import re
import sys
from optparse import OptionParser

CLASS_START_RX = re.compile("([a-zA-Z]+) {")
PROPERTY_SET_RX = re.compile("([\w.]+):")
PROPERTY_DEF_RX = re.compile("property (\w+) +(\w+) *(:.*)?")
SIGNAL_DEF_RX = re.compile("signal (\w+)( *\((?P<args>.*)\))?")
FCN_DEF_RX = re.compile("function (\w+) *\((?P<args>.*)\)")


class HeaderParser(object):
    def __init__(self, classname):
        self.classname = classname

    def __call__(self, line):
        if line.startswith("/*"):
            print line
            self.app.push_parser(CommentParser())
            return

        match = CLASS_START_RX.match(line)
        if match is None:
            return

        print "class %s : public %s {" % (self.classname, match.group(1))
        print "public:"

        self.app.push_parser(ClassParser())


class ClassParser(object):
    def __init__(self):
        self.signal_section = False

    def __call__(self, line):
        if line.startswith("/*"):
            print line
            self.app.push_parser(CommentParser())
            return

        if line.startswith("{"):
            self.app.push_parser(SkipBlockParser())
            return

        if PROPERTY_SET_RX.match(line):
            if line[-1] == "{":
                self.app.push_parser(SkipBlockParser())
            return

        match = PROPERTY_DEF_RX.match(line)
        if match is not None:
            print "Q_PROPERTY(%s %s)" % (match.group(1), match.group(2))
            value = match.group(3)
            if value is not None:
                if value.count("{") > value.count("}"):
                    self.app.push_parser(SkipBlockParser())
            return

        match = SIGNAL_DEF_RX.match(line)
        if match is not None:
            name = match.group(1)
            if match.group("args"):
                args = match.group("args")
            else:
                args = ""
            if not self.signal_section:
                print "Q_SIGNALS:"
                self.signal_section = True
            print "void %s(%s);" % (name, args)
            return

        match = FCN_DEF_RX.match(line)
        if match is not None:
            name = match.group(1)
            args = match.group("args")
            if self.signal_section:
                print "public:"
                self.signal_section = False
            print "void %s(%s);" % (name, args)
            if line.endswith("{"):
                self.app.push_parser(SkipBlockParser())
            return

        # Start of a block
        if len(line) > 0 and line[-1] == "{":
            self.app.push_parser(SkipBlockParser())

        print line


class CommentParser(object):
    def __call__(self, line):
        print line
        if line.endswith("*/"):
            self.app.pop_parser()


class SkipBlockParser(object):
    def __init__(self):
        self.count = 1

    def __call__(self, line):
        self.count += line.count("{")
        self.count -= line.count("}")
        if self.count == 0:
            self.app.pop_parser()


class App(object):
    def __init__(self, options):
        self.options = options
        self.parsers = []

    def parse(self, name):
        classname = os.path.basename(name).split(".")[0]
        self.push_parser(HeaderParser(classname))

        for num, line in enumerate(open(name).readlines()):
            parser = self.parsers[-1]
            if self.options.debug:
                parser_name = parser.__class__.__name__
                print >>sys.stderr, "%20s:%4d %s" % (parser_name, num, line.rstrip())
            parser(line.strip())
        print ";"

    def push_parser(self, parser):
        parser.app = self
        self.parsers.append(parser)

    def pop_parser(self):
        self.parsers.pop()


def main():
    parser = OptionParser("usage: %prog [options] <path/to/File.qml>")
    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug", default=False,
                      help="Log debug info to stderr")
    (options, args) = parser.parse_args()
    name = args[0]

    app = App(options)
    app.parse(name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
# vi: ts=4 sw=4 et
