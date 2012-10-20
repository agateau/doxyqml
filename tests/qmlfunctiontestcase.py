from unittest import TestCase

from qmlclass import QmlFunction, QmlArgument

class QmlFunctionTestCase(TestCase):
    def test_post_process_doc(self):
        fcn = QmlFunction()
        fcn.args = [
            QmlArgument("firstname"),
            QmlArgument("lastname"),
            QmlArgument("age"),
            ]
        fcn.doc = ["""
        /**
         * Create a user
         *
         * @param string firstname The user firstname
         * @param string lastname The user lastname
         * @param int age The user age
         */
         """]

        fcn.post_process_doc()

        self.assertEqual(fcn.args[0].type, "string")
        self.assertEqual(fcn.args[1].type, "string")
        self.assertEqual(fcn.args[2].type, "int")

        self.assertMultiLineEqual(fcn.doc[0], """
        /**
         * Create a user
         *
         * @param firstname The user firstname
         * @param lastname The user lastname
         * @param age The user age
         */
         """)
