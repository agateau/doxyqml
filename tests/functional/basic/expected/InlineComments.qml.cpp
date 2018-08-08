using namespace QtQuick;
/*
 * Header bla
 */
///< What happens here?
/**
 * A very simple item   ///< How about here?
 */
class InlineComments : public Item {
public:
Q_PROPERTY(int foo) ///< The 'foo' property
Q_SIGNALS: void clicked(int x, int y); /**< The `clicked` signal */
public:
Q_SIGNALS: void activated(); //!< Another signal
public:
void doSomething(string arg1, int arg2); /*!< @param arg1 first argument @param arg2 second argument */
/**
     * A weirdly documented function.... the inline comment will be stripped. Doxygen would ignore the inline comment anyway.
     * @param foo first argument
     * @param bar this argument does exist
     */
void weirdlyDocumented(string foo, int bar);
Q_PROPERTY(string escaped) ///< and an inline comment
Q_PROPERTY(string block) /**< and an inline comment! ***<  //!<  */
int square(arg); ///< Compute the arg^2. @return the result
void refresh(); ///< Inline comment out of place (should be moved inline in the output)
// Just some regular comment
void reload(); ///< Inline comment for a keyword following a regular comment.
/*!  Just for fun...
      ///< Inline comment
      //!< Inline comment
      @param arg1 first argument
      @param arg2 second argument
      /*!< Inline comment
    */
void update(string arg1, int arg2);

Q_PROPERTY(int weirdProperty)
/* baz */
/* foo */
///< and a useless inline comment
};
