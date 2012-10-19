#!/usr/bin/env python
import logging
import os
import re
import sys
from optparse import OptionParser


class LexerError(Exception):
    pass


COMMENT = "comment"
STRING = "string"
ELEMENT = "element"
BLOCK_START = "block_start"
BLOCK_END = "block_end"
CHAR = "char"
KEYWORD = "keyword"


class Tokenizer(object):
    def __init__(self, token_type, rx):
        self.token_type = token_type
        self.rx = rx

    def __call__(self, lexer, match):
        lexer.append_token(self.token_type, match.group(0))


class Lexer(object):
    def __init__(self, options):
        self.options = options
        self.text = ""
        self.idx = 0
        self.tokens = []

    def coord_for_idx(self):
        head, sep, tail = self.text[:self.idx].rpartition("\n")
        if sep == "\n":
            row = head.count("\n") + 2
        else:
            row = 1
        col = len(tail) + 1
        return row, col

    def tokenize(self, name):
        self.text = open(name).read()
        while True:
            self.advance()
            if self.idx == len(self.text):
                break
            try:
                self.apply_tokenizers([
                    Tokenizer(COMMENT, re.compile(r"/\*.*?\*/", re.DOTALL)),
                    Tokenizer(COMMENT, re.compile(r"//.*$", re.MULTILINE)),
                    Tokenizer(STRING, re.compile(r'("([^\\"]|(\\.))*")')),
                    Tokenizer(BLOCK_START, re.compile("{")),
                    Tokenizer(BLOCK_END, re.compile("}")),
                    Tokenizer(KEYWORD, re.compile("(property|function|signal)")),
                    Tokenizer(ELEMENT, re.compile("\w+")),
                    Tokenizer(CHAR, re.compile(".")),
                    ])

            except LexerError, exc:
                row, col = self.coord_for_idx()
                bol = self.text.rfind("\n", 0, self.idx)
                if bol == -1:
                    bol = 0
                eol = self.text.find("\n", self.idx)
                msg = self.text[bol:eol] + "\n" + "-" * (col - 1) + "^"
                logging.error("Lexer error line %d: %s\n%s", row, exc, msg)
                return False
        return True


    def advance(self):
        while self.idx < len(self.text):
            if self.text[self.idx].isspace():
                self.idx += 1
            else:
                break


    def apply_tokenizers(self, lst):
        for lexer in lst:
            match = lexer.rx.match(self.text, self.idx)
            if match:
                lexer(self, match)
                self.idx = match.end(0)
                return
        raise LexerError("No lexer matched")


    def append_token(self, _type, value):
        self.tokens.append((_type, value))


def main():
    parser = OptionParser("usage: %prog [options] <path/to/File.qml>")
    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug", default=False,
                      help="Log debug info to stderr")
    (options, args) = parser.parse_args()
    name = args[0]

    lexer = Lexer(options)
    ok = lexer.tokenize(name)
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
