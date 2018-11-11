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
private:
/**
     * A child with an ID.
     */
Item childItem;
/**
     * Another child with an ID.
     */
Item childItem2;
ShowChildComponent customComponentChildItem;
/**
         * A grandchild with an ID.
         */
ShowChildComponent showCustomComponentChildItem;
/**
     * A comment for aSplitView
     */
SplitView aSplitView;
/**
         * A comment for aRectangle.
         */
Rectangle aRectangle;
};
