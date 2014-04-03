using namespace QtQuick;
/*
 * Header bla
 */
/**
 * A very simple item
 */
class FunctionArgs : public Item {
public:
/**
     * The 'foo' property
     */
Q_PROPERTY(int foo)

Q_SIGNALS: void clicked(int x, int y); public:

Q_SIGNALS: void activated(); public:
/**
     * Do something with arg1 and arg2
     * @param arg1 first argument
     * @param arg2 second argument
     */
void doSomething(string arg1, int arg2);
/**
     * A badly documented function. Missing one argument and documenting a
     * non-existing document
     * @param foo first argument
     * @param baz this argument does not exist
     */
void badlyDocumented(string foo, bar);

Q_PROPERTY(string escaped)

Q_PROPERTY(string block)
/**
     * Compute the arg^2
     * @return the result
     */
int square(arg);
/// One-line comment
void refresh();

Q_PROPERTY(int weirdProperty)
/* baz */
/* foo */
};
