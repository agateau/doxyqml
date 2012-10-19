#!/usr/bin/env python
import logging
import os
import re
import sys
from optparse import OptionParser


class TokenizerError(Exception):
    pass


COMMENT = "comment"
STRING = "string"
ELEMENT = "element"
BLOCK_START = "block_start"
BLOCK_END = "block_end"
CHAR = "char"


class MultiLineCommentTokenizer(object):
    rx = re.compile(r'/\*.*?\*/', re.DOTALL)

    def __call__(self, tokenizer, match):
        tokenizer.append_token(COMMENT, match.group(0))


class CommentTokenizer(object):
    rx = re.compile(r'//.*$', re.MULTILINE)

    def __call__(self, tokenizer, match):
        tokenizer.append_token(COMMENT, match.group(0))


class StringTokenizer(object):
    rx = re.compile(r'("([^\\"]|(\\.))*")')

    def __call__(self, tokenizer, match):
        tokenizer.append_token(STRING, match.group(0))


class BlockTokenizer(object):
    rx = re.compile(r'[{}]')

    def __call__(self, tokenizer, match):
        value = match.group(0)
        _type = value == "{" and BLOCK_START or BLOCK_END
        tokenizer.append_token(_type, value)


class CharTokenizer(object):
    rx = re.compile(r'.')

    def __call__(self, tokenizer, match):
        tokenizer.append_token(CHAR, match.group(0))


class ElementTokenizer(object):
    rx = re.compile("[\w]+")

    def __call__(self, tokenizer, match):
        tokenizer.append_token(ELEMENT, match.group(0))


class Tokenizer(object):
    def __init__(self, options):
        self.options = options
        self.text = ""
        self.idx = 0
        self.classname = ""
        self.tokens = []

    def coord_for_idx(self):
        head, sep, tail = self.text[:self.idx].rpartition("\n")
        if sep == "\n":
            row = head.count("\n") + 2
        else:
            row = 1
        col = len(tail) + 1
        return row, col

    def start(self, name):
        self.classname = os.path.basename(name).split(".")[0]

        self.text = open(name).read()
        while True:
            self.advance()
            if self.idx == len(self.text):
                break
            try:
                self.apply_tokenizers([MultiLineCommentTokenizer(), CommentTokenizer(), StringTokenizer(), BlockTokenizer(), ElementTokenizer(), CharTokenizer()])

            except TokenizerError, exc:
                row, col = self.coord_for_idx()
                bol = self.text.rfind("\n", 0, self.idx)
                if bol == -1:
                    bol = 0
                eol = self.text.find("\n", self.idx)
                msg = self.text[bol:eol] + "\n" + "-" * (col - 1) + "^"
                logging.error("Tokenizer error line %d: %s\n%s", row, exc, msg)
                return False
        return True


    def advance(self):
        while self.idx < len(self.text):
            if self.text[self.idx].isspace():
                self.idx += 1
            else:
                break


    def apply_tokenizers(self, lst):
        for tokenizer in lst:
            match = tokenizer.rx.match(self.text, self.idx)
            if match:
                tokenizer(self, match)
                self.idx = match.end(0)
                return
        raise TokenizerError("No tokenizer matched")


    def append_token(self, _type, value):
        self.tokens.append((_type, value))


def main():
    parser = OptionParser("usage: %prog [options] <path/to/File.qml>")
    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug", default=False,
                      help="Log debug info to stderr")
    (options, args) = parser.parse_args()
    name = args[0]

    tokenizer = Tokenizer(options)
    ok = tokenizer.start(name)
    if not ok:
        return 1

    for type_, value in tokenizer.tokens:
        print "#### %s ####" % type_
        print value
    return 0


if __name__ == "__main__":
    sys.exit(main())
# vi: ts=4 sw=4 et
