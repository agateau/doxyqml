# Goals

Doxyqml turns .qml into pseudo-C++ which Doxygen can then use to generate
documentation.

# Installing

Doxyqml uses the standard Python setup tools, so you can install it with:

    python setup.py install

# Telling Doxygen to use Doxyqml

Edit your Doxygen file: first you need to set the `FILTER_PATTERNS` key to
associate .qml files with Doxyqml:

    FILTER_PATTERNS = *.qml=doxyqml

Note: On Windows you may need to use the full path of the `doxyqml.py` file
instead. For example if you installed Python 2.7 in `C:\Python27`, use this:

    FILTER_PATTERNS = *.qml=C:\Python27\Lib\site-packages\doxyqml\doxyqml.py

Then you must add .qml files to `FILE_PATTERNS`:

    FILE_PATTERNS = *.qml

# Documenting types

QML is partly-typed: functions are untyped, properties and signals are. Doxyqml
provides a way to define types when they are missing or not precise enough.

## Functions

Functions in QML are untyped, but you can define types in the documentation
like this:

    /**
     * Create a user
     * @param type:string firstname User firstname
     * @param type:string lastname User lastname
     * @param type:int User age
     * @return type:User The User object
     */
    function createUser(firstname, lastname, age);

## Properties

QML properties are typed, so Doxyqml uses them by default. You can nevertheless
overwrite the type using the same `type:<name>` syntax. This is useful to
document property aliases:

    /** type:string The user lastname */
    property alias lastname: someObject.text

## Signals

QML signals are typed, so there is no need to use the `type:<name>` syntax to
document their parameters. Using `type:<name>` syntax in signal documentation
will not work: Doxyqml won't strip it out and Doxygen will confuse it with the
parameter name.

    /**
     * User just logged in
     * @param user The user which logged in
     */
    signal loggedIn(User user)
