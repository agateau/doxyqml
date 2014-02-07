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


class LexerError(Exception):
    def __init__(self, msg, idx):
        Exception.__init__(self, msg)
        self.idx = idx


Token = namedtuple("Token", ["type", "value", "idx"])


TokenizerResult = namedtuple("TokenizerResult", ["token", "idx"])


class Tokenizer(object):
    """Helper class to extract tokens, based on regular expression

    If the regular expression defines a match group named 'value', then the
    content of this group is used as the token value. If no 'value' group is
    defined, the whole match is the token value.
    """
    def __init__(self, token_type, rx):
        self.type = token_type
        self.rx = rx
        self.groupindex = self.rx.groupindex.get("value", 0)

    def match(self, text, idx):
        """Try to match `text` at position `idx`

        Returns a TokenizerResult on success, None otherwise
        """
        match = self.rx.match(text, idx)
        if match:
            token = Token(self.type, match.group(self.groupindex), idx)
            return TokenizerResult(token, match.end(self.groupindex))
        else:
            return None


class Lexer(object):
    def __init__(self, text):
        self.tokenizers = [
            Tokenizer(COMMENT, re.compile(r"/\*.*?\*/", re.DOTALL)),
            Tokenizer(COMMENT, re.compile(r"//.*$", re.MULTILINE)),
            Tokenizer(STRING, re.compile(r'"([^\\"]|(\\.))*"')),
            Tokenizer(BLOCK_START, re.compile("{")),
            Tokenizer(BLOCK_END, re.compile("}")),
            Tokenizer(IMPORT, re.compile("^import .*$", re.MULTILINE)),
            Tokenizer(KEYWORD, re.compile("(?P<value>default\s+property|property|readonly\s+property|signal)\s+")),
            Tokenizer(KEYWORD, re.compile("(?P<value>function)\s+[^(]")),  # a named function
            Tokenizer(ELEMENT, re.compile(r"\w[\w.<>]*")),
            Tokenizer(CHAR, re.compile(".")),
            ]
        self.text = text
        self.idx = 0
        self.tokens = []


    def tokenize(self):
        while True:
            self.advance()
            if self.idx == len(self.text):
                break
            self.apply_tokenizers()


    def advance(self):
        while self.idx < len(self.text):
            if self.text[self.idx].isspace():
                self.idx += 1
            else:
                break


    def apply_tokenizers(self):
        for tokenizer in self.tokenizers:
            result = tokenizer.match(self.text, self.idx)
            if result:
                self.tokens.append(result.token)
                self.idx = result.idx
                return

        raise LexerError("No lexer matched", self.idx)
