/*
 * Header bla
 */
import QtQuick 1.1

/**
 * A very simple item
 */
Item {
    property int foo

    signal clicked(int x, int y)

    /**
     * Do something with arg1 and arg2
     */
    function doSomething(arg1, arg2) {
        console.log("arg1=" + arg1);
    }

    property string escaped: "a string \n \" \t with escaped chars"
    property string block: "a string with some block {({ ] } chars"

    /**
     * Compute the arg^2
     * @return int
     */
    function square(arg) {
        return arg * arg;
    }

    /// One-line comment
    function refresh() {
    }

    Item {
    }

    property /* foo */ int /* bar */ weirdProperty /* baz */ : /* foo */ 12
}
