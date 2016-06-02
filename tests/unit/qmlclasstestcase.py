import re
from unittest import TestCase

from doxyqml.qmlclass import QmlFunction, QmlArgument, QmlProperty

class QmlFunctionTestCase(TestCase):
    def test_post_process_doc_at(self):
        self._test_post_process_doc("""
        /**
         * Create a user
         *
         * @param type:string firstname The user firstname
         * @param type:string lastname The user lastname
         * @param type:int age The user age
         * @param misc A parameter with no type
         * @return type:User A new user
         */
         """)

    def test_post_process_doc_backslash(self):
        self._test_post_process_doc(r"""
        /**
         * Create a user
         *
         * \param type:string firstname The user firstname
         * \param type:string lastname The user lastname
         * \param type:int age The user age
         * \param misc A parameter with no type
         * \return type:User A new user
         */
         """)

    def _test_post_process_doc(self, doc):
        fcn = QmlFunction()
        fcn.args = [
            QmlArgument("firstname"),
            QmlArgument("lastname"),
            QmlArgument("age"),
            QmlArgument("misc"),
            ]
        fcn.doc = doc
        fcn.post_process_doc()

        self.assertEqual(fcn.args[0].type, "string")
        self.assertEqual(fcn.args[1].type, "string")
        self.assertEqual(fcn.args[2].type, "int")
        self.assertEqual(fcn.args[3].type, "")
        self.assertEqual(fcn.type, "User")

        # "[@\]param type:..." are turned into "@param"
        expected_doc = re.sub(r"[@\\]param type:\w+", r"@param", doc)
        # "[@\]return type:..." are turned into "[@\]return"
        expected_doc = re.sub(r"([@\\])return type:\w+", r"\1return", expected_doc)
        self.assertMultiLineEqual(fcn.doc, expected_doc)


class QmlPropertyTestCase(TestCase):
    def test_property_type(self):
        prop = QmlProperty()
        prop.doc = "/// type:User The current user"
        prop.type = "alias"

        prop.post_process_doc()

        self.assertEqual(prop.type, "User")
        self.assertEqual(prop.doc, "/// The current user")

    def test_no_property_type(self):
        prop = QmlProperty()
        prop.doc = "/// The user age"
        prop.type = "int"

        prop.post_process_doc()

        self.assertEqual(prop.type, "int")
        self.assertEqual(prop.doc, "/// The user age")

    def test_default_property(self):
        prop = QmlProperty()
        prop.doc = "/// Children"
        prop.type = "list<Item>"
        prop.is_default = True

        prop.post_process_doc()

        self.assertEqual(prop.doc, "/// Children\n" + QmlProperty.DEFAULT_PROPERTY_COMMENT)
