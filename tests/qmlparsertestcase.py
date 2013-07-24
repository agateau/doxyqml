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

    def test_default_property(self):
        src = """Item {
            /// v1 doc
            default property int v1
            /// v2 doc
            property int v2
            }"""
        lexer = Lexer(src)
        lexer.tokenize()
        qmlclass = QmlClass("Foo")
        qmlparser.parse(lexer.tokens, qmlclass)

        self.assertEqual(qmlclass.properties[0].name, "v1")
        self.assertEqual(qmlclass.properties[0].type, "int")
        self.assertEqual(qmlclass.properties[0].doc, "/// v1 doc")
        self.assert_(qmlclass.properties[0].is_default)

        self.assertEqual(qmlclass.properties[1].name, "v2")
        self.assertEqual(qmlclass.properties[1].type, "int")
        self.assertEqual(qmlclass.properties[1].doc, "/// v2 doc")
        self.assert_(not qmlclass.properties[1].is_default)

    def test_var_property(self):
        src = """Item {
            property var varProperty: { "key1": "value1", "key2": "value2" }
            }"""

        lexer = Lexer(src)
        lexer.tokenize()
        qmlclass = QmlClass("Foo")
        qmlparser.parse(lexer.tokens, qmlclass)

        self.assertEqual(qmlclass.properties[0].name, "varProperty")
        self.assertEqual(qmlclass.properties[0].type, "var")

    def test_function_property(self):
        src = """Item {
            property var fnProperty: function (arg1, arg2) { return arg1 + arg2; }
            }"""

        lexer = Lexer(src)
        lexer.tokenize()
        qmlclass = QmlClass("Foo")
        qmlparser.parse(lexer.tokens, qmlclass)

        self.assertEqual(qmlclass.properties[0].name, "fnProperty")
        self.assertEqual(qmlclass.properties[0].type, "var")

    def test_normal_arguments(self):
        src = """Item {
                     function foo(arg1, arg2) {
                         return arg1 + arg2;
                     }
                 }"""

        lexer = Lexer(src)
        lexer.tokenize()
        qmlclass = QmlClass("Foo")
        qmlparser.parse(lexer.tokens, qmlclass)

        self.assertEqual(qmlclass.functions[0].name, "foo")
        self.assertEqual(qmlclass.functions[0].type, "void")

    def test_keyword_arguments(self):
        src = """Item {
                     function foo(propertyArgument, signalArgument) {
                         return propertyArgument + signalArgument;
                     }
                 }"""

        lexer = Lexer(src)
        lexer.tokenize()
        qmlclass = QmlClass("Foo")
        qmlparser.parse(lexer.tokens, qmlclass)

        self.assertEqual(qmlclass.functions[0].name, "foo")
        self.assertEqual(qmlclass.functions[0].type, "void")
