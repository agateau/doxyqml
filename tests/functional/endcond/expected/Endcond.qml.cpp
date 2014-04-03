using namespace QtQuick;
class Endcond : public Item {
public:
/**
     * The 'foo' property
     */
Q_PROPERTY(int foo)
/// @cond TEST
/// A test property, not visible by default
Q_PROPERTY(int test)
/// @endcond TEST
};
