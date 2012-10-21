from unittest import TestCase

from lexer import Lexer

from qmlclass import QmlClass
import qmlparser

class QmlParserTestCase(TestCase):
    def test(self):
        src = "Item { function foo() {} function bar() {} }"
        lexer = Lexer(src)
        lexer.tokenize()
        qmlclass = QmlClass("Foo")
        qmlparser.parse(lexer.tokens, qmlclass)

        self.assertEqual(qmlclass.base_name, "Item")

        self.assertEqual(qmlclass.functions[0].name, "foo")
        self.assertEqual(qmlclass.functions[1].name, "bar")
        self.assertEqual(len(qmlclass.functions), 2)
