# Goals

Turns a .qml into something Doxygen can swallow through an input filter.

# Setup

First, make sure doxyqml is in $PATH. For example with:

    ln -s /path/to/doxyqml.py $HOME/bin/doxyqml

Then in your Doxygen file, add .qml files to `FILE_PATTERNS`:

    FILE_PATTERNS = *.qml

And set `FILTER_PATTERNS`:

    FILTER_PATTERNS = *.qml=doxyqml

# Documenting types

QML is partly-typed: functions are untyped, properties and signals are. Doxyqml
provide a way to define types where they are missing.

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

QML properties are typed, doxyqml will take advantage of the existing type. You
can nevertheless overwrite the type using the same `type:<name>` syntax. This is
useful for example to document property aliases:

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
