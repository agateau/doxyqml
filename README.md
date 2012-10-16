# Goals

Turn a .qml into something Doxygen can swallow

When parsing Foo.qml:

    FooBase {
    => class Foo : public FooBase {

    property $type $name
    => Q_PROPERTY($type $name)

    signal $name[(<$type $argname>...)]
    => Q_SIGNAL void $name($type $argname,...)

    function $name(<$type $argname>...)
    => Q_INVOKABLE void $name($type $argname,...)
    // Note: Need comment for return type

Ignore inner elements.

Needs two extract modes:

- extract-documented: only extract elements with a Doxygen comment block
- extract-all: extract all elements

Should be extract-documented by default to enforce good practices: an element
is private unless documented (and not documented as @internal)

# Implementation

First approach: not a full-parser, just replace interesting lines with their
C++ equivalent, remove lines for inner elements.
