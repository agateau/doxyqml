from collections import namedtuple
import re


COMMENT = "comment"
STRING = "string"
ELEMENT = "element"
BLOCK_START = "block_start"
BLOCK_END = "block_end"
CHAR = "char"
KEYWORD = "keyword"
IMPORT = "import"
PRAGMA = "pragma"


class LexerError(Exception):
    def __init__(self, msg, idx):
        Exception.__init__(self, msg)
        self.idx = idx


Token = namedtuple("Token", ["type", "value", "idx"])


class Tokenizer(object):
    def __init__(self, token_type, rx):
        self.token_type = token_type
        self.rx = rx

    def __call__(self, lexer, matched_str):
        lexer.append_token(self.token_type, matched_str)


class Lexer(object):
    def __init__(self, text):
        self.tokenizers = [
            Tokenizer(COMMENT, re.compile(r"/\*.*?\*/", re.DOTALL)),
            Tokenizer(COMMENT, re.compile(r"//.*")),
            # A double quote, then either:
            # - anything but a double quote or a backslash
            # - an escaped char (\n, \t...)
            # then a double quote
            Tokenizer(STRING, re.compile(r'("([^\\"]|(\\.))*")')),
            Tokenizer(BLOCK_START, re.compile("{")),
            Tokenizer(BLOCK_END, re.compile("}")),
            Tokenizer(IMPORT, re.compile(r"import\s+.*")),
            Tokenizer(PRAGMA, re.compile(r"pragma\s+\w.*")),
            Tokenizer(KEYWORD, re.compile(r"(default\s+property|property|readonly\s+property|signal)\s+")),
            Tokenizer(KEYWORD, re.compile(r"(function)\s+[^(]")),  # a named function
            Tokenizer(ELEMENT, re.compile(r"\w[\w.<>]*")),
            Tokenizer(CHAR, re.compile(".")),
            ]
        self.text = text.replace('\\\n', '\n')
        self.idx = 0
        self.tokens = []


    def tokenize(self):
        while True:
            self.advance()
            if self.idx == len(self.text):
                break
            self.apply_tokenizers()
        self.fixup_tokens()


    def advance(self):
        while self.idx < len(self.text):
            if self.text[self.idx].isspace():
                self.idx += 1
            else:
                break


    def apply_tokenizers(self):
        for tokenizer in self.tokenizers:
            match = tokenizer.rx.match(self.text, self.idx)

            if not match:
                continue

            if len(match.groups()) > 0:
                tokenizer(self, match.group(1))
                self.idx = match.end(1)
                return
            else:
                tokenizer(self, match.group(0))
                self.idx = match.end(0)
                return

        raise LexerError("No lexer matched", self.idx)

    def fixup_tokens(self):
        for i, t in enumerate(self.tokens):
            # Fix tokenization of a property named "property". For example:
            #   property string property: "foo"
            if (t.type == KEYWORD and t.value == "property" and i > 1 and
                    self.tokens[i - 1].type == ELEMENT and
                    self.tokens[i - 2].type == KEYWORD and self.tokens[i - 2].value.endswith("property")):
                self.tokens[i] = Token(ELEMENT, t.value, t.idx)

    def append_token(self, type, value):
        self.tokens.append(Token(type, value, self.idx))
