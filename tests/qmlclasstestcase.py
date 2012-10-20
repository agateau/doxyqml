from unittest import TestCase

from qmlclass import QmlFunction, QmlArgument, QmlProperty

class QmlFunctionTestCase(TestCase):
    def test_post_process_doc(self):
        fcn = QmlFunction()
        fcn.args = [
            QmlArgument("firstname"),
            QmlArgument("lastname"),
            QmlArgument("age"),
            QmlArgument("misc"),
            ]
        fcn.doc = """
        /**
         * Create a user
         *
         * @param type:string firstname The user firstname
         * @param type:string lastname The user lastname
         * @param type:int age The user age
         * @param misc A parameter with no type
         * @return type:User A new user
         */
         """

        fcn.post_process_doc()

        self.assertEqual(fcn.args[0].type, "string")
        self.assertEqual(fcn.args[1].type, "string")
        self.assertEqual(fcn.args[2].type, "int")
        self.assertEqual(fcn.args[3].type, "")
        self.assertEqual(fcn.type, "User")

        self.assertMultiLineEqual(fcn.doc, """
        /**
         * Create a user
         *
         * @param firstname The user firstname
         * @param lastname The user lastname
         * @param age The user age
         * @param misc A parameter with no type
         * @return A new user
         */
         """)

class QmlPropertyTestCase(TestCase):
    def test_property_type(self):
        prop = QmlProperty()
        prop.doc = "/// type:User The current user"
        prop.type = "alias"

        prop.post_process_doc()

        self.assertEqual(prop.type, "User")
        self.assertEqual(prop.doc, "/// The current user")
