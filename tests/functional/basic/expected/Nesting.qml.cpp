using namespace QtQuick;
using namespace QtQuick::Controls;
/*
 * Header bla
 */
/**
 * Parent item.
 */
class Nesting : public Item {
public:
/**
     * A child with an ID.
     */
Item childItem;
class Item {
public:

/** An attribute. */
var componentAttribute;
/** Another attribute. */
var component.attribute;
/**
         * A function in a component.
         * @param str The string to append 'a' to. 
         * @return The new string.
         */
string itemFunction(string str);
};
/**
     * Another child with an ID.
     */
Item childItem2;
class Item {
public:

};
ShowChildComponent customComponentChildItem;
class ShowChildComponent {
public:

/** An attribute. */
var componentAttribute;
/** Another attribute. */
var component.attribute;
/**
             * A function in a component.
             * @param str The string to append 'a' to. 
             * @return The new string.
             */
string showFunction(string str);
};

/**
         * A grandchild with an ID.
         */
ShowChildComponent showCustomComponentChildItem;
class ShowChildComponent {
public:

/** An attribute. */
var componentAttribute;
/** Another attribute. */
var component.attribute;
/**
             * A function in a component.
             * @param str The string to append 'a' to. 
             * @return The new string.
             */
string showFunction(string str);
};
/**
     * A comment for aSplitView
     */
SplitView aSplitView;
class SplitView {
public:

var Layout.fillHeight;
var Layout.fillWidth;
};
/**
         * A comment for aRectangle.
         */
Rectangle aRectangle;
class Rectangle {
public:

};
};
