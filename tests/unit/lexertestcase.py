from unittest import TestCase

from doxyqml.lexer import Lexer, Token, IMPORT, PRAGMA


class LexerTestCase(TestCase):
    def test_import(self):
        src = "import foo\n import bar"
        lexer = Lexer(src)
        lexer.tokenize()
        self.assertEqual(lexer.tokens[0], Token(IMPORT, "import foo", 0))
        self.assertEqual(lexer.tokens[1], Token(IMPORT, "import bar", 12))

    def test_pragma(self):
        src = "pragma foo\n pragma bar"
        lexer = Lexer(src)
        lexer.tokenize()
        self.assertEqual(lexer.tokens[0], Token(PRAGMA, "pragma foo", 0))
        self.assertEqual(lexer.tokens[1], Token(PRAGMA, "pragma bar", 12))
