/*
 * Header bla
 */
import QtQuick 1.1

///< What happens here?
/**
 * A very simple item   ///< How about here?
 */
Item {
    property int foo  ///< The 'foo' property

    signal clicked(int x, int y)  /**< The `clicked` signal */

    signal activated  //!< Another signal

    function doSomething(arg1, arg2) {   /*!< @param type:string arg1 first argument @param type:int arg2 second argument */
        console.log("arg1=" + arg1);
    }

    /**
     * A weirdly documented function.... the inline comment will be stripped. Doxygen would ignore the inline comment anyway.
     * @param type:string foo first argument
     * @param type:int bar this argument does exist
     */
    function weirdlyDocumented(foo, bar) {  //!< A weirdly documented function!
    }

    property string escaped: "a string \n \" \t with escaped chars"  ///< and an inline comment
    property string block: "a string with some block {({ ] } chars"  /**< and an inline comment! ***<  //!<  */

    function square(arg)    ///< Compute the arg^2. @return type:int the result
    {
        return arg * arg;
    }

    ///< Inline comment out of place (should be moved inline in the output)
    function refresh() {
    }

    // Just some regular comment

    function reload() ///< Inline comment for a keyword following a regular comment.
    {}

    /*!  Just for fun...
      ///< Inline comment
      //!< Inline comment
      @param type:string arg1 first argument
      @param type:int arg2 second argument
      /*!< Inline comment
    */
    function update(arg1, arg2) { }

    Item {
    }

    property /* foo */ int /* bar */ weirdProperty /* baz */ : /* foo */ 12   ///< and a useless inline comment
}
