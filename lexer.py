import re


COMMENT = "comment"
STRING = "string"
ELEMENT = "element"
BLOCK_START = "block_start"
BLOCK_END = "block_end"
CHAR = "char"
KEYWORD = "keyword"


class LexerError(Exception):
    pass


class Tokenizer(object):
    def __init__(self, token_type, rx):
        self.token_type = token_type
        self.rx = rx

    def __call__(self, lexer, match):
        lexer.append_token(self.token_type, match.group(0))


class Lexer(object):
    def __init__(self, options):
        self.tokenizers = [
            Tokenizer(COMMENT, re.compile(r"/\*.*?\*/", re.DOTALL)),
            Tokenizer(COMMENT, re.compile(r"//.*$", re.MULTILINE)),
            Tokenizer(STRING, re.compile(r'("([^\\"]|(\\.))*")')),
            Tokenizer(BLOCK_START, re.compile("{")),
            Tokenizer(BLOCK_END, re.compile("}")),
            Tokenizer(KEYWORD, re.compile("(property|function|signal)")),
            Tokenizer(ELEMENT, re.compile("\w+")),
            Tokenizer(CHAR, re.compile(".")),
            ]
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


    def tokenize(self, text):
        self.text = text
        while True:
            self.advance()
            if self.idx == len(self.text):
                break
            try:
                self.apply_tokenizers()
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


    def apply_tokenizers(self):
        for tokenizer in self.tokenizers:
            match = tokenizer.rx.match(self.text, self.idx)
            if match:
                tokenizer(self, match)
                self.idx = match.end(0)
                return
        raise LexerError("No lexer matched")


    def append_token(self, _type, value):
        self.tokens.append((_type, value))
