Item {
    property int foo

    /**
     * Do something with arg1 and arg2
     */
    function doSomething(arg1, arg2) {
        console.log("arg1=" + arg1);
    }

    /**
     * Compute the arg^2
     * @return int
     */
    function square(arg) {
        return arg * arg;
    }
}
