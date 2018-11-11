/*
 * Header bla
 */
import QtQuick 1.1
import QtQuick.Controls 1.4 as QtQuick1

/**
 * Parent item.
 */
Item {

    /**
     * A child with an ID.
     */
    Item {

        id: childItem

        /** An attribute. */
        componentAttribute: value

        /** Another attribute. */
        component.attribute: anotherValue

        /**
         * A function in a component.
         * @param type:string str The string to append 'a' to.
         * @return type:string The new string.
         */
        function itemFunction(str) {
            return str + "a";
        }
    }

    /**
     * Another child with an ID.
     */
    Item {

        id: childItem2

        ShowChildComponent {

            id: customComponentChildItem

            /** An attribute. */
            componentAttribute: value

            /** Another attribute. */
            component.attribute: anotherValue

            /**
             * A function in a component.
             * @param type:string str The string to append 'a' to.
             * @return type:string The new string.
             */
            function showFunction(str) {
                return str + "a";
            }
        }

        HideCustomComponent {

            /** An attribute. */
            componentAttribute: value

            /** Another attribute. */
            component.attribute: anotherValue

            /**
             * A function in a component.
             * @param type:string str The string to append 'a' to.
             * @return type:string The new string.
             */
            function hideFunction(str) {
                return str + "a";
            }
        }
    }

    /**
     * A child without an ID.
     */
    Item {

        /** Attribute not shown for component with no ID. */
        attributeNotShown: value

        /**
         * A grandchild with an ID.
         */
        ShowChildComponent {

            id: showCustomComponentChildItem

            /** An attribute. */
            componentAttribute: value

            /** Another attribute. */
            component.attribute: anotherValue

            /**
             * A function in a component.
             * @param type:string str The string to append 'a' to.
             * @return type:string The new string.
             */
            function showFunction(str) {
                return str + "a";
            }
        }
    }

    /**
     * A comment for aSplitView
     */
    QtQuick1.SplitView {

        id: aSplitView

        Layout.fillHeight: true
        Layout.fillWidth: true

        /**
         * A comment for aRectangle.
         */
        Rectangle {

            id: aRectangle
        }
    }
}
